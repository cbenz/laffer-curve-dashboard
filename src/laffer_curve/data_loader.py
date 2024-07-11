import pandas as pd
from dbnomics import fetch_series


def load_revenue():
    taxrev_df = fetch_series(
        [
            "OECD/REV/NES.TOTALTAX.TAXUSD.CAN",
            "OECD/REV/NES.TOTALTAX.TAXUSD.CHE",
            "OECD/REV/NES.TOTALTAX.TAXUSD.DEU",
            "OECD/REV/NES.TOTALTAX.TAXUSD.ESP",
            "OECD/REV/NES.TOTALTAX.TAXUSD.FRA",
            "OECD/REV/NES.TOTALTAX.TAXUSD.GBR",
            "OECD/REV/NES.TOTALTAX.TAXUSD.JPN",
            "OECD/REV/NES.TOTALTAX.TAXUSD.MEX",
            "OECD/REV/NES.TOTALTAX.TAXUSD.USA",
        ]
    )

    print(taxrev_df.columns)

    col_rev = ["original_period", "value", "Country"]

    df_rev = taxrev_df[col_rev].rename(columns={"value": "Revenue"}).dropna()

    return df_rev


def load_tax():
    taxrate_df = fetch_series(
        [
            "WB/WDI/A-IC.TAX.TOTL.CP.ZS-CAN",
            "WB/WDI/A-IC.TAX.TOTL.CP.ZS-CHE",
            "WB/WDI/A-IC.TAX.TOTL.CP.ZS-DEU",
            "WB/WDI/A-IC.TAX.TOTL.CP.ZS-ESP",
            "WB/WDI/A-IC.TAX.TOTL.CP.ZS-FRA",
            "WB/WDI/A-IC.TAX.TOTL.CP.ZS-GBR",
            "WB/WDI/A-IC.TAX.TOTL.CP.ZS-JPN",
            "WB/WDI/A-IC.TAX.TOTL.CP.ZS-MEX",
            "WB/WDI/A-IC.TAX.TOTL.CP.ZS-USA",
        ]
    )
    print(taxrate_df.columns)

    col_tax = ["original_period", "value", "country (label)"]

    df_tax = (
        taxrate_df[col_tax]
        .rename(columns={"country (label)": "Country", "value": "Taxe_rate"})
        .dropna()
    )

    return df_tax


def load_income_tax_data():
    taxrate_income = fetch_series(
        [
            "OECD/DP_LIVE/CAN.TAXINCOME.TOT.PC_GDP.A",
            "OECD/DP_LIVE/CHE.TAXINCOME.TOT.PC_GDP.A",
            "OECD/DP_LIVE/DEU.TAXINCOME.TOT.PC_GDP.A",
            "OECD/DP_LIVE/ESP.TAXINCOME.TOT.PC_GDP.A",
            "OECD/DP_LIVE/FRA.TAXINCOME.TOT.PC_GDP.A",
            "OECD/DP_LIVE/GBR.TAXINCOME.TOT.PC_GDP.A",
            "OECD/DP_LIVE/JPN.TAXINCOME.TOT.PC_GDP.A",
            "OECD/DP_LIVE/MEX.TAXINCOME.TOT.PC_GDP.A",
            "OECD/DP_LIVE/USA.TAXINCOME.TOT.PC_GDP.A",
        ]
    )

    col_tax_in = ["original_period", "value", "Country"]

    df_tax_in = (
        taxrate_income[col_tax_in].rename(columns={"value": "Taxe_rate"}).dropna()
    )

    return df_tax_in


def merge_series(dfs):
    df_tax, df_rev = dfs

    if df_tax.empty or df_rev.empty:
        return {}

    countries = df_tax["Country"].unique()

    merged_dfs = {}
    for country in countries:
        country_dfs = [df[df["Country"] == country] for df in dfs]

        merged_df = country_dfs[0]
        for df in country_dfs[1:]:
            merged_df = pd.merge(merged_df, df, on="original_period", how="left")

        # Check if the merged DataFrame is empty
        if not merged_df.empty:
            merged_dfs[country] = merged_df

    return merged_dfs


def filter_non_empty_dataframes(merged_data):
    return {country: df for country, df in merged_data.items() if not df.empty}


def newmerge_series(newdfs):
    df_tax_in, df_rev = newdfs

    if df_tax_in.empty or df_rev.empty:
        return {}

    countries = df_tax_in["Country"].unique()

    merged_newdfs = {}
    for country in countries:
        country_newdfs = [newdf[newdf["Country"] == country] for newdf in newdfs]

        merged_newdf = country_newdfs[0]
        for newdf in country_newdfs[1:]:
            merged_newdf = pd.merge(
                merged_newdf, newdf, on="original_period", how="left"
            )

        # Check if the merged DataFrame is empty
        if not merged_newdf.empty:
            merged_newdfs[country] = merged_newdf

    return merged_newdfs


def filter_non_empty_newdataframes(newmerged_data):
    return {
        country: newdf for country, newdf in newmerged_data.items() if not newdf.empty
    }
