# Power Consumption Dashboard

import pandas as pd
pd.set_option('display.max_columns', 10)
from bokeh.plotting import figure, ColumnDataSource
from bokeh.layouts import column, row 
from bokeh.palettes import Bokeh3
from bokeh.models import CheckboxGroup, Slider, Div
from bokeh.io import curdoc

# Load and preprocess Tetouan City power consumption dataset
df = pd.read_csv('https://archive.ics.uci.edu/ml/machine-learning-databases/00616/Tetuan%20City%20power%20consumption.csv')

# Simplify column names for ease of use
df.rename(columns={ 'Zone 1 Power Consumption': 'Zone1', 
                    'Zone 2  Power Consumption': 'Zone2', 
                    'Zone 3  Power Consumption': 'Zone3'}, 
          inplace=True)

# Convert 'DateTime' column to datetime format
df.DateTime = pd.to_datetime(df.DateTime)                    

# Aggregate data to daily averages
dfd = df.groupby(pd.Grouper(key='DateTime', freq='1D')).mean().reset_index()

# Extract month from datetime for filtering
dfd['Month'] = dfd.DateTime.dt.month


# Define the title of the Bokeh dashboard
title = Div(text='<h1">Power Consumption Dashboard</h1>')

# Define interactive tools for the Bokeh dashboard
tools_to_show = 'box_select, lasso_select, save, reset, help'

# Set initial data source for Bokeh plots to January
source = ColumnDataSource(dfd[dfd.Month==1])

# Create temperature vs. power consumption plot
f_temp = figure(title='Temperature', x_axis_label='Temperature', y_axis_label='Power Consumption',
                toolbar_location='above', tools=tools_to_show)

# Plot each zone's data with distinct colors from Bokeh3 palette
t1 = f_temp.scatter('Temperature', 'Zone1', source=source, marker='circle_dot', 
                       size=10, color=Bokeh3[0], alpha=0.7)
t2 = f_temp.scatter('Temperature', 'Zone2', source=source, marker='circle_dot', 
                       size=10, color=Bokeh3[1], alpha=0.7)              
t3 = f_temp.scatter('Temperature', 'Zone3', source=source, marker='circle_dot', 
                       size=10, color=Bokeh3[2], alpha=0.7) 

# Create humidity vs. power consumption plot
f_hum = figure(title='Humidity', x_axis_label='Humidity', y_axis_label='Power Consumption',
               toolbar_location='above', tools=tools_to_show)  

# Repeat plotting for humidity data
h1 = f_hum.scatter('Humidity', 'Zone1', source=source, marker='circle_dot', 
                      size=10, color=Bokeh3[0], alpha=0.7)
h2 = f_hum.scatter('Humidity', 'Zone2', source=source, marker='circle_dot', 
                      size=10, color=Bokeh3[1], alpha=0.7)              
h3 = f_hum.scatter('Humidity', 'Zone3', source=source, marker='circle_dot', 
                      size=10, color=Bokeh3[2], alpha=0.7)   

# Create wind speed vs. power consumption plot
f_wind = figure(title='Wind Speed', x_axis_label='Wind Speed', y_axis_label='Power Consumption',
                toolbar_location='above', tools=tools_to_show) 

# Repeat plotting for wind speed
w1 = f_wind.scatter('Wind Speed', 'Zone1', source=source, marker='circle_dot', 
                       size=10, color=Bokeh3[0], alpha=0.7)
w2 = f_wind.scatter('Wind Speed', 'Zone2', source=source, marker='circle_dot', 
                       size=10, color=Bokeh3[1], alpha=0.7)              
w3 = f_wind.scatter('Wind Speed', 'Zone3', source=source, marker='circle_dot', 
                       size=10, color=Bokeh3[2], alpha=0.7)   

# Arrange plots horizontally
f = row(f_temp, f_hum, f_wind)

# Define the labels for the checkbox
labels = ['Zone 1','Zone 2','Zone 3']

# Create the checkbox
zone_selection = CheckboxGroup(labels=labels, active=[0,1,2])

# Updating plot visibility based on checkbox selections
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
    
# Link update_checkbox to CheckboxGroup selection changes
zone_selection.on_change('active', update_checkbox) 

# Slider for selecting month
slider_month = Slider(start=1, end=12, step=1, value=1, title='Month') 

# Function to update data based on selected month
def update_data(attr, old, new):
    '''
    Update data based on selected month
    '''
    source.data = dfd[dfd.Month == new]

# Link the update_data function to changes in the slider's value
slider_month.on_change('value', update_data)

# Add slider, checkbox group, and plots to the document
curdoc().add_root(column(title, slider_month, row(f, zone_selection))) 
