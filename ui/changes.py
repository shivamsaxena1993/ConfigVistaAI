"""
==========================================================
File : changes.py

ConfigVista AI

Configuration Changes Dashboard

Author : Shivam Saxena
==========================================================
"""

from __future__ import annotations

import pandas as pd
import streamlit as st

from comparison.models import ComparisonResult


# ==========================================================
# HELPERS
# ==========================================================

def _build_dataframe(result: ComparisonResult) -> pd.DataFrame:
    """
    Convert ConfigurationChange objects into DataFrame.
    """

    rows = []

    for change in result.changes:

        rows.append(
            {
                "Type": change.change_type.value,
                "Category": change.category.value,
                "Section": change.section,
                #"Line": change.line_number,
                "Risk": change.risk_level.value,
                #"Weight": change.risk_weight,
                #"Confidence": change.confidence_score,
                "Old Value": change.old_value,
                "New Value": change.new_value,
                "Description": change.description,
                "Recommendation": change.recommendation,
            }
        )

    return pd.DataFrame(rows)


# ==========================================================
# MAIN RENDERER
# ==========================================================

def render_changes(result: ComparisonResult):

    st.header("Configuration Changes")

    if not result.changes:

        st.success("No configuration changes detected.")

        return

    df = _build_dataframe(result)

    # ------------------------------------------------------
    # FILTERS
    # ------------------------------------------------------

    with st.container(border=True):

        st.subheader("Filters")

        col1, col2, col3 = st.columns(3)

        with col1:
            category = st.selectbox(
                "Category",
                ["All"] + sorted(df["Category"].unique().tolist())
            )

        with col2:
            risk = st.selectbox(
                "Risk",
                ["All"] + sorted(df["Risk"].unique().tolist())
            )

        with col3:
            change_type = st.selectbox(
                "Change Type",
                ["All"] + sorted(df["Type"].unique().tolist())
            )

        keyword = st.text_input(
            "Search Configuration"
        )

    # ------------------------------------------------------
    # APPLY FILTERS
    # ------------------------------------------------------

    filtered = df.copy()

    if category != "All":
        filtered = filtered[
            filtered["Category"] == category
        ]

    if risk != "All":
        filtered = filtered[
            filtered["Risk"] == risk
        ]

    if change_type != "All":
        filtered = filtered[
            filtered["Type"] == change_type
        ]

    if keyword.strip():

        mask = (
            filtered.astype(str)
            .apply(
                lambda c:
                c.str.contains(
                    keyword,
                    case=False,
                    na=False,
                )
            )
            .any(axis=1)
        )

        filtered = filtered[mask]

    st.write("")

    # ------------------------------------------------------
    # SUMMARY
    # ------------------------------------------------------

    with st.container(border=True):

        st.metric(
            "Detected Configuration Changes",
            len(filtered),
        )

    st.write("")

    # ------------------------------------------------------
    # TABLE
    # ------------------------------------------------------

    with st.container(border=True):

        st.subheader("Configuration Change Summary")

        st.dataframe(
            filtered,
            use_container_width=True,
            hide_index=True,
        )

    st.write("")

    # ------------------------------------------------------
    # DETAILS
    # ------------------------------------------------------

    st.subheader("Detailed Change Analysis")

    for index, row in filtered.iterrows():

        title = (
            f"{index + 1}. "
            f"{row['Type']} | "
            f"{row['Category']} | "
            f"{row['Risk']}"
        )

        with st.expander(title):

            c1, c2 = st.columns(2)

            c1.metric(
                "Risk",
                row["Risk"]
            )
            
            c2.metric(
                "Category",
                row["Category"]
            )

            st.markdown("### Section")

            st.code(row["Section"])

            if row["Old Value"]:

                st.markdown("### Previous Configuration")

                st.code(
                    row["Old Value"],
                    language="text",
                )

            if row["New Value"]:

                st.markdown("### Updated Configuration")

                st.code(
                    row["New Value"],
                    language="text",
                )

            st.markdown("### Description")

            st.info(row["Description"])

            st.markdown("### Recommendation")

            st.success(row["Recommendation"])

    # ------------------------------------------------------
    # METRICS
    # ------------------------------------------------------

    with st.container(border=True):

        st.subheader("Change Metrics")

        c1, c2, c3 = st.columns(3)

        c1.metric(
            "Added",
            (df["Type"] == "Added").sum(),
        )

        c2.metric(
            "Modified",
            (df["Type"] == "Modified").sum(),
        )

        c3.metric(
            "Removed",
            (df["Type"] == "Removed").sum(),
        )

    st.write("")

    # ------------------------------------------------------
    # FUTURE ENHANCEMENTS
    # ------------------------------------------------------

    with st.container(border=True):

        st.subheader("Phase 2 Roadmap")

        st.caption(
            "Reserved for AI-assisted change analysis."
        )

        st.markdown(
            """
Upcoming Features

- Semantic Diff Visualization
- Side-by-side Configuration Comparison
- AI-generated Change Explanation
- Similar Historical Changes
- Root Cause Suggestions
- Impact Prediction
- Automatic Rollback Recommendation
- Change Complexity Score
- SHAP Explainability
"""
        )

    st.divider()