"""
==========================================================
File : summary.py

ConfigVista AI

Executive Summary Panel

Author : Shivam Saxena
==========================================================
"""

from __future__ import annotations

import streamlit as st
from comparison.models import ComparisonResult


def render_summary(result: ComparisonResult):
    """
    Render executive summary.
    """

    st.header("Executive Summary")

    # ------------------------------------------------------
    # Device Information
    # ------------------------------------------------------

    with st.container(border=True):

        st.subheader("Device Information")

        c1, c2 = st.columns(2)

        with c1:
            st.metric(
                "Baseline Device",
                result.baseline_hostname
            )

        with c2:
            st.metric(
                "Candidate Device",
                result.candidate_hostname
            )

    st.write("")

    # ------------------------------------------------------
    # Change Summary
    # ------------------------------------------------------

    stats = result.statistics

    with st.container(border=True):

        st.subheader("Configuration Changes")

        c1, c2, c3, c4 = st.columns(4)

        c1.metric(
            "Total",
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

    # ------------------------------------------------------
    # Comparison Information
    # ------------------------------------------------------

    with st.container(border=True):

        st.subheader("Comparison Information")

        c1, c2, c3 = st.columns(3)

        c1.metric(
            "Execution Time",
            f"{result.comparison_time_ms:.2f} ms"
        )

        c2.metric(
            "Framework Version",
            result.comparison_version
        )

        c3.metric(
            "Device Role",
            result.device_role
        )

    st.write("")

    # ------------------------------------------------------
    # Executive Summary
    # ------------------------------------------------------

    with st.container(border=True):

        st.subheader("Assessment Summary")

        st.info(result.summary)

    st.write("")

    # ------------------------------------------------------
    # Future AI Panel
    # ------------------------------------------------------

    with st.container(border=True):

        st.subheader("AI Decision Panel (Phase 2)")

        st.caption(
            "Reserved for future AI-assisted deployment "
            "recommendations."
        )

        col1, col2 = st.columns(2)

        with col1:
            st.metric("Deployment Decision", "Coming Soon")

        with col2:
            st.metric("AI Confidence", "--")

        st.markdown(
            """
Future Enhancements

- AI Deployment Recommendation
- Change Complexity Score
- Deployment Confidence
- Similar Historical Changes
- Risk Justification
- CAB Recommendation
"""
        )

    st.divider()