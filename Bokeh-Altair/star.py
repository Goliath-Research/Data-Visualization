# star.py

import numpy as np
from bokeh.layouts import column
from bokeh.models import Button
from bokeh.plotting import figure, curdoc

# Set up Bokeh figure with x, y ranges, no toolbar
p = figure(x_range=(0, 100), y_range=(0, 100), 
           toolbar_location=None)
# Set the plot background and border to black
p.border_fill_color = 'black'
p.background_fill_color = 'black'
# Remove gridlines and outline
p.outline_line_color = None
p.grid.grid_line_color = None

# Add an initially invisible star glyph to the plot
cir = p.star(x=[], y=[], line_color='black', 
             size=50, fill_color='gold') 

# Data source for updating the star glyph
ds = cir.data_source

# Callback to randomly reposition the star
def callback():
    new_data = dict()    
    new_data['x'] = np.random.randint(10, 90, size=1)    
    new_data['y'] = np.random.randint(10, 90, size=1)    
    ds.data = new_data

# Create a button to move star on click
button = Button(label="Show star!", button_type='primary')
button.on_event('button_click', callback)

# Display button and plot in Bokeh app
curdoc().add_root(column(button, p))
