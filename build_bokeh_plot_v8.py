# -*- coding: utf-8 -*-
"""
Created on Thu Sep 12 11:15:38 2019

@author: amiller
"""

#example
# import numpy as np
# import pandas as pd
# N = 50
# df = pd.DataFrame(np.random.randint(10,N,size=(N, 4)), columns=list('ABCD'))
# df['time'] = range(0,N)
# manual_points = [
#                 [[100,20], 'x_line','lower limit'], 
#                 [[20,0], 'y_line','test point'], 
#                 [[100,35], 'x_line','upper limit'],
#                 [[30,25], 'square','a point'],
#                 [[40,30], 'triangle','another point'],
#                 ]
# title_text = 'test plot'
# build_bokeh_plot(df, x_axis='time', force_all_hover=True, x_scale_type = 'datetime',y_scale_type='linear',
#                   x_label = 'Time', y_label='Temperature (C)', cols_to_drop = ['C'], title_text = title_text,
#                   xmin = 0, ymin=0, ymax=N, lines_points_both='lines', manual_points=manual_points)



def build_bokeh_plot(df,x_axis=None,cols_to_plot=None,cols_to_drop=None,xmin=None,xmax=None,ymin=None,ymax=None, 
                     legend='True',title_text = None,x_label = None, y_label = None,color_style = 'categorical', 
                     lines_points_both = 'lines', x_scale_type = None, force_all_hover = False, y_scale_type = None,
                     limit_lines = None, display_source_as_title = True, graph_x = 1400, graph_y = 700,
                     save_pickle = False, save_plot = False, save_loc = None, save_name = 'plot', manual_points = None):
#df can be a dataframe or a csv or Excel file location (full path)
#x_axis is the column to use for the x axis values (defaults to the dataframe index)
#cols_to_plot is a list of column names to be plotted
#cols_to_drop is a list of column names to not be plotted
#xmin, xmax, ymin, ymax are numeric values
#title_text, x_label,y_label are strings to put on the plot as a title
#color_style sets the coloring of plots, options are categorical (which selects by category) or anything else (which uses a spectrum) 
#lines_points_both options are lines, points or both
#x/y_scale_type options are linear, log or datetime (or mercator but probably you don't want that)
#x_scale_type selects x scale to be time by default
#force_all_hover enables all hover tools (even if only plotting selected columns).
#save_pickle saves a copy of the variables to your current working directory unless save_loc is given
#save_plot saves the .html plot file
#save_name gives a custom name to the saved plot
#manual_points provide a list of points to be added to the graph along with optional text ([[x,y],[kind],text(optional)]

    

#note: if hovertool wants to show human readable time, needs to have extra column with time string-formatted as desired (might be possible to do programmatically but a pain)
    
#    import ast
    from ast import literal_eval
    from bokeh.palettes import viridis, Category20, Category10
    from bokeh.plotting import show, figure, save, curdoc
    from bokeh.models import ColumnDataSource, Title, Range1d, Label, Scatter
    import os
    import pandas as pd
    import pickle

    curdoc().clear()
    bokeh_doc = curdoc()
#Check if source is a file
    if isinstance(df, str):
        title = df
        if (df[-4:] == '.csv'):
            df = pd.read_csv(df, delimiter=',',skiprows=0)  # doctest: +SKIP
        elif ((df[-4:] == '.xls') | (df[-5:] == '.xlsx')):
            df = pd.read_excel(df, skiprows=0)  # doctest: +SKIP
        else:
            print('Could not open file or dataframe')
            return
    else: #source is a dataframe
        title = ''
        if display_source_as_title is True:
            try:
                title = [x for x in globals() if globals()[x] is df][0] #this only works if this function is called after the DF is loaded I think
            except:
                title = title_text #'No title data found'
            pass
        
    df = df.copy(deep=True) #so this doesn't modify the original dataframe when the index column is added
    if cols_to_drop != None:
        df = df.drop(columns=cols_to_drop)

    if x_axis == None: #use the index to plot (probably a better way to do this with the index directly)
        x_axis = 'Index'
        df[x_axis] = df.index
        if x_scale_type == None:
            x_scale_type = 'linear' #assume the index is not a time
    
    if cols_to_plot == None:
        cols_to_plot=df.columns.values.tolist()
    
#drop the x axis column from the plotting list
    try:
        cols_to_plot.remove(x_axis)
    except:
        print('exception found in removing column')
        pass



#    #categorical mapping
#    Category20
#    
#    #spectrum mapping (lowercase for function ie magma(132))
#    Greys256
#    Inferno256
#    Magma256
#    Plasma256
#    Viridis256
#    Cividis256

    if color_style == 'categorical':
        if len(cols_to_plot) > 20:
            colors = viridis(len(cols_to_plot))
        else:
            if ((len(cols_to_plot) > 2) & (len(cols_to_plot) <=10)) :
                colors = Category10[len(cols_to_plot)]
            elif ((len(cols_to_plot) > 10) & (len(cols_to_plot) <=20)) :
                colors = Category20[len(cols_to_plot)]
            else:
                colors = viridis(len(cols_to_plot))
    else:
        colors  = color_style

    TOOLS="hover,crosshair,pan,wheel_zoom,zoom_in,zoom_out,box_zoom,undo,redo,reset,tap,save,box_select,poly_select,lasso_select,"

    cols_to_plot = list(cols_to_plot)
    
    if force_all_hover:
        tipnames = list(df.columns.values)
    else:
        tipnames = list(cols_to_plot)
        tipnames.append(x_axis) #always include the x_axis for reading when data happened

    tipexecute = ["(\"%s\",\"@{%s}\")," % (x,x) for x in tipnames]
    tipexecute = ''.join(tipexecute)
    tipexecute = '[' + tipexecute + ']' 
    
    TOOLTIPS = literal_eval(tipexecute)
    
    if ((xmax == None) | (xmin == None)):
        # xmin=df[x_axis].iloc[0]
        # xmax=df[x_axis].iloc[-1]
        xmin=df[x_axis].min()
        xmax=df[x_axis].max()


    if ((ymax == None) & (ymin == None) & (y_scale_type == None)): #if y limits not specified find the high and lows, then set to log scale if too big
        try:
            ymin = df[cols_to_plot].min()
            ymin = min([ x for x in ymin if type(x) in [int, float] ])
            ymax = df[cols_to_plot].max()
            ymax = max([ x for x in ymax if type(x) in [int, float] ])
            if ((ymin < -10000) | (ymax > 10000)):        #fix y range to prevent massive offscales by default
                print('Adjusted Y axis to log scale, specify ymin and ymax for custom linear values. Negative values omitted from log plot.')  
                y_scale_type='log'
            else:
                y_scale_type='linear'
        except Exception as e:
            print(str(e))
            print('could not find min and max for auto log y scale')
            pass

    if x_scale_type == None:
        x_scale_type = 'datetime' #assume datetime by default

    p = figure(title=title,tools=TOOLS,tooltips=TOOLTIPS,width=graph_x, height=graph_y,
               x_axis_type=x_scale_type, y_axis_type=y_scale_type, sizing_mode = 'stretch_both'
)

    if title_text != None:
        p.add_layout(Title(text=title_text, align="center"), "below")

    if limit_lines != None: #plot arbitrary line pairs (for limits thresholds etc)
        #limit_lines = [ [[X1,X2],[Y1,Y2]],[[X3,X4],[Y3,Y4]] ]
        for limit_line in limit_lines:
            p.line(x=limit_line[0],y=limit_line[1], alpha=0.4, color='black') 
    
    for idx,var in enumerate(cols_to_plot):
        source = ColumnDataSource(df.reset_index(drop=True))
        print(idx)
        print(var)
        if lines_points_both == 'points':
            p.circle(x=x_axis,y=var, source = source, alpha=0.4,color=colors[idx],legend_label=var)
        if lines_points_both == 'lines':
            p.line(x=x_axis,y=var, source = source, line_alpha=0.4, line_color=colors[idx], line_width=2, legend_label=var)
        if lines_points_both == 'both':
            p.circle(x=x_axis,y=var, source = source, alpha=0.4,color=colors[idx])
            p.line(x=x_axis,y=var, source = source, line_alpha=0.4, line_color=colors[idx], line_width=2, legend_label=var)


    #plot manual points
    if manual_points != None:
        #[[x,y],[style],text(optional)]

        x_limit_min = df[x_axis].min()
        x_limit_max = df[x_axis].max()
        y_limit_min = df.min(numeric_only=True).min() #this clips the x axis
        y_limit_max = df.max(numeric_only=True).max()
        
        for point in manual_points:
            if point[1] == 'x_line':
                #make line from x_min to x_max at y
                p.line([x_limit_min,x_limit_max],[point[0][1],point[0][1]])
                #add text at middle
                text = Label(x=(x_limit_min+x_limit_max)/8, y=point[0][1], text=point[2])
                 # render_mode='css',
                 # border_line_color='black', border_line_alpha=1.0,
                 # background_fill_color='white', background_fill_alpha=1.0)
                p.add_layout(text)

            elif point[1] == 'y_line':
                #make line from y_min to y_max at x
                p.line([point[0][0],point[0][0]],[y_limit_min,y_limit_max])
                text = Label(x=point[0][0], y=y_limit_min, text=point[2], angle= 90,  angle_units= "deg",)
                 # render_mode='css',
                 # border_line_color='black', border_line_alpha=1.0,
                 # background_fill_color='white', background_fill_alpha=1.0)
                p.add_layout(text)
            elif point[1] == 'text':
                #make text only at point
                text = Label(x=point[0][0], y=point[0][1], text=point[2])
                
                p.add_layout(text)

            else: #use bokeh built in glyphs
                source_annotations = ColumnDataSource(dict(x=[point[0][0]], y=[point[0][1]]))
                glyph = Scatter(x="x", y="y", size = 10, marker=point[1])
            #    glyph = Scatter(x=point[0][0], y=point[0][1], size = 5, marker=point[1])

                p.add_glyph(source_annotations, glyph)
                text = Label(x=point[0][0], y=point[0][1], text=point[2])
                p.add_layout(text)
# asterisk()
# circle()
# circle_cross()
# circle_dot()
# circle_x()
# circle_y()
# cross()
# dash()
# dot()
# diamond()
# diamond_cross()
# diamond_dot()
# hex()
# hex_dot()
# inverted_triangle()
# plus()
# square()
# square_cross()
# square_dot()
# square_pin()
# square_x()
# star()
# star_dot()
# triangle()
# triangle_dot()
# triangle_pin()
# x()
# y()




    p.x_range = Range1d(xmin, xmax)
    if x_label == None:
        p.xaxis.axis_label = x_axis
    else:
        p.xaxis.axis_label = x_label

    if ((ymax != None) & (ymin != None)):
        p.y_range = Range1d(ymin, ymax)
    if y_label != None:
        p.yaxis.axis_label = y_label


        
    if legend:
        if legend == 'right':
            p.legend.location = "top_right"
        else:
            p.legend.location = "top_left"

        p.legend.click_policy="hide" #'hide' or 'mute' (need to provide muted_color=something,muted_alpha=something)
        p.legend.label_text_font_size = '8pt'
        p.legend.label_height: 5
        p.legend.glyph_height: 5
        p.legend.label_standoff: 0

        p.legend.padding = 0
        p.legend.spacing = 0
    else:
        p.legend.visible=False
            
    if save_loc != None:
        dirpath = save_loc
    else:
        dirpath = os.getcwd()

    bokeh_doc.add_root(p)

    if save_pickle:
        with open(dirpath + '\\' + save_name + '.pickle', 'wb') as handle:
            pickle.dump(df, handle, protocol=pickle.HIGHEST_PROTOCOL)
    if save_plot:
        save(p, filename = dirpath + '\\' + save_name + '.html')
        print('Saved to ' + dirpath + '\\' + save_name + '.html')
    show(p) # open a browser 


# df = r'C:\Users\amiller\Desktop\python test\wagtech_without_calibration_8-7-19.csv'
# df = r'C:\Users\amiller\Desktop\python test\merged_fieldtest_tables_20190313.xlsx'
# df = r'C:\Users\amiller\Downloads\Alexa Fluor 568.csv'

# #df = str(input('Enter filename\n'))


# args = input('Enter args\n')
# if len(args)>0:
#     eval('build_bokeh_plot(r\''  +df+'\','+args+')')
# else:
#     eval('build_bokeh_plot(r\''+df+'\')')

# #build_bokeh_plot(df, y_scale_type = 'log', save_plot=True)
# #build_bokeh_plot(df, y_scale_type='log', x_scale_type = 'log')

# #C:\scaledata>pyinstaller -c -F build_bokeh_plot_v4.py
