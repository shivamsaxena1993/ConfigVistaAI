"""
comparison/report_generator.py

Generates reports for ConfigVista AI.

Supported Formats
-----------------
- Plain Text
- Markdown
- HTML
- JSON

Author : Shivam Saxena
Project : ConfigVista AI
"""

from __future__ import annotations

import json
from html import escape

from comparison.models import ComparisonResult, ConfigurationChange


class ReportGenerator:

    # ==========================================================
    # TEXT REPORT
    # ==========================================================

    def generate_text_report(
        self,
        result: ComparisonResult,
    ) -> str:

        stats = result.statistics

        overall_risk = result.overall_risk.value

        avg_score = result.average_risk_score

        lines = []

        lines.append("=" * 70)
        lines.append("CONFIGURATION COMPARISON REPORT")
        lines.append("=" * 70)

        lines.append("")
        lines.append(f"Baseline Device  : {result.baseline_hostname}")
        lines.append(f"Candidate Device : {result.candidate_hostname}")

        lines.append("")
        lines.append("SUMMARY")
        lines.append("-" * 70)

        lines.append(f"Total Changes : {stats.total_changes}")
        lines.append(f"Added         : {stats.added}")
        lines.append(f"Removed       : {stats.removed}")
        lines.append(f"Modified      : {stats.modified}")

        lines.append("")

        lines.append(f"Overall Risk  : {overall_risk}")
        lines.append(f"Average Score : {avg_score}/100")

        lines.append(f"High Risk     : {stats.high_risk}")
        lines.append(f"Medium Risk   : {stats.medium_risk}")
        lines.append(f"Low Risk      : {stats.low_risk}")
        lines.append(
            f"Rule Confidence : {result.average_rule_confidence}%"
        )
        lines.append(
            f"Recommendation  : {result.deployment_recommendation}"
        )
        lines.append("")
        lines.append("CATEGORY SUMMARY")
        lines.append("-" * 70)

        for category in result.category_summary:

            lines.append(
                f"{category.category.value:<12}"
                f"{category.total_changes:>5} change(s)"
            )

        lines.append("")
        lines.append("CHANGE DETAILS")
        lines.append("-" * 70)

        for i, change in enumerate(result.changes, start=1):

            lines.extend(
                self._text_change(
                    i,
                    change,
                )
            )

        lines.append("")
        lines.append("=" * 70)

        return "\n".join(lines)

    # ==========================================================

    def _text_change(
        self,
        number: int,
        change: ConfigurationChange,
    ):

        block = []

        block.append(f"{number}. {change.change_type.value}")

        block.append(
            f"   Category      : {change.category.value}"
        )

        block.append(
            f"   Section       : {change.section}"
        )

        if change.line_number:

            block.append(
                f"   Line          : {change.line_number}"
            )

        if change.old_value:

            block.append(
                f"   Old           : {change.old_value}"
            )

        if change.new_value:

            block.append(
                f"   New           : {change.new_value}"
            )

        block.append(
            f"   Risk          : {change.risk_level.value}"
        )

        block.append(
            f"   Risk Weight   : {change.risk_weight}"
        )

        block.append(
            f"  Rule Confidence    : {change.confidence_score}%"
        )

        if change.description:

            block.append(
                f"   Details       : {change.description}"
            )

        if change.recommendation:

            block.append(
                f"   Deployment Recommendation: {change.recommendation}"
            )

        block.append("")

        return block

    # ==========================================================
    # MARKDOWN
    # ==========================================================

    def generate_markdown_report(
        self,
        result: ComparisonResult,
    ) -> str:

        md = []

        md.append("# Configuration Comparison Report")

        md.append("")
        md.append(f"**Baseline:** {result.baseline_hostname}")

        md.append(f"**Candidate:** {result.candidate_hostname}")

        md.append("")
        md.append("## Summary")

        s = result.statistics

        md.append(f"- Total Changes: {s.total_changes}")
        md.append(f"- Added: {s.added}")
        md.append(f"- Removed: {s.removed}")
        md.append(f"- Modified: {s.modified}")
        md.append(f"- High Risk: {s.high_risk}")
        md.append(f"- Medium Risk: {s.medium_risk}")
        md.append(f"- Low Risk: {s.low_risk}")

        md.append("")
        md.append("## Changes")

        for c in result.changes:

            md.append(
                f"### {c.change_type.value}"
            )

            md.append(f"- Category: {c.category.value}")
            md.append(f"- Section: {c.section}")
            md.append(f"- Risk: {c.risk_level.value}")
            md.append(f"- Rule Confidence: {c.confidence_score}%")

            if c.old_value:
                md.append(f"- Old: `{c.old_value}`")

            if c.new_value:
                md.append(f"- New: `{c.new_value}`")

            if c.recommendation:
                md.append(
                    f"- Recommendation: {c.recommendation}"
                )

            md.append("")

        return "\n".join(md)

    # ==========================================================
    # HTML
    # ==========================================================

    def generate_html_report(
        self,
        result: ComparisonResult,
    ) -> str:

        html = []

        html.append("<html><body>")

        html.append("<h1>Configuration Comparison Report</h1>")

        html.append(
            f"<p><b>Baseline:</b> {escape(result.baseline_hostname)}</p>"
        )

        html.append(
            f"<p><b>Candidate:</b> {escape(result.candidate_hostname)}</p>"
        )

        html.append("<h2>Changes</h2>")

        html.append(
            "<table border='1' cellpadding='5'>"
        )

        html.append(
            "<tr>"
            "<th>#</th>"
            "<th>Type</th>"
            "<th>Category</th>"
            "<th>Section</th>"
            "<th>Risk</th>"
            "<th>Rule Confidence</th>"
            "</tr>"
        )

        for i, c in enumerate(result.changes, start=1):

            html.append(
                "<tr>"
                f"<td>{i}</td>"
                f"<td>{escape(c.change_type.value)}</td>"
                f"<td>{escape(c.category.value)}</td>"
                f"<td>{escape(c.section)}</td>"
                f"<td>{escape(c.risk_level.value)}</td>"
                f"<td>{c.confidence_score}%</td>"
                "</tr>"
            )

        html.append("</table>")
        html.append("</body></html>")

        return "\n".join(html)

    # ==========================================================
    # JSON
    # ==========================================================

    def generate_json_report(
        self,
        result: ComparisonResult,
    ):

        return {

            "baseline": result.baseline_hostname,

            "candidate": result.candidate_hostname,

            "summary": result.summary,

            "statistics": vars(result.statistics),

            "changes": [

                {

                    "type": c.change_type.value,

                    "category": c.category.value,

                    "section": c.section,

                    "old_value": c.old_value,

                    "new_value": c.new_value,

                    "risk": c.risk_level.value,

                    "risk_weight": c.risk_weight,

                    "confidence": c.confidence_score,

                    "description": c.description,

                    "recommendation": c.recommendation,

                }

                for c in result.changes

            ],

        }

    # ==========================================================

    def generate_json_string(
        self,
        result: ComparisonResult,
    ) -> str:

        return json.dumps(
            self.generate_json_report(result),
            indent=4,
        )