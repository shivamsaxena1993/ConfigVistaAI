"""
streamlit_app.py

ConfigVista AI
Intelligent Network Configuration Comparison &
Risk Assessment Framework

Author : Shivam Saxena
"""

from pathlib import Path
import tempfile

import pandas as pd
import streamlit as st

from comparison.comparison_engine import ComparisonEngine
from comparison.report_generator import ReportGenerator


# -------------------------------------------------------
# PAGE CONFIG
# -------------------------------------------------------

st.set_page_config(
    page_title="ConfigVista AI",
    page_icon="🛡️",
    layout="wide",
)

st.title("🛡️ ConfigVista AI")

st.subheader(
    "Intelligent Network Configuration Comparison & Risk Assessment Framework"
)

st.markdown("---")

# -------------------------------------------------------
# SIDEBAR
# -------------------------------------------------------

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

st.sidebar.markdown("---")

st.sidebar.info(
    """
Workflow

1. Upload Baseline

2. Upload Candidate

3. Compare

4. Review Risk

5. Download Report
"""
)

# -------------------------------------------------------
# MAIN
# -------------------------------------------------------

if run_button:

    if baseline_file is None or candidate_file is None:

        st.error("Please upload both configuration files.")

        st.stop()

    with st.spinner("Comparing configurations..."):

        with tempfile.TemporaryDirectory() as temp_dir:

            baseline_path = Path(temp_dir) / baseline_file.name
            candidate_path = Path(temp_dir) / candidate_file.name

            baseline_path.write_bytes(
                baseline_file.getvalue()
            )

            candidate_path.write_bytes(
                candidate_file.getvalue()
            )

            engine = ComparisonEngine()

            result = engine.compare(
                str(baseline_path),
                str(candidate_path),
            )

            report = ReportGenerator()

    st.success("Comparison completed successfully.")

    # ---------------------------------------------------
    # SUMMARY
    # ---------------------------------------------------

    st.header("Executive Summary")

    c1, c2, c3, c4 = st.columns(4)

    c1.metric(
        "Total Changes",
        result.statistics.total_changes,
    )

    c2.metric(
        "Added",
        result.statistics.added,
    )

    c3.metric(
        "Modified",
        result.statistics.modified,
    )

    c4.metric(
        "Removed",
        result.statistics.removed,
    )

    st.markdown("---")

    # ---------------------------------------------------
    # RISK
    # ---------------------------------------------------

    st.header("Risk Assessment")

    high = result.statistics.high_risk
    medium = result.statistics.medium_risk
    low = result.statistics.low_risk

    risk_score = (
        sum(c.risk_weight for c in result.changes)
        / len(result.changes)
        if result.changes
        else 0
    )

    col1, col2 = st.columns(2)

    with col1:

        st.metric(
            "Average Risk Score",
            f"{risk_score:.1f}/100",
        )

        st.progress(min(risk_score / 100, 1.0))

    with col2:

        st.metric("High Risk", high)

        st.metric("Medium Risk", medium)

        st.metric("Low Risk", low)

    st.markdown("---")

    # ---------------------------------------------------
    # CATEGORY SUMMARY
    # ---------------------------------------------------

    st.header("Category Summary")

    category_df = pd.DataFrame(
        [
            {
                "Category": item.category.value,
                "Changes": item.total_changes,
                "High": item.high_risk,
                "Medium": item.medium_risk,
                "Low": item.low_risk,
            }
            for item in result.category_summary
        ]
    )

    if not category_df.empty:
        st.dataframe(
            category_df,
            use_container_width=True,
            hide_index=True,
        )

    st.markdown("---")

    # ---------------------------------------------------
    # CHANGE DETAILS
    # ---------------------------------------------------

    st.header("Configuration Changes")

    rows = []

    for change in result.changes:

        rows.append(

            {

                "Type": change.change_type.value,

                "Category": change.category.value,

                "Section": change.section,

                "Old Value": change.old_value,

                "New Value": change.new_value,

                "Risk": change.risk_level.value,

                "Weight": change.risk_weight,

                "Confidence": change.confidence_score,

                "Recommendation": change.recommendation,

            }

        )

    change_df = pd.DataFrame(rows)

    st.dataframe(
        change_df,
        use_container_width=True,
        hide_index=True,
    )

    st.markdown("---")

    # ---------------------------------------------------
    # EXPANDABLE DETAILS
    # ---------------------------------------------------

    st.header("Detailed Analysis")

    for index, change in enumerate(result.changes, start=1):

        with st.expander(
            f"{index}. {change.change_type.value} | "
            f"{change.category.value} | "
            f"{change.risk_level.value}"
        ):

            st.write("### Section")

            st.code(change.section)

            if change.old_value:

                st.write("### Previous")

                st.code(change.old_value)

            if change.new_value:

                st.write("### Updated")

                st.code(change.new_value)

            st.write("### Description")

            st.write(change.description)

            st.write("### Recommendation")

            st.success(change.recommendation)

            st.write("### Confidence")

            st.progress(change.confidence_score / 100)

    st.markdown("---")

    # ---------------------------------------------------
    # DOWNLOADS
    # ---------------------------------------------------

    st.header("Download Reports")

    txt = report.generate_text_report(result)

    md = report.generate_markdown_report(result)

    html = report.generate_html_report(result)

    json_report = report.generate_json_string(result)

    d1, d2, d3, d4 = st.columns(4)

    with d1:

        st.download_button(
            "Download TXT",
            txt,
            file_name="comparison_report.txt",
        )

    with d2:

        st.download_button(
            "Download Markdown",
            md,
            file_name="comparison_report.md",
        )

    with d3:

        st.download_button(
            "Download HTML",
            html,
            file_name="comparison_report.html",
        )

    with d4:

        st.download_button(
            "Download JSON",
            json_report,
            file_name="comparison_report.json",
        )

else:

    st.info(
        "Upload a baseline and candidate configuration using the sidebar to begin the comparison."
    )

    st.markdown(
        """
### Features

- Configuration Difference Detection
- Context-Aware Change Classification
- Rule-Based Risk Assessment
- Category-Wise Analysis
- Confidence Score
- Executive Summary
- Multi-Format Report Generation
"""
    )

    st.markdown("---")

    st.caption("ConfigVista AI © 2026")