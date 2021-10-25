import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import compiler
import parser
import dash
from dash import dcc
from dash import html
import plotly.express as px
import pandas as pd
import time
import datetime
from datetime import timedelta, date
from math import *
from dash.dependencies import Input, Output

# Custom Scripts
from stock import get_candle_data
from choices import stock_choices, crypto_choices
from fig import generate_fig
from style import colors

app = dash.Dash(__name__)


### App Information ###

fig = generate_fig()

app.layout = html.Div(style={'backgroundColor': colors['background']}, children=[
    html.H1(
        children='Stonks',
        style={
            'textAlign': 'center',
            'color': colors['text']
        }
    ),

    html.H5(
        children='Desmos for Stonks: A better way to lose money.',
        style={
            'textAlign': 'center',
            'color': colors['text'],
        }
    ),

    dcc.Graph(
        id='stonks',
        figure=fig
    ),

    html.Div(children=[
        html.Label('Ticker'),
        dcc.Dropdown(
            id='ticker_dropdown',
            options=stock_choices,
            placeholder="Select a ticker",
            value='AAPL',
            clearable=False,
            style={
                'font': "Courier New",
                'color': colors['text']
            }
        ),
    ], style={'padding': 20, 'flex': 1}),


    html.Div(children=[        
        html.Label('Date Range'),
        html.Br(),
        dcc.DatePickerRange(
            id='start_end_day_picker',
            initial_visible_month=date.today().strftime("%Y-%m-%d"),
            end_date=date.today().strftime("%Y-%m-%d")
        )
    ], style={'padding': 20, 'flex': 1}),

    html.Div(children=[
        html.Label('Input Formula'),
        html.Br(),
        dcc.Input(
            id="input_formula",
            type="text",
            placeholder="Input prediction formula",
        )
    ], style={'padding': 20, 'flex': 1})
])

# Update the ticker
@app.callback(
    Output('stonks', 'figure'),
    Input('ticker_dropdown', 'value'),
    Input('start_end_day_picker', 'start_date'),
    Input('start_end_day_picker', 'end_date'),
    Input('input_formula', 'value'))
def update_graph(ticker_dropdown, start_date, end_date, input_formula):
    print("UPDATE GRAPH:", input_formula, start_date, end_date, type(end_date))
    if start_date and end_date:
        start_year, start_month, start_day = start_date.split("-")
        end_year, end_month, end_day = end_date.split("-")
        print(start_year, start_month, start_day)
        print(end_year, end_month, end_day)

        # TODO: replace day_start with start_date and same with end
        fig = generate_fig(
            day_start=datetime.datetime(int(start_year), int(start_month), int(start_day), 0, 0),
            day_end=datetime.datetime(int(end_year), int(end_month), int(end_day), 0, 0)
        )
    elif ticker_dropdown:
        print("Ticker: ", ticker_dropdown)
        fig = generate_fig(ticker=ticker_dropdown)
    elif input_formula:
        print("Input Formula", input_formula)
        fig = generate_fig(pred_formula=input_formula)
    else:
        print("Errored!")
    return fig

if __name__ == '__main__':
    app.run_server(debug=True)