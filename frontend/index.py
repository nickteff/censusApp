import dash
import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
import requests
from dash.dependencies import Output, Input

from backend import server

app = dash.Dash(
    __name__,
    server=server,
    external_stylesheets=[dbc.themes.SUPERHERO],
    url_base_pathname='/')

map_data = requests.get('http://0.0.0.0:9999/api/map/USA/both').json()

app.layout = dbc.Container(
    [
        dbc.Row(html.H1('Hello')),
        dbc.Row(
            dbc.Col(
                dcc.Dropdown(
                    id="rural-id",
                    options=[
                        {'label': rural[0], 'value': rural[1]}
                        for rural in [["Rural", 'rural'],
                                      ["Urban", 'urban'],
                                      ["Both", "both"]]
                    ],
                    value="both"

                ),
                md=9,
                style={'color': 'black'}
            )
        ),
        dbc.Row(
            [
                dbc.Col(
                    dcc.Graph(
                        id='map-id',
                        figure={
                            'data': map_data['data'],
                            'layout': map_data['layout']
                        }
                    ),
                    md=9),
                dbc.Col(
                    [html.P('world')],
                    style={
                        'background': 'purple'
                    },
                    md=3)
            ]
        )
    ], fluid=True
)


@app.callback(
    Output(component_id='map-id', component_property='figure'),
    [Input(component_id='rural-id', component_property='value')]
)
def map_graph(input_value):
    r = requests.get('http://0.0.0.0:9999/api/map/USA/{}'.format(input_value)).json()
    return {'data': r['data'], 'layout': r['layout']}
