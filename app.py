import pandas as pd
from dash import Dash, dcc, html, Input, Output
import plotly.express as px

df = pd.read_csv("processed_sales.csv")
df["date"] = pd.to_datetime(df["date"])

# Create Dash app
app = Dash(__name__)

# App layout
app.layout = html.Div(
    style={
        "fontFamily": "Arial, sans-serif",
        "backgroundColor": "#f4f6f8",
        "padding": "30px",
    },
    children=[
        html.H1(
            "Pink Morsel Sales Visualiser",
            id="app-header",
            style={
                "textAlign": "center",
                "color": "#2c3e50",
                "marginBottom": "10px",
            },
        ),

        html.P(
            "Explore how Pink Morsel sales changed over time and across regions.",
            style={
                "textAlign": "center",
                "color": "#555",
                "marginBottom": "30px",
            },
        ),

        html.Div(
            style={
                "textAlign": "center",
                "marginBottom": "20px",
            },
            children=[
                dcc.RadioItems(
                    id="region-selector",
                    options=[
                        {"label": "All", "value": "all"},
                        {"label": "North", "value": "north"},
                        {"label": "East", "value": "east"},
                        {"label": "South", "value": "south"},
                        {"label": "West", "value": "west"},
                    ],
                    value="all",
                    inline=True,
                    style={"fontSize": "16px"},
                )
            ],
        ),

        html.Div(
            style={
                "backgroundColor": "white",
                "padding": "20px",
                "borderRadius": "8px",
                "boxShadow": "0 4px 10px rgba(0,0,0,0.1)",
            },
            children=[
                dcc.Graph(id="sales-line-chart")
            ],
        ),
    ],
)

REGION_COLORS = {
    "north": "#1f77b4",
    "south": "#ff7f0e",
    "east": "#2ca02c",
    "west": "#d62728",
}

@app.callback(
    Output("sales-line-chart", "figure"),
    Input("region-selector", "value"),
)
def update_chart(selected_region):

    if selected_region == "all":
        # Aggregate per date per region
        daily_sales = (
            df.groupby(["date", "region"], as_index=False)["sales"]
            .sum()
            .sort_values("date")
        )

        fig = px.line(
            daily_sales,
            x="date",
            y="sales",
            color="region",
            color_discrete_map=REGION_COLORS,
            title="Daily Pink Morsel Sales by Region",
        )

    else:
        filtered_df = df[df["region"] == selected_region]

        daily_sales = (
            filtered_df.groupby("date", as_index=False)["sales"]
            .sum()
            .sort_values("date")
        )

        fig = px.line(
            daily_sales,
            x="date",
            y="sales",
            title=f"Daily Pink Morsel Sales – {selected_region.capitalize()}",
        )

        fig.update_traces(line_color=REGION_COLORS[selected_region])

    fig.update_layout(
        xaxis_title="Date",
        yaxis_title="Total Sales",
        title_x=0.5,
        legend_title="Region",
    )

    return fig



if __name__ == "__main__":
    app.run(debug=True)
