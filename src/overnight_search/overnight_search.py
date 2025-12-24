import math
import json
import hashlib
import time
from pathlib import Path
from itertools import product
from concurrent.futures import ProcessPoolExecutor, as_completed

import pandas as pd
from score import score_submission

ROOT = Path(__file__).resolve().parents[1]
RESULTS_DIR = ROOT / "overnight_search" / "results"
BEST_DIR = ROOT / "overnight_search" / "best"

RESULTS_DIR.mkdir(parents=True, exist_ok=True)
BEST_DIR.mkdir(parents=True, exist_ok=True)

# ------------------------
# helpers
# ------------------------

def frange(a, b, step):
    x = a
    while x <= b + 1e-12:
        yield round(x, 6)
        x += step

def config_signature(cfg: dict) -> str:
    """Unique, order-independent signature for a config"""
    payload = json.dumps(cfg, sort_keys=True)
    return hashlib.md5(payload.encode()).hexdigest()

def load_done_signatures(csv_path):
    if not csv_path.exists():
        return set()
    df = pd.read_csv(csv_path)
    return set(df["signature"].values)

# ------------------------
# packing logic
# ------------------------

def generate_placements(n, cfg):
    dx = cfg["dx"]
    dy = cfg["dy"]
    offset = cfg["offset"]
    rots = cfg["rots"]
    cbx = cfg["cbx"]
    cby = cfg["cby"]
    odd_even = cfg["odd_even"]
    dxr = cfg["dxr"]
    dyr = cfg["dyr"]

    cols = math.ceil(math.sqrt(n))
    rows = math.ceil(n / cols)

    start_x = - (cols - 1) * dx / 2
    start_y = - (rows - 1) * dy / 2

    out = []
    idx = 0
    for r in range(rows):
        rdx = dx * (dxr if (odd_even and r % 2) else 1.0)
        rdy = dy * (dyr if (odd_even and r % 2) else 1.0)
        xoff = rdx * offset if (r % 2) else 0.0
        ang = rots[r % len(rots)]

        for c in range(cols):
            if idx >= n:
                break
            x = start_x + c * rdx + xoff + cbx
            y = start_y + r * rdy + cby
            out.append((x, y, ang))
            idx += 1
    return out

def build_submission(cfg):
    rows = []
    for n in range(1, 201):
        pts = generate_placements(n, cfg)
        for i, (x, y, d) in enumerate(pts[:n]):
            rows.append({
                "id": f"{n:03d}_{i}",
                "x": str(x),
                "y": str(y),
                "deg": str(d)
            })
    return pd.DataFrame(rows)

def evaluate(cfg):
    try:
        df = build_submission(cfg)
        score = score_submission(df)
        return score
    except Exception:
        return None

# ------------------------
# main search
# ------------------------

def run_search(configs, results_csv, workers=13, top_k=20, log_every=25):
    done = load_done_signatures(results_csv)
    total = len(configs)
    pending = [cfg for cfg in configs if config_signature(cfg) not in done]

    print(f"Total configs: {total}")
    print(f"Already evaluated: {len(done)}")
    print(f"New configs to evaluate: {len(pending)}")
    print("-" * 60)

    start_time = time.time()
    completed = 0
    best = []

    with ProcessPoolExecutor(max_workers=workers) as exe:
        futures = {exe.submit(evaluate, cfg): cfg for cfg in pending}

        for fut in as_completed(futures):
            cfg = futures[fut]
            sig = config_signature(cfg)
            score = fut.result()

            completed += 1
            elapsed = time.time() - start_time
            rate = completed / elapsed if elapsed > 0 else 0.0
            remaining = (len(pending) - completed) / rate if rate > 0 else float("inf")

            row = {**cfg, "score": score, "signature": sig}
            df_row = pd.DataFrame([row])

            if results_csv.exists():
                df_row.to_csv(results_csv, mode="a", index=False, header=False)
            else:
                df_row.to_csv(results_csv, index=False)

            if score is not None:
                best.append((score, cfg))
                best.sort(key=lambda x: x[0])
                best[:] = best[:top_k]

            # 🔔 PROGRESS LOG
            if completed % log_every == 0 or completed == len(pending):
                percent = (completed / len(pending)) * 100
                best_score = best[0][0] if best else None
                print(
                    f"[{completed}/{len(pending)} | {percent:6.2f}%] "
                    f"Best: {best_score:.6f} | "
                    f"Elapsed: {elapsed/60:5.1f} min | "
                    f"ETA: {remaining/60:5.1f} min | "
                    f"Rate: {rate:5.2f} cfg/s"
                )

    print("=" * 60)
    print("Search completed.")
    print("Top results:")
    for s, cfg in best[:5]:
        print(f"  Score {s:.6f} → {cfg}")

    return best


# ------------------------
# entry point
# ------------------------

if __name__ == "__main__":

    # 🔁 rotation patterns (add more anytime!)
    rotation_patterns = [
        # (0.0, 180.0),
        # (30.0, 210.0),
        # (45.0, 225.0),
        # (90.0, 270.0),
        # (15.0, 195.0),
        # (10.0, 190.0),
        (5.0, 185.0),
        (0.0, 90.0, 180.0, 270.0),
        (330.0, 150.0),
        # (20.0, 200.0),
    ]

    # 🟦 COARSE parameters
    dx_vals = list(frange(0.67, 0.73, 0.003))
    dy_vals = list(frange(0.79, 0.85, 0.003))
    offsets = [0.45, 0.5, 0.55]
    biases = [-0.02, 0.0, 0.02]
    odd_even_opts = [False, True]
    dxr_vals = [1.0, 0.95, 1.05]
    dyr_vals = [1.0, 0.98, 1.02]

    configs = []
    for dx, dy, off, cbx, cby, oe, dxr, dyr, rot in product(
        dx_vals, dy_vals, offsets, biases, biases,
        odd_even_opts, dxr_vals, dyr_vals, rotation_patterns
    ):
        configs.append({
            "dx": dx, "dy": dy,
            "offset": off,
            "cbx": cbx, "cby": cby,
            "odd_even": oe,
            "dxr": dxr, "dyr": dyr,
            "rots": rot
        })

    print(f"Total configs generated: {len(configs)}")

    best = run_search(
        configs,
        results_csv=RESULTS_DIR / "coarse_results.csv",
        workers=12,
        top_k=20
    )

    print("Best so far:")
    for s, cfg in best[:5]:
        print(s, cfg)
