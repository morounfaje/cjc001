import time
import json
import csv
from datetime import datetime, timezone
import websocket

URL = "wss://api.derivws.com/trading/v1/options/ws/public"
SYMBOL = "R_100"
GRANULARITY = 60
BATCH_SIZE = 1000
NUM_BATCHES = 144  # 144 x 1000 minutes ~= 100 days
OUT_PATH = "r100_1m.csv"


def fetch_batch(end_epoch):
    request = {
        "ticks_history": SYMBOL,
        "end": end_epoch,
        "count": BATCH_SIZE,
        "style": "candles",
        "granularity": GRANULARITY,
    }
    ws = websocket.create_connection(URL, timeout=30)
    ws.send(json.dumps(request))
    response = json.loads(ws.recv())
    ws.close()

    if "error" in response:
        raise RuntimeError(response["error"])

    return response["candles"]


def fetch_all_candles():
    all_candles = []
    end_epoch = "latest"

    for batch_num in range(NUM_BATCHES):
        candles = fetch_batch(end_epoch)
        if not candles:
            print(f"Batch {batch_num + 1}: no more data available, stopping early.")
            break

        all_candles = candles + all_candles
        end_epoch = candles[0]["epoch"] - 1
        print(f"Batch {batch_num + 1}/{NUM_BATCHES}: got {len(candles)} candles, total so far: {len(all_candles)}")
        time.sleep(0.5)

    return all_candles


def dedupe_and_sort(candles):
    seen = {}
    for c in candles:
        seen[c["epoch"]] = c
    return [seen[epoch] for epoch in sorted(seen)]


def save_csv(candles, path):
    with open(path, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["timestamp", "open", "high", "low", "close"])
        for c in candles:
            ts = datetime.fromtimestamp(c["epoch"], tz=timezone.utc).isoformat()
            writer.writerow([ts, c["open"], c["high"], c["low"], c["close"]])


if __name__ == "__main__":
    candles = fetch_all_candles()
    candles = dedupe_and_sort(candles)
    candles = candles[:-1]
    save_csv(candles, OUT_PATH)
    print(f"Saved {len(candles)} candles to {OUT_PATH}")
    print("First:", candles[0])
    print("Last:", candles[-1])