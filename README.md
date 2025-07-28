# coint-pairs-trader 📈

A Python framework for **rolling-window cointegration pairs trading** across ETFs (and optionally cryptocurrencies).
Implements β-neutral hedging, stop-loss logic, parameter sweeps, and detailed performance analytics.

---

## 🚀 Overview
1. **Screen** pairs for cointegration (ADF test, $R^2$).
2. **Estimate** rolling OLS hedge ratio $(\alpha_t,\beta_t)$.
3. **Signal** on z-score thresholds; place β-neutral trades.
4. **Back-test** with optional transaction costs and stop-loss.
5. **Evaluate** Sharpe, max draw-down, invested Sharpe, and benchmark edge.

---

## 🗄️ Data Sources
| Asset class | Source (library)         |
|-------------|--------------------------|
| ETFs        | Yahoo Finance (`yfinance`) |
| Crypto      | Binance spot (`ccxt`)      |

Daily bars at 1d frequency (~1,000–2,000 days).

---

## 📦 Installation
```bash
git clone https://github.com/<YOUR-USER>/coint-pairs-trader.git
cd coint-pairs-trader
python -m venv venv && source venv/bin/activate  # (Windows: venv\Scripts\activate)
pip install -r requirements.txt
pip install -e .
```

---

## ⚡ Quick Start Example
```python
from src.data import get_pair_prices
from src.model import (fit_rolling_ols, z_score,
                       generate_signals, SignalParams)
from src.backtest.engine import BacktestEngine
from src.backtest.metrics import compute_metrics

# Load ETF pair prices
data = get_pair_prices(['EEM', 'VWO'], type='etf', start_date='2018-01-01')

# Rolling hedge ratio & residual calculation
alpha, beta = fit_rolling_ols(data['EEM'], data['VWO'], window=50)
resid       = data['EEM'] - (alpha + beta * data['VWO'])
z           = z_score(resid, window=50)

# Generate entry/exit signals
signals = generate_signals(z, resid,
            SignalParams(entry_z=2.5, exit_z=0.05, abs_floor=0.0))

# Run backtest
bt     = BacktestEngine(data).run(signals, beta)
metrics = compute_metrics(bt, 'EEM', 'VWO')
print(metrics)
```

---

## 🔧 Features
- Rolling OLS hedge ratio estimation (causal shift)
- β-neutral or equal-weight sizing
- Z-score entry/exit + optional stop-loss
- Full parameter sweep: CSV summary + heatmaps
- Performance metrics: Sharpe, max DD, time invested, benchmark edge
- Publication-quality plots with trade markers
- Unit tests via `pytest`

---

## 📈 Sample Results
| Pair     | Sharpe | Max DD | Edge vs 50-50 |
|----------|-------:|-------:|--------------:|
| TLT/IEF  |  1.04  |  -4.3% |         +1.04 |
| EEM/VWO  |  0.87  |  -0.5% |         +0.60 |

Cryptocurrency pairs failed cointegration screening or underperformed.

---

## 📝 Documentation
Full LaTeX report in `documentation/main.tex` covering:
1. Theory & background
2. Data preprocessing & screening
3. Strategy design & backtest implementation
4. Empirical results & robustness
5. Conclusion & appendix (pseudo-code)

---

## 🙏 Acknowledgements
Data via `yfinance` & `ccxt`; analysis in `pandas`, `numpy`, `statsmodels`.

---

### Contact
Lukas Schaller — lukas@example.com | [GitHub](https://github.com/<YOUR-USER>)