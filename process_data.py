import pandas as pd
from pathlib import Path

DATA_DIR = Path("data")

dfs = []
for file in DATA_DIR.glob("*.csv"):
    dfs.append(pd.read_csv(file))

data = pd.concat(dfs, ignore_index=True)



data = data[data["product"] == "pink morsel"]


data["price"] = (
    data["price"]
    .astype(str)
    .str.replace("$", "", regex=False)
    .astype(float)
)

data["quantity"] = data["quantity"].astype(int)


data["sales"] = data["quantity"] * data["price"]


final_data = data[["sales", "date", "region"]]

final_data.to_csv("processed_sales.csv", index=False)

