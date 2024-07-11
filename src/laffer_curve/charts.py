import numpy as np
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import PolynomialFeatures


def plot_laffer_curve(df, country):
    df["original_period"] = pd.to_datetime(df["original_period"], errors="coerce")
    df = df.dropna(subset=["original_period"])
    df["date"] = df["original_period"].dt.strftime("%Y")
    df["customdata"] = df.apply(
        lambda row: [row["date"], row["Taxe_rate"], row["Revenue"]], axis=1
    )

    df = df.dropna(subset=["Taxe_rate", "Revenue"])

    fig = px.scatter(
        df,
        x="Taxe_rate",
        y="Revenue",
        title=f"Laffer curve for {country}",
        labels={
            "Taxe_rate": "Total tax and contribution rate (% of profit)",
            "Revenue": "Total tax revenue in USD (in Million) ",
        },
        custom_data=["date", "Taxe_rate", "Revenue"],
    )

    fig.update_traces(
        hovertemplate="<br>".join(
            [
                "Date: %{customdata[0]}",
                "Total tax and contribution rate (%): %{customdata[1]}",
                "Revenue in USD (in Million): %{customdata[2]}",
            ]
        ),
        marker=dict(size=8, symbol="circle-open-dot"),
        selector=dict(mode="markers"),
    )

    # Polynomial Regression
    poly_features = PolynomialFeatures(degree=3)
    X_poly = poly_features.fit_transform(df[["Taxe_rate"]])
    poly_model = LinearRegression()
    poly_model.fit(X_poly, df["Revenue"])

    x_line = np.linspace(df["Taxe_rate"].min(), df["Taxe_rate"].max(), 100)
    x_line_poly = poly_features.transform(x_line.reshape(-1, 1))
    y_line = poly_model.predict(x_line_poly)

    fig.add_trace(
        go.Scatter(
            x=x_line,
            y=y_line,
            mode="lines",
            name="Trend Line",
            line=dict(color="Deeppink", width=3),
        )
    )

    return fig

def plot_laffer_curve_income(newdf, country):
    newdf["original_period"] = pd.to_datetime(newdf["original_period"], errors="coerce")
    newdf = newdf.dropna(subset=["original_period"])
    newdf["date"] = newdf["original_period"].dt.strftime("%Y")
    newdf["customdata"] = newdf.apply(
        lambda row: [row["date"], row["Taxe_rate"], row["Revenue"]], axis=1
    )

    newdf = newdf.dropna(subset=["Taxe_rate", "Revenue"])

    fig = px.scatter(
        newdf,
        x="Taxe_rate",
        y="Revenue",
        title=f"Laffer curve for {country}",
        labels={
            "Taxe_rate": "Tax on personal income - Total  (% of GDP)",
            "Revenue": "Total tax revenue in USD (in Million) ",
        },
        custom_data=["date", "Taxe_rate", "Revenue"],
    )

    fig.update_traces(
        hovertemplate="<br>".join(
            [
                "Date: %{customdata[0]}",
                "Tax on personal income - Total  (% of GDP): %{customdata[1]}",
                "Revenue in USD (in Million): %{customdata[2]}",
            ]
        ),
        marker=dict(size=8, symbol="circle-open-dot"),
        selector=dict(mode="markers"),
    )

    # Polynomial Regression
    poly_features = PolynomialFeatures(degree=3)
    X_poly = poly_features.fit_transform(newdf[["Taxe_rate"]])
    poly_model = LinearRegression()
    poly_model.fit(X_poly, newdf["Revenue"])

    x_line = np.linspace(newdf["Taxe_rate"].min(), newdf["Taxe_rate"].max(), 100)
    x_line_poly = poly_features.transform(x_line.reshape(-1, 1))
    y_line = poly_model.predict(x_line_poly)

    fig.add_trace(
        go.Scatter(
            x=x_line,
            y=y_line,
            mode="lines",
            name="Trend Line",
            line=dict(color="Deeppink", width=3),
        )
    )

    return fig