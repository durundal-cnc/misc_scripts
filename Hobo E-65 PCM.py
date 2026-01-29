# -*- coding: utf-8 -*-
"""
Created on Tue Jan  5 14:06:29 2021

@author: AndrewMiller
"""

def build_bokeh_plot(df,x_axis=None,cols_to_plot=None,cols_to_drop=None,xmin=None,xmax=None,ymin=None,ymax=None, 
                     legend=True,title_text = None,x_label = None, y_label = None,color_style = 'categorical', 
                     lines_points_both = 'lines', x_scale_type = None, force_all_hover = False, y_scale_type = None,
                     limit_lines = None,
                     save_pickle = False, save_plot = False, save_loc = None, save_name = 'plot'):
#df can be a dataframe or a csv or Excel file location (full path)

import pandas as pd
import sys
sys.path.append(r'C:\Users\AndrewMiller\OneDrive - Global Health Labs\Documents\Python Scripts')
from build_bokeh_plot_v6 import build_bokeh_plot



#PCM Freeze data from hobo
hobo_df = pd.read_csv(r'C:\Users\AndrewMiller\OneDrive - Global Health Labs\Documents\E-65_PCM_hobo_freeze_and_thaw_10659154.csv', delimiter=',',skiprows=0,header=1)  # doctest: +SKIP
hobo_df['time'] = pd.to_datetime(hobo_df.iloc[:,1], format='%m/%d/%y %I:%M:%S %p')
hobo_df['hours'] = [((x-hobo_df['time'].iloc[0]).total_seconds() / 3600.0 ) -75.5 for x in hobo_df['time']]

build_bokeh_plot(hobo_df, x_axis='hours', force_all_hover=True, cols_to_plot=['T-Type, °C (LGR S/N: 10659154, SEN S/N: 10659154, LBL: 1)'],
                 xmin = 0, xmax = 80, ymin = -80, ymax = 25, x_scale_type = 'linear',y_scale_type='linear',
                 x_label = 'Hours', y_label='Temperature (C)', title_text = 'E-65 PCM Freeze Time', display_source_as_title = False,
                 save_plot = True, save_loc = r'C:\Users\AndrewMiller\OneDrive - Global Health Labs\Alban vaccine application\Testing\Test report\Test data', save_name = 'E-65 PCM Freeze Time')

#E-65 hold time (first attempt)
df = pd.read_csv(r'C:\temp\pcm.csv')
df['time'] = pd.to_datetime(df['Time'], format='%m/%d/%Y %I:%M:%S %p')
df['hours'] = [((x-df['time'].iloc[0]).total_seconds() / 3600.0 )-1.094 for x in df['time']]
build_bokeh_plot(df, x_axis='hours', force_all_hover=True, y_scale_type='linear', ymin=-65, ymax=-50, cols_to_drop=['Time', 'time'],
                 x_label = 'Hours', y_label='Temperature (C)', title_text = 'E-65 PCM Hold Time', 
                 display_source_as_title = False, xmin = 1.094, x_scale_type = 'linear', xmax = 120,
                 save_plot = True, save_loc = r'C:\Users\AndrewMiller\OneDrive - Global Health Labs\Alban vaccine application\Testing\Test report\Test data', save_name = 'E-65 PCM Hold Time')

#5 and 10L 43C dry ice
df = pd.read_csv(r'C:\temp\Arktek 5 and 10L DI vertical 43C.csv')
df['time'] = pd.to_datetime(df['Time'], format='%m/%d/%Y %I:%M:%S %p')
df['hours'] = [((x-df['time'].iloc[0]).total_seconds() / 3600.0 ) for x in df['time']]
build_bokeh_plot(df, x_axis='hours', force_all_hover=True, y_scale_type='linear', ymin=-80, ymax=-50, cols_to_drop=['Time', 'time', 'Big chamber Temp PV', 'Big chamber Humidity PV'],
                 x_label = 'Hours', y_label='Temperature (C)', title_text = 'Arktek 5 and 10L DI vertical 43Chold time', 
                 display_source_as_title = False, xmin = 0, x_scale_type = 'linear',
                 save_plot = True, save_loc = r'C:\Users\AndrewMiller\OneDrive - Global Health Labs\Alban vaccine application\Testing\Test report\Test data', save_name = 'Arktek 5 and 10L DI vertical 43Chold time')

#5L 25C dry ice side
df = pd.read_csv(r'C:\temp\Arktek 5L DI vertical 25C.csv')
df['time'] = pd.to_datetime(df['Time'], format='%m/%d/%Y %I:%M:%S %p')
df['hours'] = [((x-df['time'].iloc[0]).total_seconds() / 3600.0 ) for x in df['time']]
build_bokeh_plot(df, x_axis='hours', force_all_hover=True, y_scale_type='linear', ymin=-80, ymax=-50, cols_to_drop=['Time', 'time', 'Big chamber Temp PV', 'Big chamber Humidity PV'],
                 x_label = 'Hours', y_label='Temperature (C)', title_text = 'Arktek 5L DI vertical 25C', 
                 display_source_as_title = False, xmin = 0, x_scale_type = 'linear', xmax = 330,
                 save_plot = True, save_loc = r'C:\Users\AndrewMiller\OneDrive - Global Health Labs\Alban vaccine application\Testing\Test report\Test data', save_name = 'Arktek 5L DI vertical 25C')

#5L 25C dry ice bottom
df = pd.read_csv(r'C:\temp\Arktek 5L DI bottom 25C.csv')
df['time'] = pd.to_datetime(df['Time'], format='%m/%d/%Y %I:%M:%S %p')
df['hours'] = [((x-df['time'].iloc[0]).total_seconds() / 3600.0 ) for x in df['time']]
build_bokeh_plot(df, x_axis='hours', force_all_hover=True, y_scale_type='linear', ymin=-80, ymax=-50, cols_to_drop=['Time', 'time', 'Big chamber Temp PV', 'Big chamber Humidity PV', 'Mod5TC2'],
                 x_label = 'Hours', y_label='Temperature (C)', title_text = 'Arktek 5L DI bottom 25C', 
                 display_source_as_title = False, xmin = 0, x_scale_type = 'linear', xmax = 280,
                 save_plot = True, save_loc = r'C:\Users\AndrewMiller\OneDrive - Global Health Labs\Alban vaccine application\Testing\Test report\Test data', save_name = 'Arktek 5L DI bottom 25C')

#COW tests
df = pd.read_csv(r'C:\temp\dewar heat leak COW tests.csv')
df['time'] = pd.to_datetime(df['Time'], format='%m/%d/%Y %I:%M:%S %p')
df['string time'] =df['Time']
df['hours'] = [((x-df['time'].iloc[0]).total_seconds() / 3600.0 ) for x in df['time']]
build_bokeh_plot(df, x_axis='time', force_all_hover=True, y_scale_type='linear', ymin=0, ymax=10, cols_to_drop=['hours', 'string time'],cols_to_plot=['A24', 'A421', 'A420'],
                 x_label = 'Date', y_label='Temperature (C)', title_text = 'COW tests', 
                 display_source_as_title = False,  x_scale_type = 'datetime',
                 save_plot = True, save_loc = r'C:\Users\AndrewMiller\OneDrive - Global Health Labs\Alban vaccine application\Testing\Test report\Test data', save_name = 'Arktek COW tests')

#PCM 43-25 pre-chilled
df = pd.read_csv(r'C:\temp\PCM 43-25 prechilled.csv')
df['time'] = pd.to_datetime(df['Time'], format='%m/%d/%Y %I:%M:%S %p')
df['string time'] =df['Time']
df['hours'] = [((x-df['time'].iloc[0]).total_seconds() / 3600.0 ) for x in df['time']]
build_bokeh_plot(df, x_axis='time', force_all_hover=True, y_scale_type='linear', ymin=-75, ymax=-55, cols_to_drop=['hours', 'string time'],
                 x_label = 'Date', y_label='Temperature (C)', title_text = 'PCM 43-25 prechilled', 
                 display_source_as_title = False,  x_scale_type = 'datetime',
                 save_plot = True, save_loc = r'C:\Users\AndrewMiller\OneDrive - Global Health Labs\Alban vaccine application\Testing\Test report\Test data', save_name = 'PCM 43-25 prechilled')


#PCM 43 not pre-chilled
df = pd.read_csv(r'C:\temp\PCM 43C no prechill.csv')
df['time'] = pd.to_datetime(df['Time'], format='%m/%d/%Y %I:%M:%S %p')
df['string time'] =df['Time']
df['hours'] = [((x-df['time'].iloc[0]).total_seconds() / 3600.0 -.75) for x in df['time']]
build_bokeh_plot(df, x_axis='hours', force_all_hover=True, y_scale_type='linear', ymin=-70, ymax=-55, cols_to_drop=['time', 'Time', 'Big chamber Temp PV', 'string time'],
                 x_label = 'Hours', y_label='Temperature (C)', title_text = 'PCM 43C no prechill', xmax = 80, xmin=0,
                 display_source_as_title = False,  x_scale_type = 'linear',
                 save_plot = True, save_loc = r'C:\Users\AndrewMiller\OneDrive - Global Health Labs\Alban vaccine application\Testing\Test report\Test data', save_name = 'PCM 43C no prechill')
#5L vaccine doublesided Arktek dry ice in aluminum containers 43C
df = pd.read_csv(r'C:\temp\Arktek 5L aluminum doubleside part combined.csv')
df['time'] = pd.to_datetime(df['Time'], format='%m/%d/%Y %I:%M:%S %p')
df['string time'] =df['Time']
df['hours'] = [((x-df['time'].iloc[0]).total_seconds() / 3600.0) for x in df['time']]
build_bokeh_plot(df, x_axis='hours', force_all_hover=True, y_scale_type='linear', ymin=-80, ymax=-55, cols_to_drop=['time', 'Time', 'Big chamber Temp PV', 'string time'],
                 x_label = 'Hours', y_label='Temperature (C)', title_text = '5L vaccine doublesided Arktek dry ice in aluminum containers 43C', xmin=0, xmax=315,
                 display_source_as_title = False,  x_scale_type = 'linear',
                 save_plot = True, save_loc = r'C:\Users\AndrewMiller\OneDrive - Global Health Labs\Alban vaccine application\Testing\Test report\Test data', save_name = 'Arktek 5L aluminum doubleside part combined')

