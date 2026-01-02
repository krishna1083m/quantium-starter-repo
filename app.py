import pandas as pd
from dash import Dash, dcc, html
import plotly.express as px

df = pd.read_csv("processed_sales.csv")
df["date"] = pd.to_datetime(df["date"])


daily_sales = (
    df.groupby("date", as_index=False)["sales"]
    .sum()
    .sort_values("date")
)


fig = px.line(
    daily_sales,
    x="date",
    y="sales",
    title="Pink Morsel Sales Over Time"
)

fig.update_layout(
    xaxis_title="Date",
    yaxis_title="Total Sales",
)


app = Dash(__name__)

app.layout = html.Div(
    children=[
        html.H1(
            "Impact of Pink Morsel Price Increase on Sales",
            style={"textAlign": "center"}
        ),
        dcc.Graph(figure=fig)
    ]
)

if __name__ == "__main__":
    app.run(debug=True)
