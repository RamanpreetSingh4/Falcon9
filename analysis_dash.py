# Import required libraries
import pandas as pd
import dash
import dash_html_components as html
import dash_core_components as dcc
from dash.dependencies import Input, Output
import plotly.express as px

# Read the airline data into pandas dataframe
spacex_df = pd.read_csv("spacex_launch_dash.csv")
max_payload = spacex_df['Payload Mass (kg)'].max()
min_payload = spacex_df['Payload Mass (kg)'].min()



# Create a dash application
app = dash.Dash(__name__)

# Create an app layout
app.layout = html.Div(children=[html.H1('SpaceX Launch Records Dashboard',
                                        style={'textAlign': 'center', 'color': '#503D36',
                                               'font-size': 40}),
                                # TASK 1: Add a dropdown list to enable Launch Site selection
                                # The default select value is for ALL sites
                                # dcc.Dropdown(id='site-dropdown',...)
                                html.Br(),

                                dcc.Dropdown(
                                    id = 'id',
                                    options = [
                                        {'label': 'All Sites', 'value':'All Sites'},
                                        *[{'label': i, 'value': i}for i in spacex_df['Launch Site'].unique()]
                                    ],
                                    value='All Sites',
                                    placeholder='All Sites',
                                    searchable=True
                                ),


                                # TASK 2: Add a pie chart to show the total successful launches count for all sites
                                # If a specific launch site was selected, show the Success vs. Failed counts for the site
                                html.Div(dcc.Graph(id='success-pie-chart')),
                                html.Br(),

                                html.P("Payload range (Kg):"),
                                # TASK 3: Add a slider to select payload range
                                #dcc.RangeSlider(id='payload-slider',...)
                                dcc.Slider(
                                    id='payload_slider',
                                    min=0,
                                    max=10000,
                                    step=1000,
                                    value=[1000],
                                ),
                                

                                # TASK 4: Add a scatter chart to show the correlation between payload and launch success
                                html.Div(dcc.Graph(id='success-payload-scatter-chart')),
                                ])

# TASK 2:
# Add a callback function for `site-dropdown` as input, `success-pie-chart` as output
@app.callback(
    Output(component_id='success-pie-chart', component_property='figure'),
    Input(component_id='id', component_property='value')
)

def update_pie_chart(site):
    if site == 'All Sites':
        fig = px.pie(spacex_df, values='class', names='Launch Site', title='Total Success Launches By Site')
        return fig
    else:
        filtered_df = spacex_df[spacex_df['Launch Site'] == site]
        fig = px.pie(filtered_df, names='class', title='Total Success Launches for Site')
        return fig
    

# TASK 4:
# Add a callback function for `site-dropdown` and `payload-slider` as inputs, `success-payload-scatter-chart` as output
@app.callback(
    Output(component_id='success-payload-scatter-chart', component_property='figure'),
    Input(component_id='id', component_property='value'),
    Input(component_id='payload_slider', component_property='value')
    
)

def update_scatter_chart(site, payload):
    
    mask = spacex_df['Payload Mass (kg)'] < payload
    if site == 'All Sites':
        fig = px.scatter(spacex_df[mask], x='Payload Mass (kg)', y='class', color='Booster Version Category', title='Correlation between Payload and Success for All Sites')
        return fig
    else:
        filtered_df = spacex_df[spacex_df['Launch Site'] == site]
        fig = px.scatter(filtered_df[mask], x='Payload Mass (kg)', y='class', color='Booster Version Category', title='Correlation between Payload and Success for Site')
        return fig

# Run the app
if __name__ == '__main__':
    app.run_server()
