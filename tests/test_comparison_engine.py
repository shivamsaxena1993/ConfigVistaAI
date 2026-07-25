"""
tests/test_comparison_engine.py

Integration tests for the ConfigVista AI ComparisonEngine.

Validates the active Artifact-1 pipeline:

Configuration Files
        ↓
ComparisonEngine
        ↓
DiffEngine
        ↓
ChangeClassifier
        ↓
RiskEvaluator
        ↓
ComparisonResult
        ↓
ReportGenerator

Project: ConfigVista AI
"""

from pathlib import Path

import pytest

from comparison.comparison_engine import ComparisonEngine
from comparison.models import ComparisonResult, RiskLevel
from comparison.report_generator import ReportGenerator


PROJECT_ROOT = Path(__file__).resolve().parents[1]

BASELINE = PROJECT_ROOT / "comparison_examples" / "baseline.txt"
CANDIDATE = PROJECT_ROOT / "comparison_examples" / "candidate2.txt"


@pytest.fixture(scope="module")
def comparison_result() -> ComparisonResult:
    """Run the comparison once for this test module."""

    engine = ComparisonEngine()

    return engine.compare(
        str(BASELINE),
        str(CANDIDATE),
        export_csv=False,
    )


def test_comparison_returns_result(
    comparison_result: ComparisonResult,
):
    assert isinstance(comparison_result, ComparisonResult)


def test_device_identity(
    comparison_result: ComparisonResult,
):
    assert comparison_result.baseline_hostname
    assert comparison_result.candidate_hostname


def test_changes_detected(
    comparison_result: ComparisonResult,
):
    assert len(comparison_result.changes) > 0


def test_statistics_consistent(
    comparison_result: ComparisonResult,
):
    stats = comparison_result.statistics

    assert stats.total_changes == len(comparison_result.changes)

    assert (
        stats.added
        + stats.modified
        + stats.removed
        == stats.total_changes
    )


def test_risk_statistics_consistent(
    comparison_result: ComparisonResult,
):
    result = comparison_result
    stats = result.statistics

    classified_risk_count = (
        stats.high_risk
        + stats.medium_risk
        + stats.low_risk
    )

    assert classified_risk_count <= stats.total_changes

    assert result.overall_risk in {
        RiskLevel.LOW,
        RiskLevel.MEDIUM,
        RiskLevel.HIGH,
        RiskLevel.UNKNOWN,
    }

    assert 0.0 <= result.average_risk_score <= 100.0
    assert 0.0 <= result.average_rule_confidence <= 100.0


def test_category_summary_consistent(
    comparison_result: ComparisonResult,
):
    result = comparison_result

    assert result.category_summary

    assert (
        sum(item.total_changes for item in result.category_summary)
        == result.statistics.total_changes
    )


def test_deployment_recommendation_present(
    comparison_result: ComparisonResult,
):
    assert comparison_result.deployment_recommendation.strip()


def test_summary_contains_assessment(
    comparison_result: ComparisonResult,
):
    result = comparison_result

    assert "Configuration comparison completed successfully." in result.summary
    assert f"Overall Risk : {result.overall_risk.value}" in result.summary
    assert "Average Rule Confidence" in result.summary


def test_report_generation(
    comparison_result: ComparisonResult,
):
    generator = ReportGenerator()

    text_report = generator.generate_text_report(comparison_result)
    markdown_report = generator.generate_markdown_report(comparison_result)
    html_report = generator.generate_html_report(comparison_result)
    json_report = generator.generate_json_string(comparison_result)

    assert text_report.strip()
    assert markdown_report.strip()
    assert html_report.strip()
    assert json_report.strip()

    assert comparison_result.baseline_hostname in text_report
    assert comparison_result.candidate_hostname in text_report


def test_missing_configuration_raises_error():
    engine = ComparisonEngine()

    with pytest.raises(FileNotFoundError):
        engine.compare(
            "does-not-exist-baseline.cfg",
            "does-not-exist-candidate.cfg",
            export_csv=False,
        )