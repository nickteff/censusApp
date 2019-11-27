from plotly.graph_objs._figure import Figure

from backend import api
from flask import render_template, jsonify, request
import pandas as pd
from plotly.graph_objs import *

accesstoken = 'pk.eyJ1IjoicGluZXlkYXRhIiwiYSI6ImNqb2t3NWN6ZDAycGkzcXAzODc2cml2bm8ifQ.aGKqMqIIKcLto1Lw9Ek89A'

df = pd.read_csv('compute/static/census.csv')
df.loc[:, "MSA_CODE"] = df.loc[:, "MSA_CODE"].astype('int')
tbl = pd.read_csv('compute/static/states.csv')

measure_options = {
    'income': [
        "Income Level",
        [
            'lowIncome',
            "middleIncome",
            "highIncome",
        ]
    ],
    'generation': [
        "Generation",
        [
            'silent',
            "boomer",
            "genX",
            'millenial',
            'genZ'
        ]
    ],
    'education': [
        "Education",
        [
            'EDUC_GRAD_DEG',
            'EDUC_BACH_DEG',
            'COLLEGE_NO_BACH',
            'HS_DIP',
            'NO_HS_DIP'
        ]
    ]
}


@api.route('/api/states')
def states():
    states = tbl.itertuples()
    states2 = tbl.itertuples()
    states = {
        'options': [
            {'label': state.State, 'value': state.StateCode}
            for state in states
        ],
    }

    return jsonify(states)


@api.route('/api/states/<state>')
def states_geo(state):
    layout = {"layout": {
        'autosize': True,
        'hovermode': 'closest',
        'mapbox': {
            'bearing': 0,
            'center': {
                'lat': 37,
                'lon': -95
            },
            'pitch': 0,
            'zoom': int(15),
            'style': 'streets'
        },
    }}
    return jsonify(layout)


@api.route('/api/map/<state>/<urban>')
def map_state_view(state, urban):
    if urban == "both":
        urban = ['urban', 'rural']
    else:
        urban = [urban]

    if state == 'USA':
        return jsonify(maply(df[df.Urban.isin(urban)], state).to_plotly_json())
    else:
        return jsonify(
            maply(
                df[
                    (df.STATECODE == state) &
                    (df.Urban.isin(urban))
                    ],
                state
            ).to_plotly_json())


@api.route('/api/bar/<state>/<urban>/<measure>')
def bar_state_view(state, urban, measure):
    if urban == "both":
        urban = ['urban', 'rural']
    else:
        urban = [urban]

    if state == 'USA':
        return jsonify(barmap(df[df.Urban.isin(urban)], measure).to_plotly_json())
    else:
        return jsonify(
            barmap(
                df[
                    (df.STATECODE == state) & (df.Urban.isin(urban))
                    ],
                measure
            ).to_plotly_json())


def maply(df, state=None):
    if state != None:
        lat = tbl.loc[tbl.StateCode == state, 'Lat'].values[0]
        lon = tbl.loc[tbl.StateCode == state, 'Lon'].values[0]
        zoom = float(tbl.loc[tbl.StateCode == state, 'Zoom'].values[0])
    else:
        lat = 38
        lon = -96
        zoom = 3.5
    data = [{
        'type': 'scattermapbox',
        'lat': list(df.LAT),
        'lon': list(df.LON),
        'mode': 'markers',
        'marker': {
            'size': 6
        },
        'text': ["{}, {}".format(city.CITY, city.STATECODE) for city in df.loc[:, ["CITY", "STATECODE"]].itertuples()],
    }]

    layout = {
        'autosize': True,
        'hovermode': 'closest',
        'mapbox': {
            'accesstoken': accesstoken,
            'bearing': 0,
            'center': {
                'lat': lat,
                'lon': lon
            },
            "pitch": 0,
            'zoom': zoom,
            'style': 'streets'
        },
        'margin': {
            'l': 1,
            'r': 1,
            'b': 1,
            't': 1,
            'pad': 4
        },
    }

    fig = Figure(data=data, layout=layout)

    return fig


def barmap(df, measure):
    data = [{
        'type': 'bar',
        'x': measure_options[measure][1],
        'y': list(df[measure_options[measure][1]].mean().values)
    }]

    layout = {
        'autosize': True,
        'margin': {
            'l': 1,
            'r': 1,
            'b': 30,
            't': 45,
            'pad': 0
        },
        'plot_bgcolor': '#ECECEC',
        'paper_bgcolor': '#ECECEC',
        'title': '<b>{}</b>'.format(measure_options[measure][0])
    }

    return Figure(data=data, layout=layout)

