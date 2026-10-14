\# CJC001 — Results



\## Dataset

\- Instrument: Deriv Volatility 100 Index (symbol `R\_100`)

\- Timeframe: 1-minute candles

\- Period: \~100 days (143,998 candles)

\- Source: Deriv public market-data feed (`data/download\_deriv.py`), no login/account required

\- Dataset version (SHA-256 fingerprint of the CSV): `98b663f87e02d561`



\## Strategy tested

SMA 20 / SMA 50 crossover, long-only, next-bar execution.

\- `fast\_window = 20`, `slow\_window = 50`

\- `starting\_cash = 10,000`

\- `fee\_rate = 0.001`, `slippage = 0.0005`



\## Result



| | SMA 20/50 Strategy | Buy \& Hold Benchmark |

|---|---|---|

| Total return | -98.90% | +62.04% |

| Max drawdown | -98.93% | -29.44% |

| Sharpe ratio | -0.030 | — |

| Trades | 1,617 | 1 |

| Win rate | 28.8% | — |



\## Conclusion



On 1-minute R\_100 bars over this 100-day sample, SMA 20/50 crossover is

not viable - it essentially destroyed the account. The main cause

appears to be overtrading: 1,617 trades (\~16/day) each paying \~0.3%

round-trip in fees and slippage, compounding to near-total capital loss

regardless of whether individual trades were profitable. Buy-and-hold

comfortably outperformed active trading over the same window.



\## Open question



Would a slower timeframe (5-minute or 15-minute bars) reduce trade

frequency enough to survive realistic costs? Not yet tested.



\## Reproducing this result



pip install -r requirements.txt

python data/download\_deriv.py

python main.py



Note: re-running download\_deriv.py will pull fresh, current data -

results will differ from the dataset version above, since Deriv's

market data changes constantly. This is expected and is why the

dataset version hash is recorded.

