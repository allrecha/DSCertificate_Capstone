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

#TASK 1
dropdown_options = [{'label':'All Sites','value':'ALL'}]
# Append sites to options list
for site in list(set(spacex_df['Launch Site'])):
    dropdown_options.append({'label':site,'value':site})


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
                                html.Div([
                                dcc.Dropdown(
                                    id='site-dropdown',
                                    options= dropdown_options,
                                    value='ALL',
                                    placeholder='Select a Launch Site here',
                                    searchable = True
                                    )                                    
                                ]),

                                # TASK 2: Add a pie chart to show the total successful launches count for all sites
                                # If a specific launch site was selected, show the Success vs. Failed counts for the site
                                html.Div(dcc.Graph(id='success-pie-chart')),
                                html.Br(),

                                html.P("Payload range (Kg):"),
                                # TASK 3: Add a slider to select payload range
                                dcc.RangeSlider(id='payload-slider',
                                    min=0, max=10000, step=1000,
                                    value=[min_payload, max_payload]),

                                # TASK 4: Add a scatter chart to show the correlation between payload and launch success
                                html.Div(dcc.Graph(id='success-payload-scatter-chart')),
                                ])

# TASK 2:
# Add a callback function for `site-dropdown` as input, `success-pie-chart` as output

# Function decorator to specify function input and output
@app.callback(Output(component_id='success-pie-chart', component_property='figure'),
              Input(component_id='site-dropdown', component_property='value'))

def get_pie_chart(entered_site):
    filtered_df = spacex_df.groupby('Launch Site')['class'].value_counts().reset_index(name='counts')
    total_success = spacex_df[spacex_df["class"]==1]
    success_counts = total_success.groupby('Launch Site').size().reset_index(name='counts')
    
    if entered_site == 'ALL':
        fig = px.pie(success_counts, values='counts', 
        names='Launch Site', 
        title='Total Success Launches By Site')
        return fig
    else:
        location_df = filtered_df[filtered_df['Launch Site']==entered_site]

        fig = px.pie(location_df, values='counts', 
        names='class', 
        title= f'Total Success Launches By {entered_site}')
        return fig


# TASK 4:
# Add a callback function for `site-dropdown` and `payload-slider` as inputs, 
# `success-payload-scatter-chart` as output
@app.callback(Output(component_id='success-payload-scatter-chart', component_property='figure'),
              [Input(component_id='site-dropdown', component_property='value'),
              Input(component_id='payload-slider', component_property='value')])

def get_payload_chart(entered_site, payload):

    print(payload)
    
    filtered_df = spacex_df[spacex_df['Payload Mass (kg)']>=payload[0]]
    filtered_df = filtered_df[filtered_df['Payload Mass (kg)']<=payload[1]]
    

    if entered_site == 'ALL':
        fig = px.scatter(filtered_df, x=filtered_df['Payload Mass (kg)'],
        y = filtered_df['class'], color = filtered_df['Booster Version Category'], 
        title='Correlation between Payload and Success for all Sites')
        return fig
    else:
        specific_df = filtered_df[filtered_df['Launch Site'] == entered_site]
        fig = px.scatter(specific_df, x=specific_df['Payload Mass (kg)'],
        y = specific_df['class'], color = specific_df['Booster Version Category'], 
        title=f'Correlation between Payload and Success for {entered_site}')
        return fig
        


# Run the app
if __name__ == '__main__':
    app.run_server()
