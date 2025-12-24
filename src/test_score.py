import pandas as pd
from score import score_submission

df = pd.read_csv("submissions/baseline.csv")

# strip the 's' prefix
for c in ["x", "y", "deg"]:
    df[c] = df[c].astype(str).str[1:]

print("Local score:", score_submission(df))
