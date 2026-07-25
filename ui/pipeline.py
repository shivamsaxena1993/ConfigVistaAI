
"""
====================================================================
File: pipeline.py

Project : ConfigVista AI

Purpose
-------
Phase 1 Standardized Assessment Pipeline

This module preserves the existing functionality while presenting the
assessment workflow in a consistent, future-ready format.

Future phases will replace the static status indicators with live
execution tracking.

====================================================================
"""

import streamlit as st


PIPELINE_STEPS = [
    {
        "title": "Configuration Uploaded",
        "description": "Baseline and candidate configurations received."
    },
    {
        "title": "Configuration Parsed",
        "description": "Configuration syntax successfully parsed."
    },
    {
        "title": "Features Extracted",
        "description": "Networking and security features extracted."
    },
    {
        "title": "Risk Prediction Completed",
        "description": "Rule-based risk engine completed assessment."
    },
    {
        "title": "Recommendations Generated",
        "description": "Recommended mitigation actions generated."
    },
    {
        "title": "Assessment Stored",
        "description": "Assessment persisted into SQLite repository."
    },
    {
        "title": "Assessment Completed",
        "description": "Assessment workflow finished successfully."
    }
]


def render_pipeline():
    """Render the assessment pipeline."""

    st.subheader("Assessment Pipeline")

    with st.container(border=True):

        st.caption(
            "Current execution status of the ConfigVista AI assessment workflow."
        )

        for index, step in enumerate(PIPELINE_STEPS, start=1):

            with st.container(border=True):

                c1, c2 = st.columns([1, 6])

                with c1:
                    st.success(f"{index}")

                with c2:
                    st.markdown(f"**{step['title']}**")
                    st.caption(step["description"])

    with st.container(border=True):

        st.markdown("#### Pipeline Engine")

        c1, c2, c3 = st.columns(3)

        c1.metric("Workflow", "Completed")
        c2.metric("Execution", "Sequential")
        c3.metric("Current Engine", "Rule-Based")

        st.caption(
            "Future versions will support live execution progress, "
            "parallel processing, telemetry collection, and AI-assisted "
            "decision checkpoints."
        )

    with st.container(border=True):

        st.markdown("#### Reserved for Future Phases")

        st.markdown(
            '''
- Live Progress Timeline
- Animated Execution Status
- SSH Collection Status
- Feature Engineering Status
- ML Inference Status
- Human Approval Gate
- LangSmith Trace Status
- Audit Timeline
'''
        )

    st.divider()
