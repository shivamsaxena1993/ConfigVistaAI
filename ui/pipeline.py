"""
====================================================================
File: pipeline.py

Project : ConfigVista AI

Purpose
-------
Displays Assessment Pipeline.

====================================================================
"""

import streamlit as st


def render_pipeline():
    """
    Render assessment pipeline.
    """

    st.subheader("Assessment Pipeline")

    steps = [

        "Configuration Uploaded",

        "Configuration Parsed",

        "Features Extracted",

        "Risk Prediction Completed",

        "Recommendations Generated",

        "Assessment Stored",

        "Assessment Completed"

    ]

    for step in steps:

        st.success(
            f"✅ {step}"
        )