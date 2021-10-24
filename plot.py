import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import compiler
import parser
from datetime import datetime, timedelta
from math import *
from stock import get_candle_data

# API KEY: c5qb1iaad3iaqkuej8v0

def get_price(df, price_type, time):
    return (df.loc[(df['time'] == time) & (df['type'] == price_type)].iloc[0]['price'])

resolution = 'D'
candle_data = get_candle_data('AAPL', resolution, 1590988249, 1591852249)
df = pd.DataFrame.from_dict(candle_data)
data = []

print(candle_data)

times = candle_data['t']

def switch_stock_abbrev(key):
    if key == 'c':
        return "close"
    elif key == "o":
        return "open"
    elif key == "h":
        return "high"
    elif key == "l":
        return "low"

for key, values in candle_data.items():
    print(values, times)
    if key == 'c' or key == 'o' or key == 'h' or key == 'l':
        for v, t in zip(values, times):
            data.append([v, t, switch_stock_abbrev(key)])

df = pd.DataFrame(data, columns = ["price", "time", "type"])

df['time'] = pd.to_datetime(df['time'], unit='s')


### Predicting future stock prices ###

# Formula for prediction
pred_formula = "2 * get_price(df, 'close', t-time_resolution) - get_price(df, 'close', t-2*time_resolution)"
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
print(pred_df)

### Plot everything ###

# Plot the scatter graph of the prices
fig = px.scatter(df, x="time", y="price", hover_name="type", color = "type", size_max=60)

# Plot the scatter graph of the predictions
fig.add_scatter(x=pred_df["time"], y=pred_df["price"], mode="markers", name="prediction")
fig.show()

