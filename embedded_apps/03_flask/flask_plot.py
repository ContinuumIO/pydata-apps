import flask

from bokeh.embed import components
from bokeh.resources import INLINE
from bokeh.templates import RESOURCES
from bokeh.util.string import encode_utf8

from bokeh.models import ColumnDataSource
import bokeh.plotting as plt

import numpy as np



app = flask.Flask(__name__)


def create_plot(N, func1, func2, color):
    N = 300
    x = np.linspace(0, 4*np.pi, N)
    y1 = np.sin(x)
    y2 = np.cos(x)

    source = ColumnDataSource()
    source.add(data=x, name='x')
    source.add(data=y1, name='y1')
    source.add(data=y2, name='y2')

    TOOLS = "pan,wheel_zoom,box_zoom,reset,save,box_select,lasso_select"

    s1 = plt.figure(tools=TOOLS, plot_width=350, plot_height=350)
    s1.scatter('x', 'y1', source=source, fill_color=color)

    s2 = plt.figure(tools=TOOLS, plot_width=350, plot_height=350)
    s2.scatter('x', 'y2', source=source, fill_color=color)

    p = plt.gridplot([[s1,s2]])
    return p


@app.route("/")
def index():
    args = flask.request.args
    color = flask.request.values.get("color", "black")


    p = create_plot(300, np.sin, np.cos, color=color)
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
        color=color
    )
    return encode_utf8(html)


if __name__ == "__main__":
    app.run(debug=True)
