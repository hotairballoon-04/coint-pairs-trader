# engine.py
import pandas as pd
import numpy as np
from dataclasses import dataclass


@dataclass
class BacktestParams:
    stop_loss: float = 0.05


class BacktestEngine:
    def __init__(self, data: pd.DataFrame,
                 params: BacktestParams = BacktestParams()):
        self.data = data
        self.params = params
        self.sym_a, self.sym_b = self.data.columns

    @staticmethod
    def get_position_sizes(price_a: float, price_b: float, beta_val):
        size_a = 1.0
        beta_val = 1.0 if beta_val is None else beta_val
        size_b = (price_a / price_b) * beta_val * size_a
        return size_a, size_b

    def run(self, signals: pd.DataFrame, beta: pd.Series = None):
        df = self.data.join(signals).copy()

        df['pos_a'] = 0.0
        df['pos_b'] = 0.0
        df['pnl'] = 0.0
        df['position'] = 0        # 0 flat, +1 long-spread, −1 short-spread

        state = 0
        size_a = size_b = 0.0
        entry_pa = entry_pb = np.nan

        for t in df.index:
            pa, pb = df.at[t, self.sym_a], df.at[t, self.sym_b]
            beta_t = None if beta is None else beta.at[t]

            if state != 0:
                sign = 1 if state == 1 else -1
                pnl_pct_a = sign * (pa - entry_pa) / entry_pa
                pnl_pct_b = sign * (entry_pb - pb) / entry_pb

                exit_sig = df.at[t, 'exit']
                stop_sig = (pnl_pct_a < -self.params.stop_loss) or (pnl_pct_b < -self.params.stop_loss)

                if exit_sig or stop_sig:
                    df.at[t, 'pnl'] = (pa - entry_pa) * size_a + (pb - entry_pb) * size_b
                    state = 0
                    size_a = size_b = 0.0

            if state == 0:
                if df.at[t, 'long']:
                    state = 1
                elif df.at[t, 'short']:
                    state = -1

                if state != 0:
                    size_a_abs, size_b_abs = self.get_position_sizes(pa, pb, beta_t)
                    size_a = state * size_a_abs      # +A or −A
                    size_b = -state * size_b_abs      # −B or +B
                    entry_pa, entry_pb = pa, pb

            df.at[t, 'pos_a'] = size_a
            df.at[t, 'pos_b'] = size_b
            df.at[t, 'position'] = state

        df['cum_pnl'] = df['pnl'].cumsum()
        return df
