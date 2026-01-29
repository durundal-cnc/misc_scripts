# -*- coding: utf-8 -*-
"""
Created on Thu Aug  8 09:09:47 2019

@author: amiller
"""
import sys
sys.path.append(r'L:\Research and Engineering\Data for Projects\MAISE\MaiseSoftwareTools\egmm_analysis_scripts');
import grainmoisture.emc as emc



import os
import pickle
import math
import pandas as pd

import numpy as np
import holoviews as hv
from holoviews import opts, dim
import sys
sys.path.append(r'L:\Research and Engineering\Data for Projects\MAISE\MaiseSoftwareTools\egmm_analysis_scripts');

import grainmoisture.emc as emc

import plotly
import plotly.graph_objs as go
from ast import literal_eval
import re

## add hvplot extension
#import hvplot.pandas
#import hvplot
#hv.extension('bokeh')   # make it possible to use holoviews with bokeh in jupyterlab
#from bokeh.plotting import figure, output_file, show
#import holoviews.plotting.bokeh

from bokeh.plotting import figure, show, output_file, save
from bokeh.models import ColumnDataSource, ColorBar, LinearColorMapper, Title, Range1d, CustomJS, Label, HoverTool
#from bokeh.palettes import viridis, Spectral6, Viridis3, Viridis256
#from bokeh.transform import linear_cmap

from bokeh.layouts import widgetbox,column,layout,gridplot
from bokeh.models.widgets import Dropdown, MultiSelect, Select,CheckboxGroup,Slider,DataTable, DateFormatter, TableColumn,TextInput
import sys
sys.path.append(r'L:\Research and Engineering\Data for Projects\MAISE\MaiseSoftwareTools\egmm_analysis_scripts\egmmlibrary')

# this library itself imports the sqlalchemy models used in web-app
# connection to the mysqlserver is also handled in this file
import use_the_egmm3_maise_database as db

from bokeh.palettes import Category20_20 as palette
from bokeh.palettes import Spectral10 as palette2

sys.path.append(r'L:\Research and Engineering\Data for Projects\MAISE\MaiseSoftwareTools\testing_scripts\egmm3_webui_gitremote\egmm3tools')

from loaders.testset import massaged_labtest_loader
from loaders.testset import massaged_fieldtest_loader

import itertools

#%% import hobo data
def C(f):
    c = (5.0/9)*(f - 32)
    return c

def F(c):
    f = (9.0/5)*c + 32
    return f


path = r'C:\Users\amiller\Desktop\wagtech incubator'
filelist = os.listdir(path)
filelist = [x for x in filelist if '.hobo' not in x]

for file in filelist:
    hobo_df = pd.read_csv(path+'\\'+ file, delimiter=',',skiprows=0,header=1)  # doctest: +SKIP
    hobo_df['time'] = pd.to_datetime(hobo_df.iloc[:,1], format='%m/%d/%y %I:%M:%S %p')
    hobo_df['Top'] = [C(f) for f in hobo_df.iloc[:,2]]
    hobo_df['TopMid'] = [C(f) for f in hobo_df.iloc[:,3]]
    hobo_df['BotMid'] = [C(f) for f in hobo_df.iloc[:,4]]
    hobo_df['Bot'] = [C(f) for f in hobo_df.iloc[:,5]]

    hobo_df.drop(hobo_df.columns.difference(['Top','TopMid','BotMid','Bot','time']), 1, inplace=True)


#%% plot
        
ymin = 30
ymax =100
xmin = -100
xmax = 900
TOOLS="crosshair,pan,wheel_zoom,zoom_in,zoom_out,box_zoom,undo,redo,reset,tap,save,box_select,poly_select,lasso_select,"
TOOLTIPS  = [
#    ("index", "$index"),
#    ("(x,y)", "($x, $y)"),
("time", "@time{%m/%d/%y %I:%M:%S %p}"),
("Top", "@{Top}"),
("TopMid", "@{TopMid}"),
("BotMid", "@{BotMid}"),
("Bot", "@{Bot}"),

]
   

# also plot with shifted x axis
title = 'Wagtech incubator without calibration'
print(title)

p = figure(title=title,tools=TOOLS,tooltips=TOOLTIPS,plot_width=1500, plot_height=800,x_axis_type='datetime')

hover = HoverTool(tooltips=TOOLTIPS, formatters={'time':'datetime'})
p.add_tools(hover)
#
#p.circle(hobo_df['time'],hobo_df['Top'], alpha=0.4, color='black',legend='Top')
#p.circle(hobo_df['time'],hobo_df['TopMid'], alpha=0.4, color='red',legend='TopMid')
#p.circle(hobo_df['time'],hobo_df['BotMid'],  alpha=0.4, color='green',legend='BotMid')
#p.circle(hobo_df['time'],hobo_df['Bot'],  alpha=0.4, color='blue',legend='Bot')

source = ColumnDataSource(hobo_df) #repeat with ColumnDataSource to get hovertips
from bokeh.core.properties import value

p.circle(x='time',y='Top', source = source, alpha=0.4, color='black',legend=value("Top"))
p.circle(x='time',y='TopMid', source = source, alpha=0.4, color='red',legend=value("TopMid"))
p.circle(x='time',y='BotMid', source = source, alpha=0.4, color='green',legend=value("BotMid"))
p.circle(x='time',y='Bot', source = source, alpha=0.4, color='blue',legend=value("Bot"))

p.yaxis.axis_label = 'Temp (C)'
p.xaxis.axis_label = 'Time (sec)'

#p.add_layout(Title(text=text, align="center"), "below")

p.legend.location = "top_left"
p.legend.click_policy="hide" #'hide' or 'mute' (need to provide muted_color=something,muted_alpha=something)
p.legend.label_text_font_size = '8pt'
p.legend.padding = 0
p.legend.spacing = 0
    
output_file(title + '.html', title="interactive_legend.py example")
show(p) # open a browser 
