import flask
import pandas as pd
import numpy as np

import blaze as bz
from into import into

from bokeh.embed import components
from bokeh.resources import INLINE
from bokeh.templates import RESOURCES
from bokeh.utils import encode_utf8

from bokeh.models import ColumnDataSource
import bokeh.plotting as plt


app = flask.Flask(__name__)
db = bz.Data('sqlite:///../lahman2013.sqlite')
distinct_teams = list(db.Salaries.teamID.distinct())
distinct_years = list(db.Salaries.yearID.distinct())

def create_plot(team="LAA", year=2012):
    expr = bz.by(db.Salaries.teamID,
                 avg=db.Salaries.salary.mean(),
                 max=db.Salaries.salary.max(),
                 ratio=db.Salaries.salary.max() / db.Salaries.salary.min())
    expr = expr.sort('ratio', ascending=False)

    df_salary_gb = into(pd.DataFrame, expr)
    source1 = into(ColumnDataSource, df_salary_gb[["teamID", "avg"]])

    plot1 = plt.figure(title="Salary ratio by team", x_range=list(df_salary_gb["teamID"]))
    plot1.scatter(x="teamID", y="avg", source=source1, size=20)
    plot1.xaxis.major_label_orientation = np.pi/3

    df = into(pd.DataFrame, db.Salaries)
    df = df[df["teamID"] == team]
    df = df[df["yearID"] == year]

    df = df[["playerID","salary"]].sort('salary')
    source_team = into(ColumnDataSource, df)
    p_team = plt.figure(title="Salary of players for %s during %s" % (team, year),
                        x_range=list(df["playerID"]))#, tools=TOOLS)
    p_team.scatter(x="playerID", y="salary", source=source_team, size=20)
    p_team.xaxis.major_label_orientation = np.pi/3

    p = plt.gridplot([[plot1, p_team]])
    return p

@app.route("/")
def index():
    args = flask.request.args
    selected_team = flask.request.values.get("selected_team", "LAA")
    selected_year = int(flask.request.values.get("selected_year", "2012"))

    p = create_plot(selected_team, selected_year)
    plot_resources = RESOURCES.render(
        js_raw=INLINE.js_raw,
        css_raw=INLINE.css_raw,
        js_files=INLINE.js_files,
        css_files=INLINE.css_files,
    )
    script, div = components(p, INLINE)
    html = flask.render_template(
        'embed.html',
        plot_script=script,
        plot_div=div,
        plot_resources=plot_resources,
        selected_team=selected_team,
        selected_year=selected_year,
        years=distinct_years,
        teams=distinct_teams,
    )
    return encode_utf8(html)


if __name__ == "__main__":
    app.run(debug=True)
