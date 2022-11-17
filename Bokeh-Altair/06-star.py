# star.py

import numpy as np
from bokeh.layouts import column
from bokeh.models import Button
from bokeh.plotting import figure, curdoc

# create a plot and style its properties
p = figure(x_range=(0, 100), y_range=(0, 100), toolbar_location=None)
p.border_fill_color = 'black'
p.background_fill_color = 'black'
p.outline_line_color = None
p.grid.grid_line_color = None

cir = p.star(x=[], y=[], line_color='black', size=50, fill_color='gold') 

ds = cir.data_source

# Create a callback that changes the star coordinates
def callback():
    new_data = dict()    
    new_data['x'] = np.random.randint(10, 90, size=1)    
    new_data['y'] = np.random.randint(10, 90, size=1)    
    ds.data = new_data

# Add a button widget and link it with the callback function
button = Button(label="Show star!", button_type='primary')
button.on_event('button_click', callback)

# Put the button and plot in a layout and add to the document
curdoc().add_root(column(button, p))
