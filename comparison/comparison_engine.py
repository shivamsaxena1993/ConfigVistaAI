"""
comparison/comparison_engine.py

Main orchestration engine for the Configuration Comparison Framework.

Author : Shivam Saxena
Project : ConfigVista AI
"""

from __future__ import annotations

from parser.parsers.interface_parser import InterfaceParser
from comparison.csv_exporter import CSVExporter



import time
from pathlib import Path
from typing import List

from comparison.diff_engine import DiffEngine
from comparison.change_classifier import ChangeClassifier
from comparison.risk_evaluator import RiskEvaluator


from comparison.models import (
    ComparisonResult,
    calculate_statistics,
    build_category_summary,
)

from comparison.utils import (
    find_hostname,
    read_configuration,
)


class ComparisonEngine:
    """
    Main orchestration engine.

    Processing Pipeline

        Read Configuration
                │
                ▼
        Interface Parser
                │
                ▼
            Diff Engine
                │
                ▼
            Classifier
                │
                ▼
            Risk Evaluator
                │
                ▼
            Statistics
                │
                ▼
              Result
            """

    def __init__(self):

        self.diff_engine = DiffEngine()
        self.classifier = ChangeClassifier()
        self.risk_evaluator = RiskEvaluator()
    

        # Phase 3
        self.csv_exporter = CSVExporter()

    # ==========================================================

    def compare(
        self,
        baseline_file: str,
        candidate_file: str,
        export_csv: bool = False,
        csv_output_file: str = "ml/data/raw/comparison_results.csv",
    ) -> ComparisonResult:
        """
        Compare two configuration files.
        """

        start_time = time.perf_counter()

        baseline = read_configuration(baseline_file)
        candidate = read_configuration(candidate_file)


        result = self.compare_from_text(
            baseline,
            candidate,
            start_time=start_time,
        )

        if export_csv:
            self.csv_exporter.export(
                result=result,
                output_file=csv_output_file,
                append=True,
            )

        return result

    # ==========================================================

    def compare_from_text(
        self,
        baseline_lines: List[str],
        candidate_lines: List[str],
        start_time: float | None = None,
    ) -> ComparisonResult:
        """
        Compare already-loaded configuration lines.
        """

        if start_time is None:
            start_time = time.perf_counter()

        result = ComparisonResult()

        # ------------------------------------------------------
        # Hostnames
        # ------------------------------------------------------

        result.baseline_hostname = find_hostname(
            baseline_lines
        )

        result.candidate_hostname = find_hostname(
            candidate_lines
        )

        # --------------------------------------
        # Step 0 – Parse Configuration
        # --------------------------------------

        baseline_parser = InterfaceParser(
            baseline_lines
        )

        candidate_parser = InterfaceParser(
            candidate_lines
        )   

        baseline_interfaces = baseline_parser.parse()

        candidate_interfaces = candidate_parser.parse()

        result.baseline_interfaces = baseline_interfaces

        result.candidate_interfaces = candidate_interfaces

        result.baseline_statistics = (
            baseline_parser.statistics
        )

        result.candidate_statistics = (
            candidate_parser.statistics
        )

        result.baseline_validation = (
            baseline_parser.statistics.get(
                "validation_results",
                []
            )
        )

        result.candidate_validation = (
            candidate_parser.statistics.get(
                "validation_results",
                []
            )
        )

        

        # ------------------------------------------------------
        # Step 1 - Detect Differences
        # ------------------------------------------------------

        changes = self.diff_engine.compare(
            baseline_lines,
            candidate_lines,
        )

        # ------------------------------------------------------
        # Step 2 - Classify Changes
        # ------------------------------------------------------

        changes = self.classifier.classify(changes)

        # ------------------------------------------------------
        # Step 3 - Evaluate Risk
        # ------------------------------------------------------

        changes = self.risk_evaluator.evaluate(changes)

        result.changes = changes

        result.overall_risk = self.risk_evaluator.overall_risk(
            changes
        )

        result.average_risk_score = self.risk_evaluator.risk_score(
            changes
        )

        result.average_rule_confidence = (
            self.risk_evaluator.average_rule_confidence(changes)
        )

        result.deployment_recommendation = (
            self.risk_evaluator.deployment_recommendation(changes)
        )

        # ------------------------------------------------------
        # Step 4 - Statistics
        # ------------------------------------------------------

        calculate_statistics(result)

        build_category_summary(result)

        # ------------------------------------------------------
        # Step 5 - Generate Summary
        # ------------------------------------------------------

        result.summary = self._generate_summary(result)

        result.comparison_time_ms = round(
            (time.perf_counter() - start_time) * 1000,
            2,
        )

        return result

    # ==========================================================

    def compare_directory(
        self,
        baseline_directory: str,
        candidate_directory: str,
    ) -> List[ComparisonResult]:
        """
        Compare all matching configuration files in two directories.
        """

        baseline_path = Path(baseline_directory)
        candidate_path = Path(candidate_directory)

        if not baseline_path.exists():
            raise FileNotFoundError(
                baseline_directory
            )

        if not candidate_path.exists():
            raise FileNotFoundError(
                candidate_directory
            )

        results = []

        baseline_files = sorted(
            baseline_path.glob("*")
        )

        for baseline_file in baseline_files:

            candidate_file = (
                candidate_path / baseline_file.name
            )

            if candidate_file.exists():

                results.append(
                    self.compare(
                        str(baseline_file),
                        str(candidate_file),
                        export_csv=False,
                    )
                )

        return results

    # ==========================================================

    def _generate_summary(
        self,
        result: ComparisonResult,
    ) -> str:
        """
        Generate comparison summary.
        """

        stats = result.statistics


        lines = [
            "Configuration comparison completed successfully.",
            f"Baseline Device : {result.baseline_hostname}",
            f"Candidate Device : {result.candidate_hostname}",
            f"Interfaces Parsed : {len(result.candidate_interfaces)}",
            f"Configuration Changes : {stats.total_changes}",
            f"Overall Risk : {result.overall_risk.value}",
            f"Average Risk Score : {result.average_risk_score}/100",
            f"Average Rule Confidence : {result.average_rule_confidence}%",
            f"Recommendation : {result.deployment_recommendation}",
        ]

        return "\n".join(lines)