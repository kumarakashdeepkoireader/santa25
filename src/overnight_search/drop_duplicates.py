# merge_results.py
import pandas as pd

df1 = pd.read_csv("overnight_search/results/coarse_results_ayam.csv")
df2 = pd.read_csv("overnight_search/results/coarse_results_akash.csv")

df = pd.concat([df1, df2], ignore_index=True)
df = df.drop_duplicates(subset=["signature"])
df = df.sort_values("score")

df.to_csv("overnight_search/results/coarse_results_merged.csv", index=False)

print("Merged results:", len(df))
print(df.head(10))
