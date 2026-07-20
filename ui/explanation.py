"""
====================================================================
File: explanation.py

Project : ConfigVista AI

Purpose
-------
Displays Explainable AI results.

====================================================================
"""

import streamlit as st


def render_explanation(assessment):
    """
    Render AI explanations.
    """

    st.subheader("AI Explanation")

    explanations = assessment["risk"]["explanations"]

    for item in explanations:

        with st.expander(
            item["factor"],
            expanded=False
        ):

            col1, col2 = st.columns(2)

            col1.metric(
                "Impact",
                item["impact"]
            )

            col2.metric(
                "Contribution",
                f"+{item['score']}"
            )

            st.write(item["reason"])