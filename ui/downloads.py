"""
==========================================================
File : downloads.py

ConfigVista AI

Report Downloads

Author : Shivam Saxena
==========================================================
"""

from __future__ import annotations

from pathlib import Path

import streamlit as st

from comparison.models import ComparisonResult
from comparison.report_generator import ReportGenerator


# ==========================================================
# MAIN RENDERER
# ==========================================================

def render_downloads(result: ComparisonResult):

    st.header("Reports & Downloads")

    generator = ReportGenerator()

    # ------------------------------------------------------
    # Generate Reports
    # ------------------------------------------------------

    text_report = generator.generate_text_report(result)

    markdown_report = generator.generate_markdown_report(result)

    html_report = generator.generate_html_report(result)

    json_report = generator.generate_json_string(result)

    # ------------------------------------------------------

    with st.container(border=True):

        st.subheader("Report Downloads")

        col1, col2 = st.columns(2)

        with col1:

            st.download_button(
                label="📄 Download Text Report",
                data=text_report,
                file_name="comparison_report.txt",
                mime="text/plain",
                use_container_width=True,
            )

            st.download_button(
                label="📝 Download Markdown Report",
                data=markdown_report,
                file_name="comparison_report.md",
                mime="text/markdown",
                use_container_width=True,
            )

        with col2:

            st.download_button(
                label="🌐 Download HTML Report",
                data=html_report,
                file_name="comparison_report.html",
                mime="text/html",
                use_container_width=True,
            )

            st.download_button(
                label="📦 Download JSON Report",
                data=json_report,
                file_name="comparison_report.json",
                mime="application/json",
                use_container_width=True,
            )

    st.write("")


    # ------------------------------------------------------

    with st.container(border=True):

        st.subheader("Available Reports")
    
        st.success(
            "The following reports are ready for download."
        )
    
        st.markdown(
            """
    ### Executive Reports
    
    - 📄 Text Report
    
    - 📝 Markdown Report
    
    - 🌐 HTML Report
    
    - 📦 JSON Report
    
    These reports summarize the configuration comparison,
    risk assessment and detected configuration changes.
    """
        )
    
    st.divider()
