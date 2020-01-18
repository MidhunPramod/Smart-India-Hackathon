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
    df = pd.read_sql_query("select * from grievance;".format(institute), conn)

    # Get counts of groups of 'class' and fill in 'year_month_id' column
    df4 = DataFrame({'count3': df.groupby(["g_type"]).size()}).reset_index()
    palette=['#F67088','#DC882E','#33AF79','#6E9AF3','#F963CF','#37ACA4']
    # x and y axes
    g_type=df4['g_type'].tolist()
    count3=df4['count3'].tolist()

    # Bokeh's mapping of column names and data lists
    source3 = ColumnDataSource(data=dict(g_type=g_type, count3=count3, color=palette))

    #The entire p1 thing is for the pie chart, p2 and p3 are bar graphs
    p3 = figure(x_range=g_type, y_range=(0, 5), plot_height=350, title="Grievance Division",
            toolbar_location=None, tools="")

    # # Render and show the vbar plot
    p3.vbar(x='g_type', top='count3', width=0.4, color='color', source=source3)

    #tooltips add hovertools (i.e. interactive stuff)

    tooltips3 = [
                ('Grievance Type','@g_type'),
                ('No. of grievances', '@count3'),
                ]
    p3.add_tools(HoverTool(tooltips=tooltips3))

    #FINAL SHOW :')
    #show(p3)
    output_file('templates/graph3.html')
    save(p3)