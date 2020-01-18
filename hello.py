# Data handling
import pandas as pd
import numpy as np
from pandas import DataFrame
import sqlite3
from math import pi
from flask import Flask, render_template
# Bokeh libraries
from bokeh.io import output_file
from bokeh.io.export import get_layout_html
from bokeh.plotting import figure, show
from bokeh.models import ColumnDataSource, NumeralTickFormatter
from bokeh.layouts import row, column, gridplot
from bokeh.models.widgets import Tabs, Panel
from bokeh.palettes import Viridis5, Category10, Magma 
from bokeh.models import HoverTool
from bokeh.transform import cumsum
from bokeh.embed import components
from bokeh.resources import CDN
from jinja2 import Template
from bokeh.embed import server_document


conn = sqlite3.connect("portal.db")
df = pd.read_sql_query("select * from grievance;", conn)
df_alt = pd.read_sql_query("select * from grievance where institute='MIT';", conn) #alternate database for specific college, didn't use it tho

# Get counts of groups of 'class' and fill in 'year_month_id' column
df2 = DataFrame({'count': df.groupby(["mood"]).size()}).reset_index()
df3 = DataFrame({'count2': df.groupby(["status"]).size()}).reset_index()
df4 = DataFrame({'count3': df.groupby(["g_type"]).size()}).reset_index()

print(df2)
# x and y axes
df2['angle'] = df2['count']/df2['count'].sum() * 2*pi
df2['color'] = Category10[len(df2)]
df2.loc[(df2['color']=='#1f77b4'), 'color'] = '#EC6B56'
df2.loc[(df2['color']=='#ff7f0e'), 'color'] = '#47B39C'
df2.loc[(df2['color']=='#2ca02c'), 'color'] = '#FFC154'
count2= df3['count2'].tolist()
status=df3['status'].tolist()
g_type=df4['g_type'].tolist()
count3=df4['count3'].tolist()

# Bokeh's mapping of column names and data lists
#source1 = ColumnDataSource(data=dict(mood=mood, count=count, color=Viridis5)) (USE THIS ONLY FOR BARGRAPH, SINCE FIRST PLOT PIE CHART, COMMENTED OUT)
source2 = ColumnDataSource(data=dict(status=status, count2=count2, color=Viridis5))
source3 = ColumnDataSource(data=dict(g_type=g_type, count3=count3, color=Viridis5))

#The entire p1 thing is for the pie chart, p2 and p3 are bar graphs
p1 = figure(plot_height=350, title="Mood Analysis", toolbar_location=None,
           tools="hover", tooltips="@mood: @count", x_range=(-0.5, 1.0))

p1.wedge(x=0, y=1, radius=0.4,
        start_angle=cumsum('angle', include_zero=True), end_angle=cumsum('angle'),
        line_color="white", fill_color='color', legend_field='mood', source=df2)

p1.axis.axis_label=None
p1.axis.visible=False
p1.grid.grid_line_color = None

p2 = figure(x_range=status, y_range=(0, 5), plot_height=350, title="Grievance Status",
           toolbar_location=None, tools="")

p3 = figure(x_range=g_type, y_range=(0, 5), plot_height=350, title="Grievance Division",
           toolbar_location=None, tools="")

# # Render and show the vbar plot

p2.vbar(x='status', top='count2', width=0.5, color='color', source=source2)
p3.vbar(x='g_type', top='count3', width=0.2, color='color', source=source3)

#tooltips add hovertools (i.e. interactive stuff)

tooltips2 = [
             ('Status','@status'),
             ('No. of grievances', '@count2'),
            ]

tooltips3 = [
             ('Grievance Type','@g_type'),
             ('No. of grievances', '@count3'),
            ]

p2.add_tools(HoverTool(tooltips=tooltips2))
p3.add_tools(HoverTool(tooltips=tooltips3))

#FINAL SHOW :') 
show(column(p1,p2,p3))

f = column(p1,p2,p3)

script, divs = components((p1, p2, p3))
div1, div2, div3 = divs