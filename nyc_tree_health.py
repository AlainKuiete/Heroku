import pandas as pd
import numpy as np
import dash
from dash.dependencies import Input, Output
import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objs as go


url = 'https://data.cityofnewyork.us/resource/nwxe-4ae8.json'
trees = pd.read_json(url)
trees.head(10)

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

nyc_borough = trees['boroname'].unique()
trees['spc_common'].fillna("NA", inplace=True)
species = trees['spc_common'].unique()

app.layout = html.Div([
    html.Div([
    	html.Div([html.H1("Health of New York City Trees ")], style={'textAlign': "center", 'padding': 10}),

        html.Div([
        	
            dcc.Dropdown(
                id='specie',
                options=[{'label': i, 'value': i} for i in species],
                value='red maple'
            ),  
        ],style={'width': '24%', 'display': 'inline-block'}),

        html.Div([
            dcc.RadioItems(
                id='borough',
                options=[{'label': i, 'value': i} for i in nyc_borough],
                value='Bronx',
                labelStyle={'display': 'inline-block'}
            ),
        ],style={'width': '24%', 'display': 'inline-block'}),


            
    ]),

    dcc.Graph(id='tree_health'),

])

@app.callback(
    Output('tree_health', 'figure'),
    [Input('borough', 'value'),
    Input('specie','value')
     ])
def update_graph(boroughs, tree_type):
    treesh = trees[trees["boroname"] == boroughs]
    treesh = treesh[treesh["spc_common"] == tree_type]
    trace = go.Histogram(x=treesh["health"], opacity=0.7, marker={"line": {"color": "#25232C", "width": 0.2}})

    layout = go.Layout(title=f"Trees Health Distribution", xaxis={"title": "Health Quality", "showgrid": False},
                       yaxis={"title": "Count", "showgrid": False} )
    figure = {"data": [trace], "layout": layout}

    return figure


if __name__ == '__main__':
    app.run_server(debug=True)




