import ccxt
import pandas as pd
import warnings


def _fetch(symbol: str, exchange:str = "binance", since: int = None, limit: int = 1000, timeframe:str = "1d"):
    ex = getattr(ccxt, exchange)()
    bars = ex.fetch_ohlcv(symbol, timeframe=timeframe,since= since, limit=limit)
    df = pd.DataFrame(bars, columns=["ts","o","h","l","c","v"])
    df["dt"] = pd.to_datetime(df.ts, unit="ms")
    return df.set_index("dt")["c"].rename(symbol)


def fetch_crypto_pair(sym_a: str, sym_b: str, start: str, end: str, interval: str):
    ts_start = pd.Timestamp(start, tz="UTC")
    since = int(ts_start.timestamp() * 1000)

    if end is None:
        ts_end = pd.Timestamp.now(tz="UTC")
    else:
        ts_end = pd.Timestamp(end, tz="UTC")
    n_days = (ts_end.normalize() - ts_start.normalize()).days + 1
    limit = n_days

    if limit > 1000:
        warnings.warn(
            message="Crypto data can only be fetched up to 1000 time points at a time."
            f"You requested {limit} points. Requesting the maximum of 1000 points.\n"
            "Reduce data range or increase the interval.",
            category=UserWarning,
            stacklevel=2
        )

    a = _fetch(symbol=sym_a, since=since, limit=limit, timeframe=interval)
    b = _fetch(symbol=sym_b, since=since, limit=limit, timeframe=interval)

    return pd.concat([a, b], axis=1).dropna()
