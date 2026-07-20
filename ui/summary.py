"""
====================================================================
File: summary.py

Project : ConfigVista AI

Purpose
-------
Displays the Assessment Summary section.

====================================================================
"""

import streamlit as st


def render_summary(assessment):

    risk = assessment["risk"]

    recommendation = assessment["recommendation"]

    col1, col2, col3, col4 = st.columns(4)

    col1.metric(
        "Assessment ID",
        assessment["change_reference"]
    )

    col2.metric(
        "Hostname",
        assessment["hostname"]
    )

    col3.metric(
        "Risk",
        risk["risk_label"]
    )

    col4.metric(
        "Priority",
        recommendation["priority"]
    )

    col1, col2 = st.columns(2)

    col1.metric(
        "Confidence",
        f"{risk['confidence_score']} %"
    )

    col2.metric(
        "Risk Score",
        f"{risk['risk_score']} / 100"
    )

    st.caption(
        f"Generated : {assessment['generated_at']}"
    )

    st.info(risk["summary"])