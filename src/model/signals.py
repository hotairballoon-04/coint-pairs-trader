import pandas as pd
from dataclasses import dataclass


@dataclass
class SignalParams:
    entry_z: float = 2.5
    exit_z:  float = 0.05
    abs_floor: float = 0.0   # trade only if |residual| >= abs_floor


def generate_signals(z: pd.Series,
             residual: pd.Series,
             params: SignalParams) -> pd.DataFrame:
    """
    Generate trading signals based on the z-score of the residuals.
    :param z:           Z-scores of the residuals
    :param residual:    residuals
    :param params:      Parameters for signal generation
    :return:            DataFrame with trading signals
    """
    long_entry = (z < -params.entry_z) & (abs(residual) >= params.abs_floor)
    short_entry = (z > params.entry_z) & (abs(residual) >= params.abs_floor)
    exit_sig = (abs(z) < params.exit_z)
    return pd.DataFrame({
        'long': long_entry,
        'short': short_entry,
        'exit': exit_sig
    })
