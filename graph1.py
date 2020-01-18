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
        #df_alt = pd.read_sql_query("select * from grievance where institute='MIT';", conn) #alternate database for specific college, didn't use it tho

        # Get counts of groups of 'class' and fill in 'year_month_id' column
        df2 = DataFrame({'count': df.groupby(["mood"]).size()}).reset_index()
        df3 = DataFrame({'count2': df.groupby(["status"]).size()}).reset_index()
        df4 = DataFrame({'count3': df.groupby(["g_type"]).size()}).reset_index()

        print(df2)
        # x and y axes
        df2['angle'] = df2['count']/df2['count'].sum() * 2*pi

        palette={1:['#EC6B56'],2:['#EC6B56','#47B39C'] ,3:['#EC6B56','#47B39C','#FFC154']}
        df2['color']=palette[len(df2)]
        if(len(df2)>3):
                df2['color'] = Category10[len(df2)]
        else:
                df2['color'] = palette[len(df2)]
                
        # df2.loc[(df2['color']=='#1f77b4'), 'color'] = '#EC6B56'
        # df2.loc[(df2['color']=='#ff7f0e'), 'color'] = '#47B39C'
        # df2.loc[(df2['color']=='#2ca02c'), 'color'] = '#FFC154'


        # Bokeh's mapping of column names and data lists
        #source1 = ColumnDataSource(data=dict(mood=mood, count=count, color=Viridis5)) (USE THIS ONLY FOR BARGRAPH, SINCE FIRST PLOT PIE CHART, COMMENTED OUT)


        #The entire p1 thing is for the pie chart, p2 and p3 are bar graphs
        p1 = figure(plot_height=350, title="Mood Analysis", toolbar_location=None,
                tools="hover", tooltips="@mood: @count", x_range=(-0.5, 1.0))

        p1.wedge(x=0, y=1, radius=0.4,
                start_angle=cumsum('angle', include_zero=True), end_angle=cumsum('angle'),
                line_color="white", fill_color='color', legend_field='mood', source=df2)

        p1.axis.axis_label=None
        p1.axis.visible=False
        p1.grid.grid_line_color = None



        #tooltips add hovertools (i.e. interactive stuff)



        #FINAL SHOW :')
        #show(p1)
        output_file('templates/graph1.html')
        save(p1)