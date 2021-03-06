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

launch_sites = {"All Sites" : "ALL"}
lst = spacex_df["Launch Site"].unique()
for i,ls in enumerate(lst):
    launch_sites["site"+str(i+1)] = ls
# Create an app layout
app.layout = html.Div(children=[html.H1('SpaceX Launch Records Dashboard',
                                        style={'textAlign': 'center', 'color': '#503D36',
                                               'font-size': 40}),
                                # TASK 1: Add a dropdown list to enable Launch Site selection
                                # The default select value is for ALL sites
                                # dcc.Dropdown(id='site-dropdown',...)
                                dcc.Dropdown(id='site-dropdown',
                                options=[{'label' : key, 'value' : val} for key,val in launch_sites.items()],
                                value='ALL',
                                placeholder= "Select a Launch Site Here",
                                searchable=True
                                ),
                                html.Br(),

                                # TASK 2: Add a pie chart to show the total successful launches count for all sites
                                # If a specific launch site was selected, show the Success vs. Failed counts for the site
                                html.Div(dcc.Graph(id='success-pie-chart')),
                                html.Br(),

                                html.P("Payload range (Kg):"),
                                # TASK 3: Add a slider to select payload range
                                dcc.RangeSlider(id='payload-slider',
                                    min=0, max=10000, step=1000,
                                    marks={0: '0',
                                        1000: '1000',
                                        2000: '2000',
                                        3000: '3000',
                                        4000: '4000',
                                        5000: '5000',
                                        6000: '6000',
                                        7000: '7000',
                                        8000: '8000',
                                        9000: '9000',
                                        10000: '10000'},
                                    value=[min_payload, max_payload]),
                                # TASK 4: Add a scatter chart to show the correlation between payload and launch success
                                html.Div(dcc.Graph(id='success-payload-scatter-chart')),
                                ])

# TASK 2:
# Add a callback function for `site-dropdown` as input, `success-pie-chart` as output
@app.callback(Output(component_id='success-pie-chart', component_property='figure'),
              Input(component_id='site-dropdown', component_property='value'))
def get_piew_chart(entered_site):
    if entered_site == 'ALL':
        filtered_df = spacex_df
        fig = px.pie(filtered_df, values='class',names="Launch Site", title='Success Rate for all sites')
    else:
        filtered_df = spacex_df[spacex_df["Launch Site"]==entered_site].groupby(["Launch Site", "class"]).\
            size().reset_index(name="class count")
        
        fig = px.pie(filtered_df, values='class count',names="class", title='Success Rate for '+ entered_site)
    return fig
# TASK 4:
# Add a callback function for `site-dropdown` and `payload-slider` as inputs, `success-payload-scatter-chart` as output
@app.callback(Output(component_id='success-payload-scatter-chart', component_property='figure'),
    [Input(component_id='site-dropdown', component_property='value'), 
    Input(component_id="payload-slider", component_property="value")]
)
def get_scatter_plot(site, slider):
    low, high = slider
    mask = ((spacex_df["Payload Mass (kg)"] > low )& (spacex_df["Payload Mass (kg)"] <high))
    filtered_df = spacex_df[mask]
    if site == "ALL":
        fig = px.scatter(filtered_df, x="Payload Mass (kg)", y ="class",
         color = 'Booster Version Category',
         hover_data=['Booster Version'],
         title = 'Payload Vs Class For All Sites')
    else:
        filtered_df = filtered_df[spacex_df["Launch Site"]==site]
        fig = px.scatter(filtered_df, x="Payload Mass (kg)", y ="class",
         color = 'Booster Version Category',
         title = 'Payload Vs Class For ' + site)
    return fig

# Run the app
if __name__ == '__main__':
    app.run_server()
