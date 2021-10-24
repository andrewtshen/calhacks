import finnhub

finnhub_client = finnhub.Client(api_key="c5qb1iaad3iaqkuej8v0")

def get_candle_data(symbol, resolution, unix_start, unix_end):
    return finnhub_client.stock_candles(symbol, resolution, unix_start, unix_end)


# print(finnhub_client.stock_candles('AAPL', 'D', 1590988249, 1591852249))

# print(get_candle_data('AAPL', 'D', 1590988249, 1591852249))

