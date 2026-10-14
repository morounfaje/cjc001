import time
import json
import csv
import os
from datetime import datetime, timezone
import websocket

URL = "wss://api.derivws.com/trading/v1/options/ws/public"
SYMBOL = "R_100"
GRANULARITY = 60
BATCH_SIZE = 1000
NUM_BATCHES = 1052  # ~730 days (2 years)
OUT_PATH = "r100_1m.csv"
PROGRESS_PATH = "r100_1m_partial.csv"
SAVE_EVERY = 50
MAX_RETRIES = 5


def fetch_batch(end_epoch):
    request = {
        "ticks_history": SYMBOL,
        "end": end_epoch,
        "count": BATCH_SIZE,
        "style": "candles",
        "granularity": GRANULARITY,
    }
    ws = websocket.create_connection(URL, timeout=30)
    try:
        ws.send(json.dumps(request))
        response = json.loads(ws.recv())
    finally:
        ws.close()

    if "error" in response:
        raise RuntimeError(response["error"])

    return response["candles"]


def fetch_batch_with_retry(end_epoch):
    for attempt in range(1, MAX_RETRIES + 1):
        try:
            return fetch_batch(end_epoch)
        except Exception as e:
            wait = attempt * 3
            print(f"  Attempt {attempt} failed ({e}). Retrying in {wait}s...")
            time.sleep(wait)
    raise RuntimeError(f"Failed after {MAX_RETRIES} attempts")


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


def fetch_all_candles():
    all_candles = []
    end_epoch = "latest"

    for batch_num in range(NUM_BATCHES):
        candles = fetch_batch_with_retry(end_epoch)
        if not candles:
            print(f"Batch {batch_num + 1}: no more data available, stopping early.")
            break

        all_candles = candles + all_candles
        end_epoch = candles[0]["epoch"] - 1
        print(f"Batch {batch_num + 1}/{NUM_BATCHES}: got {len(candles)} candles, total so far: {len(all_candles)}")

        if (batch_num + 1) % SAVE_EVERY == 0:
            save_csv(dedupe_and_sort(all_candles), PROGRESS_PATH)
            print(f"  Progress saved to {PROGRESS_PATH} ({len(all_candles)} candles so far)")

        time.sleep(0.5)

    return all_candles


if __name__ == "__main__":
    candles = fetch_all_candles()
    candles = dedupe_and_sort(candles)
    candles = candles[:-1]
    save_csv(candles, OUT_PATH)
    if os.path.exists(PROGRESS_PATH):
        os.remove(PROGRESS_PATH)
    print(f"Saved {len(candles)} candles to {OUT_PATH}")
    print("First:", candles[0])
    print("Last:", candles[-1])