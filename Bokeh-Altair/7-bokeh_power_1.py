# Power Consumption Dashboard

import numpy as np
import pandas as pd
pd.set_option('display.max_columns', 10)
from bokeh.plotting import figure, ColumnDataSource
from bokeh.layouts import column, row 
from bokeh.palettes import Bokeh3
from bokeh.models import Toggle, Slider
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
tools_to_show = 'box_select, lasso_select, save, reset, help'

source = ColumnDataSource(data=dfd[dfd.Month==1])

f_temp = figure(title='Temperature', x_axis_label='Temperature', y_axis_label='Power Consumption',
                toolbar_location='above', tools=tools_to_show, 
                #width=350, height=300
        )
t1 = f_temp.circle_dot('Temperature', 'Zone1', source=source, size=10, color=Bokeh3[0], alpha=0.7)
t2 = f_temp.circle_dot('Temperature', 'Zone2', source=source, size=10, color=Bokeh3[1], alpha=0.7)              
t3 = f_temp.circle_dot('Temperature', 'Zone3', source=source, size=10, color=Bokeh3[2], alpha=0.7) 

f_hum = figure(title='Humidity', x_axis_label='Humidity', y_axis_label='Power Consumption',
                toolbar_location='above', tools=tools_to_show, 
                #width=350, height=300
        )  
h1 = f_hum.circle_dot('Humidity', 'Zone1', source=source, size=10, color=Bokeh3[0], alpha=0.7)
h2 = f_hum.circle_dot('Humidity', 'Zone2', source=source, size=10, color=Bokeh3[1], alpha=0.7)              
h3 = f_hum.circle_dot('Humidity', 'Zone3', source=source, size=10, color=Bokeh3[2], alpha=0.7)   

f_wind = figure(title='Wind Speed', x_axis_label='Wind Speed', y_axis_label='Power Consumption',
                toolbar_location='above', tools=tools_to_show, 
                #width=350, height=300
        ) 
w1 = f_wind.circle_dot('Wind Speed', 'Zone1', source=source, size=10, color=Bokeh3[0], alpha=0.7)
w2 = f_wind.circle_dot('Wind Speed', 'Zone2', source=source, size=10, color=Bokeh3[1], alpha=0.7)              
w3 = f_wind.circle_dot('Wind Speed', 'Zone3', source=source, size=10, color=Bokeh3[2], alpha=0.7)   

f = row(f_temp, f_hum, f_wind)

toggle_z1 = Toggle(label='Zone 1', width=100, active=True)
toggle_z1.js_link('active', t1, 'visible')
toggle_z1.js_link('active', h1, 'visible')
toggle_z1.js_link('active', w1, 'visible')

toggle_z2 = Toggle(label='Zone 2', width=100, active=True)
toggle_z2.js_link('active', t2, 'visible')
toggle_z2.js_link('active', h2, 'visible')
toggle_z2.js_link('active', w2, 'visible')

toggle_z3 = Toggle(label='Zone 3', width=100, active=True)
toggle_z3.js_link('active', t3, 'visible')
toggle_z3.js_link('active', h3, 'visible')
toggle_z3.js_link('active', w3, 'visible')

slider_month = Slider(start=1, end=12, step=1, value=1, title='Month')

def update_data(attr, old, new):
    '''
    '''
    source.data = dfd[dfd.Month == new]

slider_month.on_change('value', update_data)

curdoc().add_root(column(row(toggle_z1, toggle_z2, toggle_z3, slider_month),f))