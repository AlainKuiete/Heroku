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


        html.Div([
            
            dcc.Dropdown(
                id='specie1',
                options=[{'label': i, 'value': i} for i in species],
                value='red maple'
            ),  
        ],style={'width': '24%', 'display': 'inline-block'}),

        html.Div([
            dcc.RadioItems(
                id='borough1',
                options=[{'label': i, 'value': i} for i in nyc_borough],
                value='Bronx',
                labelStyle={'display': 'inline-block'}
            ),
        ],style={'width': '24%', 'display': 'inline-block'}),


     ]),       
    
    html.Div([
        html.Div([
            dcc.Graph(id='tree_health'),
            ],style={'width': '48%', 'display': 'inline-block'}),

        html.Div([

            dcc.Graph(id='tree_health1'),
            ],style={'width': '48%', 'display': 'inline-block'}),
        
        
        ]),
    
    

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


@app.callback(
    Output('tree_health1', 'figure'),
    [Input("borough1", "value"), Input("specie1", "value")])
def update_scatter(borough, specie):
    treesh = trees[trees["boroname"] == borough]
    treesh = treesh[treesh["spc_common"] == specie]
    
    

    trees['steward'].fillna("NA", inplace=True)
    stwrd_name = trees['steward'].unique()
    trace = []
    for stwrd in stwrd_name:
        treesh = treesh[treesh['steward']== stwrd]
        trace.append(go.Histogram(x=treesh['health'], opacity=0.7, marker={"line": {"color": "#25232C", "width": 0.2}}))
    
    '''trace.append(go.Scatter(x.append(dff.count()), y.append(dff["health"].count()), mode="markers",
                                name=stwrd.title(),
                                marker={"size": 10}))
                        
    layout = go.Layout(title=f"Tree Health  vs Steward", colorway=['#fa9fb5', '#c51b8a'], hovermode='closest',
                       xaxis={"title": "Steward", "range": [-2, 75], "tick0": 0, "dtick": 5, "showgrid": False, },
                       yaxis={"title": "Tree health", "range": [-15, 300], "tick0": 0, "dtick": 25,
                        "showgrid": False, }, )'''
    

    layout = go.Layout(title=f"Trees Health Distribution", xaxis={"title": "Health Quality", "showgrid": False},
                       yaxis={"title": "Count", "showgrid": False} )


    figure1 = {"data": trace, "layout": layout}
    
    return figure1



if __name__ == '__main__':
    app.run_server(debug=True)
