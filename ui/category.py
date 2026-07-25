"""
==========================================================
File : category.py

ConfigVista AI

Category Analytics Dashboard

Author : Shivam Saxena
==========================================================
"""

from __future__ import annotations

import streamlit as st
import pandas as pd

from comparison.models import ComparisonResult


# ==========================================================
# HELPERS
# ==========================================================

def _category_dataframe(result: ComparisonResult) -> pd.DataFrame:
    """
    Convert category summary into dataframe.
    """

    rows = []

    for item in result.category_summary:

        rows.append(
            {
                "Category": item.category.value,
                "Total Changes": item.total_changes,
                "High Risk": item.high_risk,
                "Medium Risk": item.medium_risk,
                "Low Risk": item.low_risk,
            }
        )

    return pd.DataFrame(rows)


# ==========================================================
# MAIN RENDERER
# ==========================================================

def render_category(result: ComparisonResult):

    st.header("Category Analysis")

    if not result.category_summary:

        st.info("No configuration changes detected.")

        return

    # ------------------------------------------------------
    # KPI SUMMARY
    # ------------------------------------------------------

    total_categories = len(result.category_summary)

    most_changed = max(
        result.category_summary,
        key=lambda x: x.total_changes,
    )

    highest_risk = max(
        result.category_summary,
        key=lambda x: x.high_risk,
    )

    c1, c2, c3 = st.columns(3)

    c1.metric(
        "Categories Changed",
        total_categories,
    )

    display_name = most_changed.category.value

    if display_name == "Unknown":
        display_name = "Needs Classification"
    
    c2.metric(
        "Most Modified",
        display_name,
    )

    c3.metric(
        "Highest Risk Category",
        highest_risk.category.value,
    )

    st.write("")

    # ------------------------------------------------------
    # CATEGORY TABLE
    # ------------------------------------------------------

    with st.container(border=True):

        st.subheader("Category Summary")

        df = _category_dataframe(result)

        st.dataframe(
            df,
            use_container_width=True,
            hide_index=True,
        )

    st.write("")

    # ------------------------------------------------------
    # BAR CHART
    # ------------------------------------------------------

    with st.container(border=True):

        st.subheader("Changes by Category")

        chart_df = (
            df.set_index("Category")["Total Changes"]
        )

        st.bar_chart(chart_df)

    st.write("")

    # ------------------------------------------------------
    # RISK DISTRIBUTION
    # ------------------------------------------------------

    with st.container(border=True):

        st.subheader("Risk Distribution")

        risk_df = (
            df.set_index("Category")[
                [
                    "High Risk",
                    "Medium Risk",
                    "Low Risk",
                ]
            ]
        )

        st.bar_chart(risk_df)

    st.write("")

    # ------------------------------------------------------
    # CATEGORY DETAILS
    # ------------------------------------------------------

    with st.container(border=True):

        st.subheader("Category Details")

        for item in result.category_summary:

            with st.expander(item.category.value):

                c1, c2, c3, c4 = st.columns(4)

                c1.metric(
                    "Total",
                    item.total_changes,
                )

                c2.metric(
                    "High",
                    item.high_risk,
                )

                c3.metric(
                    "Medium",
                    item.medium_risk,
                )

                c4.metric(
                    "Low",
                    item.low_risk,
                )

    st.write("")

    # ------------------------------------------------------
    # FUTURE AI ANALYTICS
    # ------------------------------------------------------

    with st.container(border=True):

        st.subheader("Future Analytics (Phase 2)")

        st.caption(
            "Reserved for ML-powered category insights."
        )

        st.markdown(
            """
Upcoming Enhancements

- Category Trend Analysis
- Historical Category Comparison
- ML Category Risk Prediction
- Top Risk Drivers
- Category-wise Success Rate
- Predictive Failure Analysis
- AI Recommendations
"""
        )

    st.divider()