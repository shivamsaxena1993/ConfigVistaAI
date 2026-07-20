"""
====================================================================
File: knowledgebase.py

Project : ConfigVista AI

Purpose
-------
Displays historical assessments stored in SQLite.

====================================================================
"""

import pandas as pd
import streamlit as st

from services.history_service import HistoryService


def render_knowledgebase():
    """
    Render Assessment Repository.
    """

    history = HistoryService()

    rows = history.get_all_assessments()

    if not rows:

        st.info("No assessments found.")

        history.close()

        return

    data = []

    for row in rows:

        data.append({

            "Assessment ID": row.change_reference,

            "Risk": row.risk_label,

            "Confidence": row.confidence_score,

            "Status": row.change_status,

            "Created": row.created_at

        })

    st.subheader("Assessment Repository")

    st.dataframe(
        pd.DataFrame(data),
        use_container_width=True
    )

    selected = st.selectbox(

        "Select Assessment",

        rows,

        format_func=lambda x: x.change_reference

    )

    features = history.get_features(
        selected.change_id
    )

    recommendations = history.get_recommendations(
        selected.change_id
    )

    st.divider()

    st.subheader("Stored Features")

    st.json(features)

    st.subheader("Stored Recommendations")

    for rec in recommendations:

        with st.expander(rec.llm_summary):

            st.write(rec.recommendation_text)

            st.caption(rec.explanation)

    history.close()