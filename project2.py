
import pandas as pd
import numpy as np
import dash
from dash.dependencies import Input, Output
import dash_core_components as dcc
import dash_html_components as html


external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

url = 'https://raw.githubusercontent.com/AlainKuiete/DATA608ASSINGMENTS/master/Global_Mobility_Report.csv'

mobility = pd.read_csv(url)

mobility.columns = ['country_code', 'country_region', 'region1', 'region2', 'date', 
              'recreation', 'grocery', 'parks', 'transit', 'workplaces', 'residentials']

mobile = mobility.copy()
cr_code = mobile['country_code'].unique()
country_region = mobile['country_region'].dropna().unique()
mobile['region1'].fillna("NA", inplace=True)
sub_region1 = mobile['region1'].dropna().unique()
mobile['region2'].fillna("NA", inplace=True)
sub_region2 = mobile['region2'].dropna().unique()

'''places = {'recreation': 'retail_and_recreation_percent_change_from_baseline',
            'grocery': 'grocery_and_pharmacy_percent_change_from_baseline',
            'parks': 'parks_percent_change_from_baseline',
            'transit': 'transit_stations_percent_change_from_baseline',
            'workplaces': 'workplaces_percent_change_from_baseline',
            'residentials': 'residential_percent_change_from_baseline'
            }
'''
places = ['recreation', 'grocery', 'parks', 'transit', 'workplaces', 'residentials']
# Boostrap CSS.
app.layout = html.Div(
    html.Div([
        html.Div(
            [
                html.H1(children='Community Mobility Report',
                        className='nine columns'),
                html.Img(
                    src="https://icons8.com/icon/CGf5JvobsqEu/coronavirus",
                    className='three columns',
                    style={
                        'height': '9%',
                        'width': '9%',
                        'float': 'right',
                        'position': 'relative',
                        'padding-top': 0,
                        'padding-right': 0
                    },
                ),
                html.Div(children='''
                        Each Community Mobility Report dataset is presented by location and highlights the percent change in
visits to places like grocery stores and parks within a geographic area.

                        ''',
                        className='nine columns'
                )
            ], className="row"
        ),

        html.Div(
            [
                html.Div(
                    [
                        html.P('Choose Country:'),
                        dcc.Dropdown(
                                id = 'CountryRegion',
                                options = [{'label': i, 'value': i} for i in country_region],
                                value='United States'
                        ),
                    ],style={'margin-top': '10', 'width': '24%', 'display': 'inline-block'}, className = "three columns",
                    
                ),
                html.Div(
                    [
                        html.P('Choose Region:'),
                        
                        dcc.Dropdown(
                                id='SubRegion1',
                                options= [{'label': i, 'value': i} for i in sub_region1],
                                value='New York'
                            ),  
                        
                    ],style={'margin-top': '10', 'width': '24%', 'display': 'inline-block'}, className = "three columns",
                ),

                html.Div(
                    [
                        html.P('Choose Region:'),
                        dcc.Dropdown(
                                id = 'SubRegion2',
                                options= [{'label': k, 'value': k} for k in sub_region2],
                                value='Bronx County',
                            ),
                    ],style={'width': '24%', 'display': 'inline-block'}, className = "three columns",
                ),
                    
            ], className="row"
        ),


        html.Div([
            html.P('Choose Paces:'),
                        dcc.Checklist(
                                id = 'Places',
                                options=[
                                    {'label': l, 'value': l } for l in places
                                ],     
                            ),
            ], style={'margin-top': '10'}, className = 'row'
        ),

        html.Div(
            [
            html.Div([
                    dcc.Graph(
                        id='retail-graph'
                    )
                ], className= 'six columns'
                ),

                html.Div([
                    dcc.Graph(
                        id='grocery-graph'
                    )
                ], className= 'six columns'
                )
            ], className="row"
        )
    ], className='ten columns offset-by-one')
)

@app.callback(
    Output('SubRegion1', 'options'),
    [Input('CountryRegion', 'value')])
def set_region1_options(selected_country):
    mobile['region1'].fillna("NA", inplace=True)
    return [{'label': i, 'value': i} for i in mobile[mobile["country_region"]==selected_country]['region1'].dropna().unique()]

@app.callback(
    Output('SubRegion1', 'value'),
    [Input('SubRegion1', 'options')])
def set_region1_value(available_options):
    return available_options[0]['value']

@app.callback(
    Output('SubRegion2', 'options'),
    [Input('SubRegion1', 'value')])
def set_region2_options(selected_region):
    mobile['region1'].fillna("NA", inplace=True)
    return [{'label': i, 'value': i} for i in mobile[mobile["region1"]==selected_region]['region2'].dropna().unique()]

@app.callback(
    Output('SubRegion2', 'value'),
    [Input('SubRegion2', 'options')])
def set_region2_value(available_options):
    return available_options[0]['value']


@app.callback(
    Output('retail-graph', 'figure'),
    [Input('SubRegion1', 'value'),
    Input('Places', 'value'),
    ])
def update_graph(region, place):

    
    cmobility = mobility[mobility["region2"] == region]
    cmobility.reset_index(inplace=True)
    cmobility.set_index('date', inplace=True)
    y = cmobility[place]
    data = [
    {'x': cmobility.index, 'y': y, 'type': 'line', 'name': 'Global_Mobility_Report'

    },
    ]

    figure = {
        'data': data,
        'layout': {
            'title': 'Mobility Trend',
            'xaxis' : dict(
                title='x Axis',
                titlefont=dict(
                family='Courier New, monospace',
                size=20,
                color='#7f7f7f'
            )),
            'yaxis' : dict(
                title='y Axis',
                titlefont=dict(
                family='Helvetica, monospace',
                size=20,
                color='#7f7f7f'
            ))
        }
    }
    return figure    

if __name__ == '__main__':
    app.run_server(debug=True)
