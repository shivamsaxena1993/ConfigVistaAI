"""
====================================================================
File: risk.py

Project : ConfigVista AI

Purpose
-------
Displays the Risk Assessment dashboard.

====================================================================
"""

import streamlit as st


def render_risk(assessment):
    """
    Render the Risk Assessment section.
    """

    risk = assessment["risk"]

    st.subheader("Risk Assessment")

    # ----------------------------------------------------------
    # Risk Metrics
    # ----------------------------------------------------------

    col1, col2, col3 = st.columns(3)

    col1.metric(
        "Risk Level",
        risk["risk_label"]
    )

    col2.metric(
        "Risk Score",
        f"{risk['risk_score']} / 100"
    )

    col3.metric(
        "Confidence",
        f"{risk['confidence_score']} %"
    )

    st.divider()

    # ----------------------------------------------------------
    # Progress Bar
    # ----------------------------------------------------------

    st.write("Overall Risk Score")

    st.progress(
        min(risk["risk_score"] / 100, 1.0)
    )

    # ----------------------------------------------------------
    # Risk Badge
    # ----------------------------------------------------------

    if risk["risk_label"] == "High":

        st.error(
            "🔴 HIGH RISK CHANGE"
        )

    elif risk["risk_label"] == "Medium":

        st.warning(
            "🟡 MEDIUM RISK CHANGE"
        )

    else:

        st.success(
            "🟢 LOW RISK CHANGE"
        )

    st.info(
        risk["summary"]
    )