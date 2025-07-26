import numpy as np
import pandas as pd
from typing import Callable, Dict

TRADING_DAYS = 252


# strategy metrics
def sharpe_total(df: pd.DataFrame, *_: object) -> float:
    """Annualised Sharpe of *all* daily P&L."""
    ret = df['pnl']
    return (ret.mean() / ret.std()) * np.sqrt(TRADING_DAYS) if ret.std() != 0 else np.nan


def sharpe_invested(df: pd.DataFrame, *_: object) -> float:
    """Sharpe calculated only over days when a position was open (position.shift(1)!=0)."""
    daily_ret = df['cum_pnl'].diff().fillna(0)
    mask = df['position'].shift(1) != 0  # invested yesterday
    inv_ret = daily_ret[mask]
    return (inv_ret.mean() / inv_ret.std()) * np.sqrt(TRADING_DAYS) if inv_ret.std() != 0 else np.nan


def pct_time_in_market(df: pd.DataFrame, *_: object) -> float:
    """Percentage of days the strategy had a live position."""
    return 100 * (df['position'] != 0).mean()


def max_dd_strategy(df: pd.DataFrame, *_: object) -> float:
    """Maximum draw‑down of strategy equity curve."""
    dd = df['cum_pnl'] - df['cum_pnl'].cummax()
    return dd.min()


def total_return_pct(df: pd.DataFrame, _a: str, _b: str, *_: object) -> float:
    """Total return of the strategy in percent."""
    invested = (df['pos_a'].abs() * df[_a] + df['pos_b'].abs() * df[_b])
    max_invested = invested.max()
    if max_invested == 0:
        return np.nan
    return 100 * df['cum_pnl'].iloc[-1] / max_invested


# 50-50 benchmark
def returns_5050(df: pd.DataFrame, sym_a: str, sym_b: str) -> pd.Series:
    ret_a = df[sym_a].pct_change()
    ret_b = df[sym_b].pct_change()
    return 0.5 * (ret_a + ret_b)


def total_return_5050(df: pd.DataFrame, sym_a: str, sym_b: str, *_: object) -> float:
    ew_ret = returns_5050(df, sym_a, sym_b).dropna()
    return 100 * ((1 + ew_ret).prod() - 1)


def sharpe_5050(df: pd.DataFrame, sym_a: str, sym_b: str, *_: object) -> float:
    ew_ret = returns_5050(df, sym_a, sym_b).dropna()
    return (ew_ret.mean() / ew_ret.std()) * np.sqrt(TRADING_DAYS) if ew_ret.std() != 0 else np.nan


def max_dd_5050(df: pd.DataFrame, sym_a: str, sym_b: str, *_: object) -> float:
    ew_ret = returns_5050(df, sym_a, sym_b).dropna()
    cum = (1 + ew_ret).cumprod() - 1
    dd = cum - cum.cummax()
    return dd.min()


_METRIC_FUNCS: Dict[str, Callable[..., float]] = {
    'sharpe_total':        sharpe_total,
    'sharpe_invested':     sharpe_invested,
    'pct_time_in_market':  pct_time_in_market,
    'max_dd_strategy':     max_dd_strategy,
    'total_return_pct':    total_return_pct,
    'total_return_50_50':  total_return_5050,
    'sharpe_50_50':        sharpe_5050,
    'max_dd_50_50':        max_dd_5050,
}
