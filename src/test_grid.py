import pandas as pd
from score import score_submission

df = pd.read_csv("submissions/grid.csv")

for c in ["x", "y", "deg"]:
    df[c] = df[c].astype(str).str[1:]

print("Grid score:", score_submission(df))
