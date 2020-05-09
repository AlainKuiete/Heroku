
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

cr_code = mobility['country_region_code'].unique()
country_region = mobility['country_region'].dropna().unique()
mobility['sub_region_1'].fillna("NA", inplace=True)
sub_region1 = mobility['sub_region_1'].unique()
mobility['sub_region_2'].fillna("NA", inplace=True)
sub_region2 = mobility['sub_region_2'].unique()

places = {'Recreation': 'retail_and_recreation_percent_change_from_baseline',
            'Grocery': 'grocery_and_pharmacy_percent_change_from_baseline',
            'Parks': 'parks_percent_change_from_baseline',
            'Transit': 'transit_stations_percent_change_from_baseline',
            'Workplaces': 'workplaces_percent_change_from_baseline',
            'Residentials': 'residential_percent_change_from_baseline'
            }

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
                                options=[
                                    {'label': i, 'value': i} for i in country_region],
                                value='United States'
                        ),
                    ],style={'margin-top': '10', 'width': '24%', 'display': 'inline-block'}, className = "three columns",
                    
                ),
                html.Div(
                    [
                        html.P('Choose Region:'),
            
                        dcc.Dropdown(
                                id='SubRegion1',
                                options=[{'label': i, 'value': i} for i in sub_region1],
                                value='New York'
                            ),  
                        
                    ],style={'margin-top': '10', 'width': '24%', 'display': 'inline-block'}, className = "three columns",
                ),

                html.Div(
                    [
                        html.P('Choose Region:'),
                        dcc.Dropdown(
                                id = 'SubRegion2',
                                options=[{'label': k, 'value': k} for k in sub_region2],
                                value='New York',
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
                                    {'label': l, 'value': places[l]} for l in places.keys()
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
    Output('retail-graph', 'figure'),
    [Input('CountryRegion', 'value'),
    Input('SubRegion1', 'value'),
    Input('SubRegion2', 'value'),
    Input('Places', 'value'),
    ])
def update_graph(country, sregion1, sregion2, place):
    cmobility = mobility[mobility["country_region"] == country]
    cmobility = cmobility[cmobility["sub_region_1"] == sregion1]
    cmobility = cmobility[cmobility["sub_region_2"] == sregion2]

    data = []

    for key in places.keys():
        data.append(dict(
            x=cmobility[cmobility[places[key]]==place]['date'],
            y=cmobility[cmobility[places[key]]==place][places[key]]))

    figure = {
        'data': data,
        'layout': {
            'title': 'Graph 1',
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
