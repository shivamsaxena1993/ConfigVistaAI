"""
==========================================================
File : dashboard.py

ConfigVista AI

Shared Dashboard Components

Author : Shivam Saxena
==========================================================
"""

from __future__ import annotations

import streamlit as st

from comparison.models import (ComparisonResult,RiskLevel)


# ==========================================================
# PAGE HEADER
# ==========================================================

def render_header() -> None:
    """Render application title."""

    st.title("🛡️ ConfigVista AI")

    st.subheader(
        "Intelligent Network Configuration Comparison & "
        "Risk Assessment Framework"
    )

    st.divider()


# ==========================================================
# SIDEBAR
# ==========================================================

def render_sidebar():
    """
    Render sidebar and return uploaded files + run button.
    """

    st.sidebar.header("Configuration Files")

    baseline_file = st.sidebar.file_uploader(
        "Baseline Configuration",
        type=["txt", "cfg", "conf"],
    )

    candidate_file = st.sidebar.file_uploader(
        "Candidate Configuration",
        type=["txt", "cfg", "conf"],
    )

    run_button = st.sidebar.button(
        "Compare Configurations",
        use_container_width=True,
    )

    st.sidebar.divider()

    st.sidebar.markdown("### Workflow")

    st.sidebar.markdown(
        """
1. Upload Baseline

2. Upload Candidate

3. Compare Configurations

4. Review Risk Assessment

5. Download Reports
"""
    )

    st.sidebar.divider()

    st.sidebar.caption("ConfigVista AI")
    st.sidebar.caption("Version 2.2")

    return baseline_file, candidate_file, run_button


# ==========================================================
# HELPERS
# ==========================================================




# ==========================================================
# OVERVIEW
# ==========================================================

def render_overview(result: ComparisonResult):
    """
    Executive Overview Dashboard
    """

    st.header("Executive Overview")

    stats = result.statistics
    parser_stats = result.candidate_statistics or {}

    interface_count = parser_stats.get(
        "interfaces",
        len(result.candidate_interfaces),
    )

    validation_failures = parser_stats.get(
        "validation_failures",
        len(result.candidate_validation),
    )

    interfaces = max(
        parser_stats.get("interfaces",1),
        1
    )

    health_score = int(
        100 * (
            1 -
            validation_failures/interfaces
        )
    )

    health_score=max(
        health_score,
        60
    )

    overall_risk = result.overall_risk

    # ======================================================
    # Executive KPIs
    # ======================================================

    c1, c2, c3, c4 = st.columns(4)

    c1.metric(
        "Interfaces",
        interface_count,
    )

    c2.metric(
        "Configuration Changes",
        stats.total_changes,
    )

    c3.metric(
        "Overall Risk",
        overall_risk.value,
    )

    c4.metric(
        "Configuration Health",
        f"{health_score}%",
    )

    st.write("")

    # ======================================================
    # Configuration Information
    # ======================================================

    with st.container(border=True):

        st.subheader("Configuration Information")

        c1, c2 = st.columns(2)

        c1.metric(
            "Baseline Device",
            result.baseline_hostname,
        )

        c2.metric(
            "Candidate Device",
            result.candidate_hostname,
        )

    st.write("")

    # ======================================================
    # Parser Intelligence
    # ======================================================

    with st.container(border=True):

        st.subheader("Parser Intelligence")

        row1 = st.columns(4)

        row1[0].metric(
            "Interfaces",
            parser_stats.get("interfaces", 0),
        )

        row1[1].metric(
            "Physical",
            parser_stats.get("physical", 0),
        )

        row1[2].metric(
            "Routed",
            parser_stats.get("routed", 0),
        )

        row1[3].metric(
            "Switchports",
            parser_stats.get("switchports", 0),
        )

        row2 = st.columns(4)

        row2[0].metric(
            "Trunks",
            parser_stats.get("trunks", 0),
        )

        row2[1].metric(
            "Access Ports",
            parser_stats.get("access_ports", 0),
        )

        row2[2].metric(
            "QoS",
            parser_stats.get("qos_interfaces", 0),
        )

        row2[3].metric(
            "ACL",
            parser_stats.get("acl_interfaces", 0),
        )

        row3 = st.columns(4)

        row3[0].metric(
            "Loopbacks",
            parser_stats.get("loopbacks", 0),
        )

        row3[1].metric(
            "SVIs",
            parser_stats.get("svis", 0),
        )

        row3[2].metric(
            "Port-Channels",
            parser_stats.get("port_channels", 0),
        )

        row3[3].metric(
            "Tunnels",
            parser_stats.get("tunnels", 0),
        )

    st.write("")

    # ======================================================
    # Configuration Validation
    # ======================================================

    with st.container(border=True):

        st.subheader("Configuration Observations")

        c1, c2 = st.columns([1, 3])

        with c1:

            st.metric(
                "Validation Findings",
                validation_failures,
            )

            st.metric(
                "Health Score",
                f"{health_score}%",
            )

        with c2:

            st.progress(
                min(health_score / 100, 1.0)
            )

            validation = result.candidate_validation

            if not validation:
            
                st.success(
                    "No parser observations detected."
                )

            else:
            
                st.info(
                    f"{len(validation)} parser observations detected."
                )

                with st.expander(
                    "View Parser Observations"
                ):

                    for observation in validation:
                        st.info(observation)

    st.write("")

    # ======================================================
    # Risk Summary
    # ======================================================

    with st.container(border=True):

        st.subheader("Risk Summary")

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

    # ======================================================
    # Deployment Recommendation
    # ======================================================

    with st.container(border=True):

        st.subheader("Deployment Recommendation")
    
        if overall_risk == RiskLevel.HIGH:
            st.error(result.deployment_recommendation)
    
        elif overall_risk == RiskLevel.MEDIUM:
            st.warning(result.deployment_recommendation)
    
        elif overall_risk == RiskLevel.LOW:
            st.success(result.deployment_recommendation)
    
        else:
            st.info(result.deployment_recommendation)
    
        st.write("")

    # ======================================================
    # Executive Assessment
    # ======================================================

    with st.container(border=True):

        st.subheader("Executive Assessment")

        st.info(result.summary)

    st.write("")

    # ======================================================
    # Framework Information
    # ======================================================

    with st.container(border=True):

        st.subheader("Framework Information")

        c1, c2, c3, c4 = st.columns(4)

        c1.metric(
            "Execution Time",
            f"{result.comparison_time_ms:.2f} ms",
        )

        c2.metric(
            "Framework Version",
            result.comparison_version,
        )

        c3.metric(
            "Device Role",
            result.device_role,
        )

        c4.metric(
            "Parser Observations",
            validation_failures,
        )

    st.divider()


# ==========================================================
# FOOTER
# ==========================================================

def render_footer():
    """Footer."""

    st.divider()

    st.caption(
        "ConfigVista AI © 2026 | "
        "AI-Powered Network Configuration Comparison & Risk Assessment Platform"
    )