import pandas as pd

rows = []

SPACING = 0.8   # small enough to stay in bounds

for n in range(1, 201):
    start_x = - (n - 1) * SPACING / 2  # center around 0

    for i in range(n):
        x = start_x + i * SPACING

        rows.append({
            "id": f"{n:03d}_{i}",
            "x": f"s{x}",
            "y": "s0.0",
            "deg": "s0.0"
        })

df = pd.DataFrame(rows)
df.to_csv("submissions/baseline.csv", index=False)

print("baseline.csv generated")
