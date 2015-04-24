from bokeh.models import ColumnDataSource
from bokeh.plotting import *

import numpy as np

output_file("static_plot.html")

N = 300
x = np.linspace(0, 4*np.pi, N)
y1 = np.sin(x)
y2 = np.cos(x)

source = ColumnDataSource()
source.add(data=x, name='x')
source.add(data=y1, name='y1')
source.add(data=y2, name='y2')

TOOLS = "pan,wheel_zoom,box_zoom,reset,save,box_select,lasso_select"

s1 = figure(tools=TOOLS, plot_width=350, plot_height=350)
s1.scatter('x', 'y1', source=source)

s2 = figure(tools=TOOLS, plot_width=350, plot_height=350)
s2.scatter('x', 'y2', source=source)

p = gridplot([[s1,s2]])
show(p)
