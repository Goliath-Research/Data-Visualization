# Power Consumption Dashboard

import pandas as pd
pd.set_option('display.max_columns', 10)
from bokeh.plotting import figure, ColumnDataSource
from bokeh.layouts import column, row 
from bokeh.palettes import Bokeh3
from bokeh.models import CheckboxGroup, Slider, Div
from bokeh.io import curdoc

# Power Consumption of Tetouan City dataset
df = pd.read_csv('https://archive.ics.uci.edu/ml/machine-learning-databases/00616/Tetuan%20City%20power%20consumption.csv')

# Renaming some columns
df.rename(columns={ 'Zone 1 Power Consumption': 'Zone1', 
                    'Zone 2  Power Consumption': 'Zone2', 
                    'Zone 3  Power Consumption': 'Zone3'}, 
                    inplace=True)

df.DateTime = pd.to_datetime(df.DateTime)                    

# Getting one value per day
dfd = df.groupby(pd.Grouper(key='DateTime', freq='1D')).mean().reset_index()

# Creating the Month variable
dfd['Month'] = dfd.DateTime.dt.month

# Creating the Bokeh Dashboard

title = Div(text='<h1">Power Consumption Dashboard</h1>')

tools_to_show = 'box_select, lasso_select, save, reset, help'

source = ColumnDataSource(dfd[dfd.Month==1])

f_temp = figure(title='Temperature', x_axis_label='Temperature', y_axis_label='Power Consumption',
                toolbar_location='above', tools=tools_to_show)
t1 = f_temp.circle_dot('Temperature', 'Zone1', source=source, size=10, color=Bokeh3[0], alpha=0.7)
t2 = f_temp.circle_dot('Temperature', 'Zone2', source=source, size=10, color=Bokeh3[1], alpha=0.7)              
t3 = f_temp.circle_dot('Temperature', 'Zone3', source=source, size=10, color=Bokeh3[2], alpha=0.7) 

f_hum = figure(title='Humidity', x_axis_label='Humidity', y_axis_label='Power Consumption',
                toolbar_location='above', tools=tools_to_show)  
h1 = f_hum.circle_dot('Humidity', 'Zone1', source=source, size=10, color=Bokeh3[0], alpha=0.7)
h2 = f_hum.circle_dot('Humidity', 'Zone2', source=source, size=10, color=Bokeh3[1], alpha=0.7)              
h3 = f_hum.circle_dot('Humidity', 'Zone3', source=source, size=10, color=Bokeh3[2], alpha=0.7)   

f_wind = figure(title='Wind Speed', x_axis_label='Wind Speed', y_axis_label='Power Consumption',
                toolbar_location='above', tools=tools_to_show) 
w1 = f_wind.circle_dot('Wind Speed', 'Zone1', source=source, size=10, color=Bokeh3[0], alpha=0.7)
w2 = f_wind.circle_dot('Wind Speed', 'Zone2', source=source, size=10, color=Bokeh3[1], alpha=0.7)              
w3 = f_wind.circle_dot('Wind Speed', 'Zone3', source=source, size=10, color=Bokeh3[2], alpha=0.7)   

f = row(f_temp, f_hum, f_wind)

labels = ['Zone 1','Zone 2','Zone 3']

#Create the checkbox
zone_selection = CheckboxGroup(labels=labels, active=[0,1,2])

def update_checkbox(attr, old, new):
    # Getting active checkbox values
    active_checkbox = zone_selection.active
    # Setting all graphs to False
    t1.visible = False
    t2.visible = False
    t3.visible = False
    h1.visible = False
    h2.visible = False
    h3.visible = False
    w1.visible = False
    w2.visible = False
    w3.visible = False
    # Zone 1
    if 0 in active_checkbox:
        t1.visible = True
        h1.visible = True
        w1.visible = True
    # Zone 2
    if 1 in active_checkbox:
        t2.visible = True
        h2.visible = True
        w2.visible = True
    # Zone 3
    if 2 in active_checkbox:
        t3.visible = True
        h3.visible = True
        w3.visible = True
    
zone_selection.on_change('active', update_checkbox) 

slider_month = Slider(start=1, end=12, step=1, value=1, title='Month') 

def update_data(attr, old, new):
    '''
    '''
    source.data = dfd[dfd.Month == new]

slider_month.on_change('value', update_data)

curdoc().add_root(column(title, slider_month, row(f, zone_selection))) 