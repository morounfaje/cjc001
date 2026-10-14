import sys
import os

base = os.path.dirname(__file__)
for folder in ["data", "strategy", "backtest", "portfolio", "metrics"]:
    sys.path.append(os.path.join(base, folder))