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
from bokeh.plotting import figure, show, save
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

def makegraph(institute):
    conn = sqlite3.connect("portal.db")
    df = pd.read_sql_query("select * from grievance;", conn)
    df_alt = pd.read_sql_query("select * from grievance;", conn) #alternate database for specific college, didn't use it tho

    # Get counts of groups of 'class' and fill in 'year_month_id' column
    df2 = DataFrame({'count': df.groupby(["mood"]).size()}).reset_index()
    df3 = DataFrame({'count2': df.groupby(["status"]).size()}).reset_index()
    df4 = DataFrame({'count3': df.groupby(["g_type"]).size()}).reset_index()
    palette=['#F67088','#DC882E','#33AF79','#6E9AF3','#F963CF','#37ACA4']
    print(df2)
    # x and y axes
    count2= df3['count2'].tolist()
    status=df3['status'].tolist()
    # Bokeh's mapping of column names and data lists
    source2 = ColumnDataSource(data=dict(status=status, count2=count2, color=palette))

    #The entire p1 thing is for the pie chart, p2 and p3 are bar graphs
    p2 = figure(x_range=status, y_range=(0, 5), plot_height=350, title="Grievance Status",
            toolbar_location=None, tools="")

    # # Render and show the vbar plot
    p2.vbar(x='status', top='count2', width=0.2, color='color', source=source2)

    #tooltips add hovertools (i.e. interactive stuff)

    tooltips2 = [
                ('Status','@status'),
                ('No. of grievances', '@count2'),
                ]

    p2.add_tools(HoverTool(tooltips=tooltips2))

    #FINAL SHOW :')
    #show(p2)
    output_file('templates/graph2.html')
    save(p2)
