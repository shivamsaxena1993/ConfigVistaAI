"""
====================================================================
File: streamlit_app.py

Project : ConfigVista AI

Purpose
-------
Main Streamlit Application

This file orchestrates the UI components.

====================================================================
"""

import os
import tempfile
import time

import streamlit as st

from services.assessment_service import AssessmentService

from ui.dashboard import (
    render_sidebar,
    render_header,
    render_dashboard
)

from ui.summary import render_summary
from ui.configuration import render_configuration
from ui.risk import render_risk
from ui.explanation import render_explanation
from ui.recommendation import render_recommendations
from ui.pipeline import render_pipeline
from ui.knowledgebase import render_knowledgebase



# ==========================================================
# PAGE CONFIGURATION
# ==========================================================

st.set_page_config(
    page_title="ConfigVista AI",
    page_icon="🛰️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ==========================================================
# HEADER & SIDEBAR
# ==========================================================

render_sidebar()

render_header()

render_dashboard()

# ==========================================================
# TABS
# ==========================================================

tab1, tab2 = st.tabs(
    [
        "🛰️ Run Assessment",
        "📚 AI Knowledge Base"
    ]
)

# ==========================================================
# TAB 1 - RUN ASSESSMENT
# ==========================================================

with tab1:

    st.subheader("Upload Cisco Configuration")

    uploaded_file = st.file_uploader(
        "Choose a Cisco IOS Configuration File",
        type=["txt", "cfg", "conf"]
    )

    if uploaded_file is not None:

        with tempfile.NamedTemporaryFile(
            delete=False,
            suffix=".txt"
        ) as temp:

            temp.write(uploaded_file.getvalue())
            temp_file = temp.name

        with st.spinner(
            "Running ConfigVista AI Assessment..."
        ):

            try:

                start = time.perf_counter()

                assessment = AssessmentService().run(temp_file)

                elapsed = time.perf_counter() - start

                st.success("Assessment Completed Successfully")
                st.caption(f"⏱️ Processing Time: {elapsed:.2f} seconds")

            except Exception as e:
            
                st.exception(e)
                st.stop()

            finally:
            
                if os.path.exists(temp_file):
                    os.remove(temp_file)

        st.success(
            "Assessment Completed Successfully"
        )

        st.divider()

        # ---------------------------------------
        # Assessment Summary
        # ---------------------------------------

        render_summary(assessment)

        st.divider()

        # ---------------------------------------
        # Configuration Overview
        # ---------------------------------------

        render_configuration(assessment)

        st.divider()

        # ---------------------------------------
        # Risk Assessment
        # ---------------------------------------

        render_risk(assessment)

        st.divider()

        # ---------------------------------------
        # Explainable AI
        # ---------------------------------------

        render_explanation(assessment)

        st.divider()

        # ---------------------------------------
        # Recommendations
        # ---------------------------------------

        render_recommendations(assessment)

        st.divider()

        # ---------------------------------------
        # Pipeline
        # ---------------------------------------

        render_pipeline()

# ==========================================================
# TAB 2 - AI KNOWLEDGE BASE
# ==========================================================

with tab2:

    render_knowledgebase()

# ==========================================================
# FOOTER
# ==========================================================

st.divider()

st.caption(
    "ConfigVista AI | Intelligent Network Change Risk Prediction & Decision Support Framework"
)

st.caption(
    "MSc Dissertation Prototype | Shivam Saxena | Version 1.0 MVP"
)