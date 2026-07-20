"""
comparison/comparison_engine.py

Main orchestration engine for the Configuration Comparison Framework.

Author : Shivam Saxena
Project : ConfigVista AI
"""

from __future__ import annotations

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
        Result
    """

    def __init__(self):

        self.diff_engine = DiffEngine()
        self.classifier = ChangeClassifier()
        self.risk_evaluator = RiskEvaluator()

    # ==========================================================

    def compare(
        self,
        baseline_file: str,
        candidate_file: str,
    ) -> ComparisonResult:
        """
        Compare two configuration files.
        """

        start_time = time.perf_counter()

        baseline = read_configuration(baseline_file)
        candidate = read_configuration(candidate_file)

        return self.compare_from_text(
            baseline,
            candidate,
            start_time=start_time,
        )

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

        # ------------------------------------------------------
        # Step 4 - Statistics
        # ------------------------------------------------------

        calculate_statistics(result)

        build_category_summary(result)

        # ------------------------------------------------------
        # Summary
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

        overall_risk = self.risk_evaluator.overall_risk(
            result.changes
        )

        average_risk = self.risk_evaluator.risk_score(
            result.changes
        )

        lines = [

            f"{stats.total_changes} configuration change(s) detected.",

            f"Overall Risk : {overall_risk.value}",

            f"Average Risk Score : {average_risk}/100",

            f"Added : {stats.added}",

            f"Removed : {stats.removed}",

            f"Modified : {stats.modified}",

        ]

        return "\n".join(lines)