import importlib

import numpy as np
import plotly.graph_objects as go
import streamlit as st
from charts import plot_laffer_curve, plot_laffer_curve_income
from data_loader import (
    filter_non_empty_dataframes,
    filter_non_empty_newdataframes,
    load_income_tax_data,
    load_revenue,
    load_tax,
    merge_series,
    newmerge_series,
)
from streamlit_option_menu import option_menu


def main():
    package_dir = importlib.resources.files("laffer_curve")
    st.set_page_config(
        page_title="DBnomics Laffer Curve",
        page_icon=str(package_dir / "images/favicon.png"),
    )
    st.image(str(package_dir / "images/dbnomics.svg"), width=300)

    st.title(":blue[Laffer Curve]")

    def local_css(file_name):
        with open(file_name) as f:
            st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

    local_css(package_dir / "assets/styles.css")

    st.markdown(
        """
        <style>
        hr {
            height: 1px;
            border: none;
            color: #333;
            background-color: #333;
            margin-top: 3px;
            margin-bottom: 3px;
        }
        }
        </style>
        """,
        unsafe_allow_html=True,
    )

    st.markdown("---")

    with st.sidebar:
        selected = option_menu(
            menu_title="Menu",
            options=[
                "Explanations",
                "Laffer Curve (household tax)",
                "Laffer Curve (business tax)",
                "Sources",
            ],
            icons=["book", "bar-chart", "bar-chart", "search"],
            menu_icon=":",
            default_index=0,
        )

    if selected == "Explanations":
        st.subheader(":blue[**Explanations**]")
        st.write(
            "The Laffer Curve is a hypothesis formulated by economist Arthur Laffer in 1974.\n"
            "\n"
            'Arthur Laffer (1940- ) is a liberal American economist. He is a proponent of "supply-side economics," a school of thought that argues stimulating growth requires supporting supply, and therefore businesses.\n'
            "He notably inspired Reagan's economic policies, which led to a significant reduction in taxes.\n"
            "\n"
            'Thus, Arthur Laffer defends the adage "too much tax kills tax". \n'
            "According to Laffer's theory, an increase in taxes contributes to the growth of state revenues up to a certain threshold.\n"
            "Once this threshold is passed, increasing taxes leads to a decrease in fiscal revenues.\n"
            "However, Laffer never defined this threshold, i.e., the tax rate that maximizes state revenues.\n"
        )

        # Laffer curve example
        tax_rates = np.linspace(0, 1, 500)
        revenues = tax_rates * (1 - tax_rates) ** 2 * 150

        fig = go.Figure()

        fig.add_trace(
            go.Scatter(
                x=tax_rates,
                y=revenues,
                mode="lines",
                name="Example of Laffer Curve",
                line=dict(color="Deeppink"),
            )
        )
        fig.add_vline(
            x=1 / 3,
            line=dict(color="gold", dash="dash"),
            annotation_text="Maximum",
            annotation_position="top",
        )

        fig.update_layout(
            title="Laffer Curve in theory",
            xaxis=dict(showticklabels=False),
            yaxis=dict(showticklabels=False),
            xaxis_title="Tax rate",
            yaxis_title="Taxe revenue",
            legend=dict(x=0.8, y=1.15),
            template="plotly_white",
        )

        st.plotly_chart(fig)

        st.write(
            "\n"
            '**Why "too much tax kills tax"?**\n'
            "A too high level of taxation would lead to an economic slowdown by discouraging households from working.\n"
            "\n"
            "According to Laffer, there would be two effects of reducing income taxes:\n"
            "1. **Immediate effect**: The reduction in taxes leads to an equivalent decrease in state revenues.\n"
            "2. **Long-term effect**: The money not spent on paying taxes will be spent elsewhere. Demand would increase, which would be beneficial for economic growth.\n"
            "\n"
            "Thus, two opposing effects would occur :\n"
            "1. **Income effect**: Increasing taxes would push workers to work more to maintain their income level.\n"
            "2. **Substitution effect**: Households would not seek to work more (due to the reduced income from additional work) and might decide to turn to leisure instead.\n"
            "\n"
            "*How to know which effect dominates?*\n"
            "\n"
            "Many economists reject Laffer's theory, finding it too simplistic. Empirical studies show the model's excessive simplicity.\n"
        )

    if selected == "Laffer Curve (household tax)":
        # Plot for Laffer Curve for Household
        st.subheader(":blue[**Charts**]")
        df_rev = load_revenue()
        df_tax_in = load_income_tax_data()
        merged_newdfs = newmerge_series((df_tax_in, df_rev))
        filtered_newdfs = filter_non_empty_newdataframes(merged_newdfs)

        country = st.selectbox("Select a country", list(filtered_newdfs.keys()))

        if country:
            fig = plot_laffer_curve_income(filtered_newdfs[country], country)
            st.plotly_chart(fig)

        st.write(
            "**Tax on personal income:**\n"
            "Taxes levied on the net income and capital gain of individuals and measured as % of GDP ([OECD](https://www.oecd.org/en/data/indicators/tax-on-personal-income.html))\n"
        )

    if selected == "Laffer Curve (business tax)":
        # Plot for Laffer Curve for business
        st.subheader(":blue[**Charts**]")
        df_rev = load_revenue()
        df_tax = load_tax()
        merged_dfs = merge_series((df_tax, df_rev))
        filtered_dfs = filter_non_empty_dataframes(merged_dfs)

        country = st.selectbox("Select a country", list(filtered_dfs.keys()))

        if country:
            fig = plot_laffer_curve(filtered_dfs[country], country)
            st.plotly_chart(fig)

        st.write(
            "**Tax rate and contribution rate (% of profit) :** \n"
            "This tax rate only measures the amount of taxes and mandatory contributitons payable by business and not household ([World Bank](https://databank.worldbank.org/metadataglossary/world-development-indicators/series/IC.TAX.TOTL.CP.ZS))\n"
        )
    if selected == "Sources":
        st.subheader("**Data**")
        st.write(
            "[Total tax and contribution rate](https://db.nomics.world/WB/WDI?q=Total+tax+and+contribution+rate&tab=list)\n"
            "\n"
            "[Tax Revenue](https://db.nomics.world/OECD/REV?tab=list)\n"
        )
        st.markdown("---")
        st.write("[Source Code](https://github.com/dbnomics/laffer-curve-dashboard)")
        st.write("[DBnomics](https://db.nomics.world)")


if __name__ == "__main__":
    main()
