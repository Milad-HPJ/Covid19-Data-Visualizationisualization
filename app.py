# Import packages
from dash import Dash, html, dash_table, dcc, callback, Output, Input
import dash_bootstrap_components as dbc
import plotly.express as px
import pandas as pd
import numpy as np
from sklearn.impute import SimpleImputer

# Incorporate data
df = pd.read_csv("WHO-COVID-19-global-data.csv")
df = df.drop(["Country_code"], axis=1)

# Renaming columns (only Date_reported to Date)
df.rename(columns={"Date_reported": "Date"}, inplace=True)

# Renaming rows (WHO region short hand to full sentence)
df.replace(
    {
        "EMRO": "Eastern Mediterranean Region",
        "EURO": "European Region",
        "AFRO": "African Region",
        "WPRO": "Western Pacific Region",
        "AMRO": "Region of the Americas",
        "SEARO": "South-East Asian Region",
    },
    inplace=True,
)

# Converts daates to pandas date format
df["Date"] = pd.to_datetime(df["Date"])

# Impute all the missing values using constant strategy (there are lots of strategy)
imputer = SimpleImputer(strategy="constant")
df = pd.DataFrame(imputer.fit_transform(df), columns=df.columns)

# Groups all the data to gether, addes all the records to each country and save it in df3
df = (
    df.groupby(["Country", "Date", "WHO_region"])[
        ["New_cases", "New_deaths", "Cumulative_cases", "Cumulative_deaths"]
    ]
    .sum()
    .reset_index()
)

# Getting number of counteries in the CSV file (237)
counteries = df["Country"].unique()

# Slicing the data-frame for faster load time, remove this for an accurate result
df = df[::20]

# Initialize the app - incorporate a Dash Bootstrap theme
external_stylesheets = [dbc.themes.CERULEAN]
app = Dash(__name__, external_stylesheets=external_stylesheets)


# App layout
app.layout = dbc.Container(
    [
        dbc.Row([html.Div("WHO-COVID-19-global-data", className="firstHedder")]),
        dbc.Row(
            [
                dbc.Container(
                    [dash_table.DataTable(data=df.to_dict("records"), page_size=12)]
                ),
                dbc.Row(
                    [
                        dbc.Col(
                            [
                                dbc.Row(
                                    [
                                        html.Div(
                                            "Select the Y axis",
                                            className="y-xSelector",
                                        ),
                                        dbc.RadioItems(
                                            options=[
                                                {"label": x, "value": x}
                                                for x in ["New_cases", "New_deaths"]
                                            ],
                                            value="New_cases",
                                            inline=True,
                                            id="yAxisRadio",
                                        ),
                                        html.Div(
                                            "Select the X axis",
                                            className="y-xSelector",
                                        ),
                                        dbc.RadioItems(
                                            options=[
                                                {"label": x, "value": x}
                                                for x in [
                                                    "Country",
                                                    "Date",
                                                    "WHO_region",
                                                ]
                                            ],
                                            value="WHO_region",
                                            inline=True,
                                            id="xAxisRadio",
                                        ),
                                    ]
                                ),
                                dbc.Col([dcc.Graph(figure={}, id="main-graph")], width=12)
                            ]
                        ),
                        
                        dbc.Col(
                            [
                                dbc.Row(
                                    [
                                        html.Div(
                                            "Select the Y axis",
                                            className="y-xSelector",
                                        ),
                                        dbc.RadioItems(
                                            options=[
                                                {"label": x, "value": x}
                                                for x in [
                                                    "Cumulative_cases",
                                                    "Cumulative_deaths",
                                                ]
                                            ],
                                            value="Cumulative_cases",
                                            inline=True,
                                            id="yAxisRadio2",
                                        ),
                                        html.Div(
                                            "Select rhe X axis",
                                            className="y-xSelector",
                                        ),
                                        dbc.RadioItems(
                                            options=[
                                                {"label": x, "value": x}
                                                for x in [
                                                    "Country",
                                                    "Date",
                                                    "WHO_region",
                                                ]
                                            ],
                                            value="WHO_region",
                                            inline=True,
                                            id="xAxisRadio2",
                                        ),
                                    ]
                                ),
                                dbc.Col(
                                    [dcc.Graph(figure={}, id="main-graph2")], width=12
                                ),
                            ]
                        ),
                    ]
                ),
            ]
        ),
    ],
    fluid=True,
)


# Add controls to build the interaction
@callback(
    Output(component_id="main-graph", component_property="figure"),
    Input(component_id="xAxisRadio", component_property="value"),
    Input(component_id="yAxisRadio", component_property="value"),
)
@callback(
    Output(component_id="main-graph2", component_property="figure"),
    Input(component_id="xAxisRadio2", component_property="value"),
    Input(component_id="yAxisRadio2", component_property="value"),
)
def update_graph(row_chosen, col_chosen):
    fig = px.histogram(df, x=row_chosen, y=col_chosen, histfunc="sum")
    return fig


def update_graph2(row_chosen, col_chosen):
    fig2 = px.histogram(df, x=row_chosen, y=col_chosen)
    return fig2


# Run the app
if __name__ == "__main__":
    app.run_server(debug=True)
