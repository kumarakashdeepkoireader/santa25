import pandas as pd
from pack import grid_pack

rows = []

for n in range(1, 201):
    placements = grid_pack(n)

    for i, (x, y, deg) in enumerate(placements):
        rows.append({
            "id": f"{n:03d}_{i}",
            "x": f"s{x}",
            "y": f"s{y}",
            "deg": f"s{deg}"
        })

df = pd.DataFrame(rows)
df.to_csv("submissions/grid.csv", index=False)

print("grid.csv generated")
