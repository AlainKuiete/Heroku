
import pandas as pd
import numpy as np
import dash
from dash.dependencies import Input, Output
import dash_core_components as dcc
import dash_html_components as html
import plotly
import plotly.graph_objs as go


external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

server = app.server

url = 'https://raw.githubusercontent.com/AlainKuiete/DATA608ASSINGMENTS/master/Global_Mobility_Report.csv'
mobility = pd.read_csv(url, low_memory=False)
mobility.columns = ['code', 'country', 'region1', 'region2', 'date', 'recreation', 'grocery', 'parks', 'transit', 'workplaces', 'residentials' ]

code = mobility['code'].unique()
country = mobility['country'].dropna().unique()
mobility['region1'].fillna("NA", inplace=True)
sub_region1 = mobility['region1'].unique()
mobility['region2'].fillna("NA", inplace=True)
sub_region2 = mobility['region2'].unique()

places = ['recreation', 'grocery', 'parks', 'transit', 'workplaces', 'residentials']

local_text = {'recreation': 'Mobility trends for places like restaurants, cafes, shopping centers, theme parks, museums, libraries, and movie theaters.',
 'grocery': 'Mobility trends for places like grocery markets, food warehouses, farmers markets, specialty food shops, drug stores, and pharmacies.',
  'parks': 'Mobility trends for places like national parks, public beaches, marinas, dog parks, plazas, and public gardens.',
   'transit': 'Mobility trends for places like public transport hubs such as subway, bus, and train stations.',
    'workplaces': 'Mobility trends for places of work.',
     'residentials': 'Mobility trends for places of residence.'}


# Boostrap CSS.
app.layout = html.Div(
    html.Div([
        html.Div(
            [
                html.H2(children='Covid-19 Community Mobility Reports',
                        className='nine columns'),
                html.Img(
                    src="https://img.icons8.com/bubbles/50/000000/coronavirus.png",
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
                html.H4(children='''
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
                        html.H6('Choose Country:'),
                        dcc.Dropdown(
                                id = 'CountryRegion',
                                options=[
                                    {'label': i, 'value': i} for i in country],
                                value='United States'
                        ),
                    ],style={'margin-top': '10', 'width': '24%', 'display': 'inline-block'}, className = "three columns",
                    
                ),
                html.Div(
                    [
                        html.H6('Choose Region:'),
            
                        dcc.Dropdown(
                                id='SubRegion1',
                                options=[{'label': i, 'value': i} for i in sub_region1],
                                value='New York'
                            ),  
                        
                    ],style={'margin-top': '10', 'width': '24%', 'display': 'inline-block'}, className = "three columns",
                ),

                html.Div(
                    [
                        html.H6('Choose Region:'),
                        dcc.Dropdown(
                                id = 'SubRegion2',
                                options=[{'label': k, 'value': k} for k in sub_region2],
                                value='Bronx County',
                            ),
                    ],style={'width': '24%', 'display': 'inline-block'}, className = "three columns",
                ),
                    
            ], className="row"
        ),

        html.Div([
            html.Div([
                html.H6('Choose Location:'),
                dcc.RadioItems(
                                id = 'Places',
                                options=[{'label': l, 'value': l} for l in places],
                                value='recreation', 
                            ),
                ], style={'margin-top': '10', 'width': '24%', 'display': 'inline-block'}, className = "three columns",
                ),
            html.Div([
                html.H6('Summary Statistics'),
                dcc.Textarea(
                            id='Stats',
                            value = 'Mobility Report Statistics',
                            style={'width': '50%',}
                            ),
                ], style={'width': '50%', 'display': 'inline-block'}, className = "four columns",
                 )
            ], style={'margin-top': '10'}, className = 'row',
            ),

        html.Div(
            [
            html.Div([
                    dcc.Graph(
                        id='retail-graph'
                    )
                ], className= 'ten columns'
                ),

                html.Div([
                    dcc.Markdown(
                        id='Text',
                        children = '''**This text will be bold**'''
                    )
                ], className= 'two columns'
                )
            ], className="row"
        )
    ], className='ten columns offset-by-one')
)

@app.callback(
    Output('SubRegion1', 'options'),
    [Input('CountryRegion', 'value')])
def set_region1_options(selected_country):
    mobility['region1'].fillna("NA", inplace=True)
    return [{'label': i, 'value': i} for i in mobility[mobility["country"]==selected_country]['region1'].unique()]

@app.callback(
    Output('SubRegion1', 'value'),
    [Input('SubRegion1', 'options')])
def set_region1_value(available_options):
    return available_options[0]['value']

@app.callback(
    Output('SubRegion2', 'options'),
    [Input('SubRegion1', 'value')])
def set_region2_options(selected_region):
    mobility['region1'].fillna("NA", inplace=True)
    return [{'label': i, 'value': i} for i in mobility[mobility["region1"]==selected_region]['region2'].unique()]

# Region to choose



@app.callback(
    [Output('retail-graph', 'figure'),
    Output('Stats', 'value')],
    [Input('SubRegion2', 'value'),
    Input('SubRegion1', 'value'),
    Input('CountryRegion', 'value'),
    Input('Places', 'value'),
    ])


def update_value(sregion2, sregion1, scountry, location):
    url = 'https://raw.githubusercontent.com/AlainKuiete/DATA608ASSINGMENTS/master/Global_Mobility_Report.csv'
    df = pd.read_csv(url)

    df.columns = ['code', 'country', 'region1', 'region2', 'date', 'recreation', 'grocery', 'parks', 'transit', 'workplaces', 'residentials' ]
    df.reset_index(inplace=True)
    df.set_index("date", inplace=True)
    x = df.index
    if sregion2 != 'NA':
        y = df[df['region2']==sregion2][location]
    elif sregion2 != 'NA' and sregion2 == 'NA':
        y = df[df['region1']==sregion1][location]
    else:
        y = df[df['country']==scountry][location]

    stat = '{}'.format(y.describe())

    data = plotly.graph_objs.Scatter(
            x=x,
            y=y,
            name=location,
            mode= 'lines+markers',
            fill="tozeroy",
            fillcolor="#6897bb",
            )
    figure = {'data': [data],'layout' : go.Layout(title = '{}'.format(location), xaxis=dict(title='baseline'))}

    #figure = {'data': [data],'layout' : go.Layout(xaxis=dict(range=[min(x),max(x)]),
    #                                            yaxis=dict(range=[min(y),max(y)]),)}
    return figure, stat

@app.callback(
    Output('Text', 'children'),
    [Input('Places', 'value')])    
def update_text(place):
    return local_text[place]


if __name__ == '__main__':
    app.run_server(debug=True)
