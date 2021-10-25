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
from datetime import timedelta
from math import *
from stock import get_candle_data
from choices import stock_choices, crypto_choices
from style import colors

# API KEY: c5qb1iaad3iaqkuej8v0

def get_price(df, price_type, time):
	return (df.loc[(df['time'] == time) & (df['type'] == price_type)].iloc[0]['price'])

def switch_stock_abbrev(key):
    if key == 'c':
        return "close"
    elif key == "o":
        return "open"
    elif key == "h":
        return "high"
    elif key == "l":
        return "low"

# TODO: Replace with actual resolution
def generate_fig(
	ticker="AAPL",
	day_start=datetime.datetime(2020, 10, 23, 0, 0), 
	day_end=datetime.datetime(2021, 10, 23, 0, 0),
	resolution='D',
	pred_formula = "2 * get_price(df, 'close', t-time_resolution) - get_price(df, 'close', t-2*time_resolution)"
	):
	
	# TODO: Replace with actual values
	day_start = day_start.strftime('%s')
	day_end = day_end.strftime('%s')

	print("DEBUG: Formula: ", pred_formula)
	candle_data = get_candle_data(ticker, resolution, day_start, day_end)
	df = pd.DataFrame.from_dict(candle_data)
	data = []

	times = candle_data['t']

	for key, values in candle_data.items():
	    if key == 'c' or key == 'o' or key == 'h' or key == 'l':
	        for v, t in zip(values, times):
	            data.append([v, t, switch_stock_abbrev(key)])

	df = pd.DataFrame(data, columns = ["price", "time", "type"])

	df['time'] = pd.to_datetime(df['time'], unit='s')


	### Predicting future stock prices ###


	# Formula for prediction
	parsed = parser.expr(pred_formula)
	code = parsed.compile()


	# Compute the predictions based on formula
	pred = []
	for t in df['time']:
	    t += timedelta(days=1)
	    time_data = df.loc[df['time'] == t]
	    if resolution == 'D':
	        time_resolution = timedelta(days=1)
	        try:
	            pred.append([t, eval(code)])
	        except:
	            pred.append([t, None])
	pred_df = pd.DataFrame(pred, columns = ["time", "price"])


	### Plot everything ###


	# Plot the scatter graph of the prices
	fig = px.scatter(df, x="time", y="price", hover_name="type", color = "type", size_max=60)

	# Plot the scatter graph of the predictions
	fig.add_scatter(x=pred_df["time"], y=pred_df["price"], mode="markers", name="prediction")


	fig.update_layout(
	    plot_bgcolor=colors['background'],
	    paper_bgcolor=colors['background'],
	    font_color=colors['text']
	)
	return fig

