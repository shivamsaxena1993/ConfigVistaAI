"""
==========================================================
File : streamlit_app.py

ConfigVista AI

Main Application

Author : Shivam Saxena
==========================================================
"""

from __future__ import annotations

import tempfile

import streamlit as st

from comparison.comparison_engine import ComparisonEngine

from ui.dashboard import (
    render_header,
    render_sidebar,
    render_overview,
    render_footer,
)

from ui.summary import render_summary
from ui.risk import render_risk
from ui.category import render_category
from ui.changes import render_changes
from ui.details import render_details
from ui.downloads import render_downloads


# ==========================================================
# PAGE CONFIGURATION
# ==========================================================

st.set_page_config(
    page_title="ConfigVista AI",
    page_icon="🛡️",
    layout="wide",
)

# ==========================================================
# HEADER
# ==========================================================

render_header()

# ==========================================================
# SIDEBAR
# ==========================================================

baseline_file, candidate_file, run_button = render_sidebar()

# ==========================================================
# MAIN APPLICATION
# ==========================================================

if run_button:

    if baseline_file is None or candidate_file is None:

        st.warning(
            "Please upload both configuration files."
        )

        st.stop()

    with st.spinner("Analyzing configurations..."):

        # --------------------------------------------
        # Save uploaded files temporarily
        # --------------------------------------------

        with tempfile.NamedTemporaryFile(
            delete=False,
            suffix=".cfg",
        ) as base_tmp:

            base_tmp.write(
                baseline_file.getbuffer()
            )

            baseline_path = base_tmp.name

        with tempfile.NamedTemporaryFile(
            delete=False,
            suffix=".cfg",
        ) as cand_tmp:

            cand_tmp.write(
                candidate_file.getbuffer()
            )

            candidate_path = cand_tmp.name

        # --------------------------------------------
        # Run Comparison
        # --------------------------------------------

        engine = ComparisonEngine()

        result = engine.compare(
            baseline_path,
            candidate_path,
        )

    # =====================================================
    # DASHBOARD
    # =====================================================

    render_overview(result)

    # =====================================================
    # TABS
    # =====================================================

    tabs = st.tabs(
        [
            "📋 Summary",
            "⚠ Risk",
            "📊 Categories",
            "🔍 Changes",
            "📑 Details",
            "⬇ Reports",
        ]
    )

    with tabs[0]:
        render_summary(result)

    with tabs[1]:
        render_risk(result)

    with tabs[2]:
        render_category(result)

    with tabs[3]:
        render_changes(result)

    with tabs[4]:
        render_details(result)

    with tabs[5]:
        render_downloads(result)

else:

    st.info(
        """
Upload a Baseline Configuration and a Candidate
Configuration from the sidebar and click
**Compare Configurations** to begin.
"""
    )

# ==========================================================
# FOOTER
# ==========================================================

render_footer()