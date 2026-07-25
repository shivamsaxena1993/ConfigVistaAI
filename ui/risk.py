"""
==========================================================
File : risk.py

ConfigVista AI

Risk Assessment Dashboard

Author : Shivam Saxena
==========================================================
"""

from __future__ import annotations


import streamlit as st

from comparison.models import (ComparisonResult, RiskLevel)


# ==========================================================
# Helpers
# ==========================================================


def _risk_banner(level: RiskLevel):

    if level == RiskLevel.HIGH:
        st.error("🔴 HIGH RISK DEPLOYMENT")

    elif level == RiskLevel.MEDIUM:
        st.warning("🟡 MEDIUM RISK DEPLOYMENT")

    elif level == RiskLevel.LOW:
        st.success("🟢 LOW RISK DEPLOYMENT")

    else:
        st.info("⚪ UNKNOWN RISK")


# ==========================================================
# Main Renderer
# ==========================================================

def render_risk(result: ComparisonResult):

    st.header("Risk Assessment")

    stats = result.statistics

    overall = result.overall_risk
    average = result.average_risk_score
    confidence = result.average_rule_confidence

    # ------------------------------------------------------

    with st.container(border=True):

        st.subheader("Overall Risk")

        c1, c2, c3 = st.columns(3)

        c1.metric(
            "Overall Risk",
            overall.value,
        )

        c2.metric(
            "Average Risk Score",
            f"{average}/100",
        )

        c3.metric(
            "Rule Confidence",
            f"{confidence} %",
        )

        st.progress(min(average / 100, 1.0))

        _risk_banner(overall)

    # ------------------------------------------------------

    with st.container(border=True):

        st.subheader("Risk Distribution")

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

    # ------------------------------------------------------

    with st.container(border=True):

        st.subheader("Deployment Recommendation")

        if overall == RiskLevel.HIGH:
            st.error(result.deployment_recommendation)
    
        elif overall == RiskLevel.MEDIUM:
            st.warning(result.deployment_recommendation)

        elif overall == RiskLevel.LOW:
            st.success(result.deployment_recommendation)

        else:
            st.info(result.deployment_recommendation)

    # ------------------------------------------------------

    with st.container(border=True):

        st.subheader("Risk Breakdown")

        rows = []

        for change in result.changes:

            rows.append(
                {
                    "Category": change.category.value,
                    "Risk": change.risk_level.value,
                    "Weight": change.risk_weight,
                    "Confidence": change.confidence_score,
                }
            )

        if rows:
            st.dataframe(
                rows,
                use_container_width=True,
                hide_index=True,
            )

    # ------------------------------------------------------

    with st.container(border=True):

        st.subheader("Phase 2 Enhancements")

        st.caption(
            "Reserved for AI-assisted risk prediction."
        )

        st.markdown(
            """
Upcoming Features

- ML Risk Prediction
- XGBoost Risk Score
- Random Forest Comparison
- SHAP Explainability
- Historical Similar Changes
- Change Complexity Index
- Deployment Success Probability
- CAB Recommendation
- Human-in-the-Loop Approval
"""
        )

    st.divider()