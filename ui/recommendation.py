"""
====================================================================
File: recommendation.py

Project : ConfigVista AI

Purpose
-------
Displays AI generated recommendations.

====================================================================
"""

import streamlit as st


def render_recommendations(assessment):
    """
    Render grouped recommendations.
    """

    recommendation = assessment["recommendation"]

    grouped = {}

    for rec in recommendation["recommendations"]:

        grouped.setdefault(
            rec["category"],
            []
        ).append(rec)

    st.subheader("Recommended Actions")

    for category, items in grouped.items():

        with st.expander(
            category,
            expanded=True
        ):

            for item in items:

                st.markdown(
                    f"### ✔ {item['action']}"
                )

                st.caption(
                    item["reason"]
                )