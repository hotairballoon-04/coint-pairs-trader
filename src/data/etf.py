import yfinance as yf
import pandas as pd

def _fetch(ticker, start, end, interval="1d", auto_adjust=True):
    df = yf.download(ticker, start=start, end=end,
                     interval=interval, auto_adjust=auto_adjust,
                     progress=False)
    series = df["Close"].copy()
    series.name = ticker
    return series

def fetch_etf_pair(sym_a, sym_b, start, end, interval):
    a = _fetch(ticker=sym_a, start=start, end=end, interval=interval)
    b = _fetch(ticker=sym_b, start=start, end=end, interval=interval)
    return pd.concat([a, b], axis=1).dropna()