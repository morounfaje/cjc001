\# CJC001 — Results



> \*\*v2 update:\*\* This version upgrades the original 100-day research with a

> full 1-year dataset and multi-timeframe analysis. The 100-day finding

> wasn't wrong — it was incomplete. See "Sampling bias" below.



\## Datasets



| | 100-day (v1) | 1-year (v2) |

|---|---|---|

| Candles | 143,998 | 525,600 |

| Period | \~Jul-Oct 2026 | Oct 2025 - Oct 2026 |

| Dataset version | `98b663f87e02d561` | `5561f6d2894c36d3` |



Source: Deriv public market-data feed (`data/download\_deriv.py`), symbol

`R\_100`, no login/account required. Note: \~1 year is the practical history

limit of this feed for 1-minute candles — requests for more return

overlapping data, which `dedupe\_and\_sort()` correctly collapses.



\## Strategy tested



SMA 20 / SMA 50 crossover, long-only, next-bar execution.

`starting\_cash = 10,000`, `fee\_rate = 0.001`, `slippage = 0.0005`.



\## Results across timeframes (1-year dataset)



| Timeframe | Return | Drawdown | Trades | Win rate |

|---|---|---|---|---|

| 1-minute | -100.00% | -100.00% | 5,946 | 27.6% |

| 5-minute | -98.01% | -98.03% | 1,189 | 31.4% |

| 15-minute | -77.67% | -81.10% | 403 | 33.7% |

| 1-hour | -75.26% | -78.79% | 109 | 30.3% |

| 4-hour | +17.60% | -41.33% | 21 | 33.3% |

| Buy \& Hold | -40.93% | -79.10% | 1 | - |



(100-day results for comparison: 1-min -98.90%, 5-min -58.41%,

15-min -11.09%, 1-hour -41.56%, 4-hour -31.16%, Buy\&Hold +62.04%.)



\## Key findings



\*\*1. Overtrading destroys accounts on fast timeframes.\*\*

Every account-wipeout result (1-min through 1-hour) traces back to trade

frequency: thousands of round-trips each paying \~0.3% in fees and

slippage compounds multiplicatively. At 1-minute bars on the full year,

5,946 trades compounded costs down to $0.0001 of a $10,000 account -

confirmed by direct calculation (0.997^2973 \~ 0.00009), not a bug.



\*\*2. Sampling bias: short windows can mislead.\*\*

The 100-day sample showed buy-and-hold up +62%. The full year showed

buy-and-hold down -41%, because R\_100 fell from 1066 to 632 over the

year - the 100-day window had simply landed in a rising stretch of a

longer downtrend. This is the single most important lesson from this

project: a short backtest window can show you a real but unrepresentative

slice of the market.



\*\*3. The 4-hour "winning" result does not hold up under inspection.\*\*

+17.60% looked like a genuine edge until we broke down the 21 trades

individually (`inspect\_4h\_trades.py`). The top 3 winning trades totaled

$12,572 against a total profit of only $2,610 - meaning the other 18

trades lost \~$9,962 net combined. Two single trades (+46.04% and

+84.87%, each catching one large sustained trend) account for the

entire positive result. Remove either one and the year is a loss.

With 21 trades, this is not a statistically reliable sample.



\## Honest overall conclusion



Across every timeframe and both sample windows tested, SMA 20/50

crossover on Deriv R\_100 shows no reliable, repeatable edge once

realistic trading costs are included. The one apparently profitable

result (4-hour) is explained by two outlier trades, not a consistent

strategy advantage. Slower timeframes meaningfully reduce cost drag,

but reducing damage is not the same as proving a strategy works.


## EMA vs SMA comparison (v3)

Same engine, same 1-year dataset, same costs — only the moving-average
type changed (SMA 20/50 vs EMA 20/50, both crossover-based).

| Timeframe | SMA Return | SMA Win% | EMA Return | EMA Win% |
|---|---|---|---|---|
| 1-minute | -100.00% | 27.6% | -100.00% | 23.2% |
| 5-minute | -98.01% | 31.4% | -97.55% | 23.8% |
| 15-minute | -77.67% | 33.7% | -77.05% | 29.2% |
| 1-hour | -75.26% | 30.3% | -67.15% | 17.2% |
| 4-hour | +17.60% | 33.3% | -43.95% | 14.8% |

EMA's win rate is lower than SMA's at every single timeframe tested - a
consistent 5-for-5 pattern, not noise. Most tellingly, EMA did not
replicate SMA's one apparently "winning" 4-hour result: EMA lost 43.95%
over the same period SMA gained 17.60%. Since EMA is a close structural
cousin of SMA (same crossover idea, faster-reacting average), a real
trend-following edge in this market should plausibly show up in both.
Its absence in EMA is further evidence the SMA 4-hour result was driven
by chance (two outlier trades, documented above) rather than a genuine,
repeatable edge.

**Conclusion:** faster-reacting EMA does not outperform SMA on R_100 -
if anything, it performs modestly worse by win rate across the board.
Neither moving-average type produces a reliable edge once realistic
costs are included, across any timeframe tested.



\## Reproducing this result



pip install -r requirements.txt

python data/download\_deriv.py

python main.py

python compare\_timeframes.py

python inspect\_4h\_trades.py



Re-running `download\_deriv.py` pulls fresh, current data - results will

differ from the dataset versions above, since R\_100's market data is

continuously updated. This is expected; the dataset version hashes

above identify exactly which data produced these specific results.

