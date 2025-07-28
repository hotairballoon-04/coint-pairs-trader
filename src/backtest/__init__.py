from .engine import BacktestEngine, BacktestParams
from .metrics import _METRIC_FUNCS
import pandas as pd

__all__ = [
    'BacktestEngine',
    'BacktestParams',
    'compute_metrics',
]


def compute_metrics(df: pd.DataFrame,
                    symbol_a: str,
                    symbol_b: str,
                    start_capital: float = 100.0,
                    metrics_list: list[str] = None) -> dict[str, float]:
    """Return a dict of the requested metrics (all if None)."""
    selected = metrics_list or list(_METRIC_FUNCS.keys())
    out: dict[str, float] = {}
    for name in selected:
        if name not in _METRIC_FUNCS:
            raise ValueError(f"Unknown metric '{name}'. Available: {list(_METRIC_FUNCS)}")
        func = _METRIC_FUNCS[name]
        out[name] = func(df, symbol_a, symbol_b, start_capital)
    return out
