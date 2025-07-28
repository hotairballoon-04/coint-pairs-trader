# coint-pairs-trader 📈

A Python framework for **rolling-window cointegration pairs trading** across ETFs (and optionally cryptocurrencies).
Implements β-neutral hedging, stop-loss logic, parameter analysis, and detailed performance analytics.
For an introduction read `documentation/main.pdf`.

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
git clone https://github.com/hotairballoon-04/coint-pairs-trader.git
cd coint-pairs-trader
python -m venv venv && source venv/bin/activate  # (Windows: venv\Scripts\activate)
pip install -r requirements.txt
```

---

## ⚡ Quick Start Example
```python
from src.data import get_pair_prices
from src.model import (fit_rolling_ols, z_score,
                       generate_signals, SignalParams)
from src.backtest import BacktestEngine, compute_metrics

# Load ETF pair prices
data = get_pair_prices(['EEM', 'VWO'], type='etf', start_date='2018-01-01')

# Rolling hedge ratio & residual calculation
alpha, beta = fit_rolling_ols(data['EEM'], data['VWO'], window=50)
resid = data['EEM'] - (alpha + beta * data['VWO'])
z = z_score(resid, window=50)

# Generate entry/exit signals
signals = generate_signals(z, resid,
            SignalParams(entry_z=2.5, exit_z=0.05, abs_floor=0.0))

# Run backtest
bt = BacktestEngine(data).run(signals, beta)
metrics = compute_metrics(bt, 'EEM', 'VWO')
print(metrics)
```

---

## 🔧 Features
- Rolling OLS hedge ratio estimation
- $\beta$-neutral or equal-weight sizing
- Z-score entry/exit + optional stop-loss
- Full parameter sweep
- Performance metrics: Sharpe, max DD, time invested, total return

Main functionality can be found in `src`. Smaller visualisations and evaluations in `experiments` and `notebooks`.

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
Lukas Schaller — [LinkedIn](https://www.linkedin.com/in/lukas-schaller)
