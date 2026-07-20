"""
tests/test_comparison_engine.py

Integration Test for ConfigVista AI

Tests the complete pipeline:

Configuration Files
        │
        ▼
Comparison Engine
        │
        ▼
Diff Engine
        │
        ▼
Change Classifier
        │
        ▼
Risk Evaluator
        │
        ▼
Statistics
        │
        ▼
Report Generator

Author : Shivam Saxena
Project : ConfigVista AI
"""

from comparison.comparison_engine import ComparisonEngine
from comparison.report_generator import ReportGenerator
from comparison.models import RiskLevel


BASELINE = "comparison_examples/baseline.txt"
CANDIDATE = "comparison_examples/candidate2.txt"


def run_integration_test():

    print("=" * 70)
    print("Running ComparisonEngine Integration Test")
    print("=" * 70)

    # ------------------------------------------------------
    # Engine
    # ------------------------------------------------------

    engine = ComparisonEngine()

    result = engine.compare(
        BASELINE,
        CANDIDATE,
    )

    # ------------------------------------------------------
    # Basic Validation
    # ------------------------------------------------------

    assert result is not None

    assert result.baseline_hostname == "Branch-R1"

    assert result.candidate_hostname == "Branch-R2"

    assert len(result.changes) > 0

    print("✓ Configuration comparison completed")

    # ------------------------------------------------------
    # Statistics
    # ------------------------------------------------------

    stats = result.statistics

    assert stats.total_changes == len(result.changes)

    assert stats.added >= 0

    assert stats.modified >= 0

    assert stats.removed >= 0

    print("✓ Statistics validated")

    # ------------------------------------------------------
    # Risk Validation
    # ------------------------------------------------------

    high = [
        c
        for c in result.changes
        if c.risk_level == RiskLevel.HIGH
    ]

    medium = [
        c
        for c in result.changes
        if c.risk_level == RiskLevel.MEDIUM
    ]

    low = [
        c
        for c in result.changes
        if c.risk_level == RiskLevel.LOW
    ]

    assert (
        len(high)
        + len(medium)
        + len(low)
        <= len(result.changes)
    )

    print("✓ Risk evaluation validated")

    # ------------------------------------------------------
    # Category Summary
    # ------------------------------------------------------

    assert len(result.category_summary) > 0

    print("✓ Category summary validated")

    # ------------------------------------------------------
    # Report Generation
    # ------------------------------------------------------

    report_generator = ReportGenerator()

    text_report = report_generator.generate_text_report(
        result
    )

    markdown_report = report_generator.generate_markdown_report(
        result
    )

    html_report = report_generator.generate_html_report(
        result
    )

    json_report = report_generator.generate_json_string(
        result
    )

    assert len(text_report) > 0

    assert len(markdown_report) > 0

    assert len(html_report) > 0

    assert len(json_report) > 0

    print("✓ Report generation validated")

    # ------------------------------------------------------
    # Print Summary
    # ------------------------------------------------------

    print()

    print("=" * 70)
    print("Comparison Summary")
    print("=" * 70)

    print(result.summary)

    print()

    print(result.statistics)

    print()

    print("=" * 70)
    print("Generated Report")
    print("=" * 70)

    print(text_report)

    print("=" * 70)
    print("Integration Test PASSED")
    print("=" * 70)


if __name__ == "__main__":

    run_integration_test()