import pandas as pd
from pathlib import Path

DATA_DIR= Path("data")

dfs=[]
for file in DATA_DIR.glob("*.csv"):
    df=pd.read_csv(file)
    dfs.append(df)

data=pd.concat(dfs,ignore_index=True)

data=data[data["product"]=="pink morsel"]#only to keep pink morsel

data["sales"]=data["quantity"]*data["price"]

final_data=data[["sales","date","region"]]

final_data.to_csv("processed_sales.csv",index=False)


print("done with processing,Output saved to processed_sales.csv")