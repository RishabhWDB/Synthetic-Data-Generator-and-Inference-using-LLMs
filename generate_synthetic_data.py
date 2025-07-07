import pandas as pd
from sdv.tabular import CTGAN

df = pd.read_csv("real_data.csv")

model = CTGAN()
model.fit(df)

synthetic_df = model.sample(100)

synthetic_df.to_csv("synthetic_data.csv", index=False)
print("[+] Saved 100 synthetic samples to synthetic_data.csv")
