from .etf import fetch_etf_pair
from .crypto import fetch_crypto_pair
import pandas as pd


def get_pair_prices(symbols: list[str], type: str = "etf", start_date: str = "2018-01-01", end_date: str = None, interval: str = "1d") -> pd.DataFrame:
    """
    Get pair prices for two assets (symbols).
    symbols :           list[str]   e.g. ['BTC/USDT', 'ETH/USDT'] or ['EEM','VWO']
    :param type:        "etf" of "crypto"
    :param start_date:  ISO date
    :param end_date:    ISO date (default is today)
    :param interval:    time interval of data, default is "1d"
    :return:            pd.DataFrame with two columns of prices indexed by date
    """

    if len(symbols) != 2:
        raise ValueError("Exactly two symbols required")

    if type == "etf":
        return fetch_etf_pair(symbols[0], symbols[1], start_date, end_date, interval)
    elif type == "crypto":
        #raise NotImplementedError("Crypto pair prices fetching is not implemented yet.")
        return fetch_crypto_pair(symbols[0], symbols[1], start_date, end_date, interval)
    else:
        raise ValueError(f"Unsupported type {type}. Use 'etf' or 'crypto'.")