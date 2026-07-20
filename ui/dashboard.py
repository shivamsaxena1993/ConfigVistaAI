"""
====================================================================
File: dashboard.py

Project : ConfigVista AI

Purpose
-------
Dashboard Header, Sidebar and System Overview.

====================================================================
"""

import streamlit as st

from services.history_service import HistoryService


def render_sidebar():

    history = HistoryService()

    rows = history.get_all_assessments()

    total = len(rows)

    high = len(
        [r for r in rows if r.risk_label == "High"]
    )

    medium = len(
        [r for r in rows if r.risk_label == "Medium"]
    )

    low = len(
        [r for r in rows if r.risk_label == "Low"]
    )

    history.close()

    with st.sidebar:

        st.image(
            "https://img.icons8.com/fluency/96/artificial-intelligence.png",
            width=80
        )

        st.title("ConfigVista AI")

        st.caption(
            "MSc Dissertation Prototype"
        )

        st.divider()

        st.subheader("Project")

        st.write(
            "Network Change Risk Prediction & Decision Support"
        )

        st.divider()

        st.subheader("Current Implementation")

        st.markdown(
            """
- Risk Engine : Rule-Based
- Database : SQLite
- UI : Streamlit
- Parser : Cisco IOS
- Repository Pattern : Enabled
"""
        )

        st.divider()

        st.subheader("Assessment Statistics")

        st.metric(
            "Total Assessments",
            total
        )

        st.metric(
            "High Risk",
            high
        )

        st.metric(
            "Medium Risk",
            medium
        )

        st.metric(
            "Low Risk",
            low
        )

        st.divider()

        st.subheader("Roadmap")

        st.markdown(
            """
✅ Configuration Parser

✅ Feature Engineering

✅ Risk Prediction

✅ Recommendation Engine

⬜ Random Forest

⬜ XGBoost

⬜ LLM

⬜ RAG

⬜ Live SSH

⬜ LangSmith

⬜ Human Approval
"""
        )

        st.divider()

        st.caption(
            "Developed by Shivam Saxena"
        )


def render_header():

    st.title("🛰 ConfigVista AI")

    st.markdown(
        """
### Intelligent Network Change Risk Prediction &
### Decision Support Framework
"""
    )

    st.caption(
        "MSc Dissertation Prototype"
    )


def render_dashboard():

    history = HistoryService()

    rows = history.get_all_assessments()

    total = len(rows)

    high = len(
        [r for r in rows if r.risk_label == "High"]
    )

    medium = len(
        [r for r in rows if r.risk_label == "Medium"]
    )

    low = len(
        [r for r in rows if r.risk_label == "Low"]
    )

    history.close()

    st.subheader("System Overview")

    c1, c2, c3, c4 = st.columns(4)

    c1.metric(
        "Assessments",
        total
    )

    c2.metric(
        "High Risk",
        high
    )

    c3.metric(
        "Medium Risk",
        medium
    )

    c4.metric(
        "Low Risk",
        low
    )

    st.divider()