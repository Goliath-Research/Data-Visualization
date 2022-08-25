# Power consumption in Tetouan, 2017

# Import libraries
import pandas as pd
import plotly.express as px
from dash import Dash, html, dcc, Input, Output


# 1. Getting and exploring the data

# Load the dataset
df=pd.read_csv('https://archive.ics.uci.edu/ml/machine-learning-databases/00616/Tetuan%20City%20power%20consumption.csv')

# Changing DateTime column to datetime
df.DateTime = pd.to_datetime(df.DateTime)

# Renaming some columns
df.rename(columns={'Zone 1 Power Consumption': 'Zone1', 'Zone 2  Power Consumption': 'Zone2', 
                   'Zone 3  Power Consumption': 'Zone3'}, inplace=True)

# Adding a column with Month
df['Month'] = df.DateTime.dt.month

# Getting one value per day
dfd = df.groupby(pd.Grouper(key='DateTime', freq='1D')).mean().reset_index()


# 2. Building the layout 

# Create the Dash app
app = Dash()

# Creating the layout
app.layout = html.Div([
    # title
    html.Div(html.H1('Power consumption in Tetouan, 2017'), 
            style={'text-align': 'center', 'color':'grey'}),
    # checklist        
    dcc.Checklist(id='zone-check',
        options={
            'Zone1': ' Zone 1    ',
            'Zone2': ' Zone 2    ',
            'Zone3': ' Zone 3    ',                
        }, 
        value=['Zone1', 'Zone2', 'Zone3'],
        style={'width':'20%', 'display':'inline-block', 'horizontal-align':'right'}    
    ), # end of checklist
    # slider
    html.Div([
        dcc.Slider(1, 12, 1, value=1,
            id='month-slider',
            marks={
                1: 'Jan', 
                2: 'Feb', 
                3: 'Mar', 
                4: 'Apr', 
                5: 'May', 
                6: 'Jun', 
                7: 'Jul', 
                8: 'Aug', 
                9: 'Sep', 
                10: 'Oct', 
                11: 'Nov', 
                12: 'Dec'
            },
            included=False,
            tooltip={"placement": "top", "always_visible": True},
        ), # end of slider
    ], style={'width': '67%', 'display': 'inline-block'}),    
    # horizontal line
    html.Hr(),
    # graphs
    dcc.Graph(id='fig-s1', style={'width': '28%', 'display': 'inline-block'}),
    dcc.Graph(id='fig-s2', style={'width': '28%', 'display': 'inline-block'}),
    dcc.Graph(id='fig-s3', style={'width': '28%', 'display': 'inline-block'}),    
])


# 3. Adding interactivity with callback functions

# Set up the callback function
@app.callback(
    Output('fig-s1',  'figure'),
    Output('fig-s2',  'figure'),
    Output('fig-s3',  'figure'),
    Input ('month-slider', 'value'),
    Input ('zone-check',   'value'),
)

def update_graphs(sel_month, sel_zones):
    # filtering the dataframe
    dfd_sel = dfd[dfd['Month'] == sel_month]

    # getting the zones to plot    
    zones = [z for z in ['Zone1','Zone2','Zone3'] if z in sel_zones]
    
    # Temperature vs Power Consumption
    fig_s1 = px.scatter(dfd_sel, x='Temperature', y=zones,
                hover_data={'Temperature':':.2f', 'value':':.2f'},
                title='<b> Temperature vs Power Consumption </b>'
                )
    
    # Humidity vs Power Consumption
    fig_s2 = px.scatter(dfd_sel, x='Humidity', y=zones,
                hover_data={'Humidity':':.2f', 'value':':.2f'},
                title='<b> Humidity vs Power Consumption </b>'
                )
    
    # Wind Speed vs Power Consumption
    fig_s3 = px.scatter(dfd_sel, x='Wind Speed', y=zones,
                hover_data={'Wind Speed':':.2f', 'value':':.2f'},
                title='<b> Wind Speed vs Power Consumption </b>'
                )    
        
    return fig_s1, fig_s2, fig_s3


# 4. Running the dashboard

# Run local server
if __name__ == '__main__':
    app.run_server(debug=True)
