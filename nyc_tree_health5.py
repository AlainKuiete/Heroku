import pandas as pd
import numpy as np
import dash
from dash.dependencies import Input, Output
import dash_core_components as dcc
import dash_html_components as html


boro = []
url = 'https://data.cityofnewyork.us/resource/nwxe-4ae8.json'
trees = pd.read_json(url)

boro.append('Bronx')
soql_url = ('https://data.cityofnewyork.us/resource/nwxe-4ae8.json?' +\
        '$select=spc_common,steward,health,count(tree_id)' +\
        '&$where=boroname=\'Bronx\''+\
        '&$group=spc_common,steward,health').replace(' ', '%20')
Bronx_trees = pd.read_json(soql_url)

boro.append('Manhattan')
soql_url = ('https://data.cityofnewyork.us/resource/nwxe-4ae8.json?' +\
        '$select=spc_common,steward,health,count(tree_id)' +\
        '&$where=boroname=\'Manhattan\''+\
        '&$group=spc_common,steward,health').replace(' ', '%20')
Manhattan_trees = pd.read_json(soql_url)

boro.append('Brooklyn')
soql_url = ('https://data.cityofnewyork.us/resource/nwxe-4ae8.json?' +\
        '$select=spc_common,steward,health,count(tree_id)' +\
        '&$where=boroname=\'Brooklyn\''+\
        '&$group=spc_common,steward,health').replace(' ', '%20')
Brooklyn_trees = pd.read_json(soql_url)


boro.append('Queens')
soql_url = ('https://data.cityofnewyork.us/resource/nwxe-4ae8.json?' +\
        '$select=spc_common,steward,health,count(tree_id)' +\
        '&$where=boroname=\'Queens\''+\
        '&$group=spc_common,steward,health').replace(' ', '%20')
Queens_trees = pd.read_json(soql_url)

boro.append('Staten Island')
soql_url = ('https://data.cityofnewyork.us/resource/nwxe-4ae8.json?' +\
        '$select=spc_common,steward,health,count(tree_id)' +\
        '&$where=boroname=\'Staten Island\''+\
        '&$group=spc_common,steward,health').replace(' ', '%20')
StatenIsland_trees = pd.read_json(soql_url)



trees_health = {'Bronx':Bronx_trees, 'Manhattan':Manhattan_trees, 'Brooklyn':Brooklyn_trees, 'Queens':Queens_trees, 'Staten Island':StatenIsland_trees}

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

nyc_borough = trees['boroname'].unique()
trees['spc_common'].fillna("NA", inplace=True)
species = trees['spc_common'].unique()
trees['health'].fillna("NA", inplace=True)
qualities = trees['health'].unique()

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

        html.Div([
            dcc.RadioItems(
                id='quality',
                options=[{'label': i, 'value': i} for i in qualities],
                value='Good',
                labelStyle={'display': 'inline-block'}
            ),

            dcc.RadioItems(
                id='yaxis-type',
                options=[{'label': i, 'value': i} for i in ['Linear', 'Log']],
                value='Linear',
                labelStyle={'display': 'inline-block'}
                ),
        ],style={'width': '24%', 'display': 'inline-block'}),

            
    ]),

    dcc.Graph(id='tree_health'),

])


@app.callback(
    Output('tree_health', 'figure'),
    [Input('borough', 'value'),
    Input('specie','value'),
    Input('quality','value'),
    Input('yaxis-type','value'),
     ])
def update_graph(boroughs, tree_type, quality,yaxis_type):
    treesh = trees[trees["boroname"] == boroughs]
    treesh = treesh[treesh["spc_common"] == tree_type]
    
     treesh = trees_health[boroughs]
    
    traces = []
    for i in qualities:
        treesh = treesh[treesh['health']==quality]
        trees_by_health = treesh[treesh['health'] == i]
        traces.append(dict(
            x = trees_by_health.index,
            y = trees_by_health['count_tree_id'],
            mode='markers',
            opacity=0.7,
            marker={
                'size': 15,
                'line': {'width': 0.5, 'color': 'white'}
            },
            name=i
            ))

    layout = dict(
            xaxis={
                'title': species,
                'type': 'linear' 
            },
            yaxis={
                'title': 'Count',
                'type': 'linear' if yaxis_type == 'Linear' else 'log'
            },
            margin={'l': 40, 'b': 40, 't': 10, 'r': 0},
            hovermode='closest',
            transition = {'duration': 500},)
    figure = {"data": traces, "layout": layout}
    return figure


if __name__ == '__main__':
    app.run_server(debug=True)


   