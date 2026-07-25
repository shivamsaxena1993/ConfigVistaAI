"""
==========================================================
File : details.py

ConfigVista AI

Comparison Details

Author : Shivam Saxena
==========================================================
"""

from __future__ import annotations

import streamlit as st

from comparison.models import ComparisonResult


# ==========================================================
# MAIN RENDERER
# ==========================================================

def render_details(result: ComparisonResult):

    st.header("Comparison Details")

    # ------------------------------------------------------

    with st.container(border=True):

        st.subheader("Comparison Information")

        c1, c2 = st.columns(2)

        with c1:

            st.text_input(
                "Baseline Hostname",
                value=result.baseline_hostname,
                disabled=True,
            )

            st.text_input(
                "Candidate Hostname",
                value=result.candidate_hostname,
                disabled=True,
            )

            st.text_input(
                "Device Role",
                value=result.device_role,
                disabled=True,
            )

        with c2:

            st.text_input(
                "Framework Version",
                value=result.comparison_version,
                disabled=True,
            )

            st.text_input(
                "Execution Time",
                value=f"{result.comparison_time_ms:.2f} ms",
                disabled=True,
            )

            st.text_input(
                "Total Changes",
                value=str(result.statistics.total_changes),
                disabled=True,
            )

    st.write("")

    # ------------------------------------------------------

    with st.container(border=True):

        st.subheader("Statistics")

        stats = result.statistics

        c1,c2,c3,c4 = st.columns(4)

        c1.metric(
            "Total Changes",
            stats.total_changes
        )
        
        c2.metric(
            "Added",
            stats.added
        )
        
        c3.metric(
            "Modified",
            stats.modified
        )
        
        c4.metric(
            "Removed",
            stats.removed
        )

        st.write("")

        c1, c2, c3 = st.columns(3)

        c1.metric(
            "High Risk",
            stats.high_risk,
        )

        c2.metric(
            "Medium Risk",
            stats.medium_risk,
        )

        c3.metric(
            "Low Risk",
            stats.low_risk,
        )

    st.write("")

    # ------------------------------------------------------

    with st.container(border=True):

        st.subheader("Comparison Summary")

        st.text_area(
            "",
            value=result.summary,
            height=180,
            disabled=True,
        )

    st.write("")

    # ------------------------------------------------------

    with st.container(border=True):

        st.subheader("Configuration Categories")

        if result.category_summary:

            for category in result.category_summary:

                with st.expander(category.category.value):

                    c1, c2 = st.columns(2)

                    with c1:

                        st.metric(
                            "Total Changes",
                            category.total_changes,
                        )

                        st.metric(
                            "High Risk",
                            category.high_risk,
                        )

                    with c2:

                        st.metric(
                            "Medium Risk",
                            category.medium_risk,
                        )

                        st.metric(
                            "Low Risk",
                            category.low_risk,
                        )

        else:

            st.info(
                "No category information available."
            )

    st.write("")

    # ------------------------------------------------------

    with st.container(border=True):

        st.subheader("Framework Information")

        st.markdown(
            """
### ConfigVista AI Processing Pipeline

✔ Configuration Parsing

✔ Difference Detection

✔ Semantic Classification

✔ Risk Evaluation

✔ Statistics Generation

✔ Category Aggregation

✔ Report Generation

---

### Future Enhancements

- AI Copilot
- XGBoost Risk Prediction
- SHAP Explainability
- Historical Change Correlation
- RAG Knowledge Base
- Deployment Recommendation Engine
"""
        )

    st.divider()