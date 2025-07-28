import pandas as pd
import itertools, yaml
from pathlib import Path
import matplotlib.pyplot as plt
import statsmodels.api as sm
from src.data import get_pair_prices
from src.model import fit_rolling_ols, z_score, generate_signals, SignalParams
from src.backtest import BacktestEngine, compute_metrics

def get_static_adf_value(price_df, symbol_a, symbol_b):
    X = sm.add_constant(price_df[symbol_b])
    static_ols = sm.OLS(price_df[symbol_a], X).fit()
    alpha_static = static_ols.params["const"]
    beta_static = static_ols.params[symbol_b]

    residuals_static = price_df[symbol_a] - (
            alpha_static + beta_static * price_df[symbol_b])

    adf_stat, p_val, *_ = sm.tsa.adfuller(residuals_static.dropna())

    return adf_stat, p_val


PAIRS = yaml.safe_load(open("pairs.yml"))  # [{type: etf, symbols:[EEM,VWO]}, …]
PARAM_GRID = {
    "entry_z":   [2.0, 2.5, 3.0],
    "exit_z":    [0.05, 0.25],
    "window":    [40, 50, 60],
    "abs_floor": [0.0, 0.5],
}

results = []
for pair in PAIRS:
    if pair["type"] not in ["etf", "crypto"]:
        print(f"Skipping unsupported pair type: {pair['type']}")
        continue
    symbol_a, symbol_b = pair["symbols"]
    price_df = get_pair_prices(pair["symbols"], type=pair["type"], start_date='2023-01-01')
    adf_statistic, p_value = get_static_adf_value(price_df, symbol_a, symbol_b)
    for (e, x, w, f) in itertools.product(*PARAM_GRID.values()):
        alpha, beta = fit_rolling_ols(price_df[symbol_a], price_df[symbol_b], window=w)
        residuals = (price_df[symbol_a] - (alpha + beta*price_df[symbol_b])).dropna()
        z = z_score(residuals, window=w)
        sig = generate_signals(z, residuals, SignalParams(e, x, f))
        bt = BacktestEngine(price_df).run(sig, beta)
        metr = compute_metrics(bt, symbol_a, symbol_b)
        metr.update(
            dict(pair=f"{symbol_a}/{symbol_b}", entry=e, exit=x, window=w,
                 floor=f, adf_statistic=adf_statistic, p_value=p_value)
        )
        results.append(metr)
        # save equity curve
        curve_path = Path(f"plots/{symbol_a.replace('/', '-')}_{symbol_b.replace('/', '-')}_e{e}_x{x}_w{w}_f{f}.png")
        bt['cum_pnl'].plot(title=str(curve_path.stem)).figure.savefig(curve_path)
        plt.close()
        print(f"Completed {pair['type']} {symbol_a.replace('/', '-')}/{symbol_b.replace('/', '-')} e={e}, x={x}, w={w}, f={f}")

Path("results").mkdir(exist_ok=True)
pd.DataFrame(results).to_csv("results/grid_summary.csv", index=False)
