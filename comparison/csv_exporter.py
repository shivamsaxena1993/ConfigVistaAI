"""
comparison/csv_exporter.py

Exports comparison results into a structured CSV dataset.

This CSV serves as the raw input dataset for the
Machine Learning pipeline (Phase 3).

Author  : Shivam Saxena
Project : ConfigVista AI
"""

from __future__ import annotations

import uuid
from datetime import datetime
from pathlib import Path

import pandas as pd

from comparison.models import ComparisonResult
from pandas.errors import EmptyDataError


class CSVExporter:
    """
    Export ComparisonResult into CSV.

    One row represents one ConfigurationChange.
    """

    DEFAULT_COLUMNS = [
        "comparison_id",
        "timestamp",
        "baseline_hostname",
        "candidate_hostname",
        "category",
        "section",
        "change_type",
        "line_number",
        "old_value",
        "new_value",
        "risk_label",
        "risk_weight",
        "confidence_score",
        "description",
        "recommendation",
    ]

    def export(
        self,
        result: ComparisonResult,
        output_file: str,
        append: bool = True,
    ) -> Path:
        """
        Export comparison results to CSV.

        Parameters
        ----------
        result : ComparisonResult

        output_file : str

        append : bool
            True  -> append new comparison
            False -> overwrite existing CSV
        """

        rows = self._build_rows(result)

        df = pd.DataFrame(rows)

        output_path = Path(output_file)

        output_path.parent.mkdir(
            parents=True,
            exist_ok=True,
        )

        if append and output_path.exists():

            try:
                existing = pd.read_csv(output_path)

                df = pd.concat(
                    [existing, df],
                    ignore_index=True,
                )

            except EmptyDataError:
                # Existing file is empty; write the new dataframe only.
                pass

        df.to_csv(
            output_path,
            index=False,
        )

        return output_path

    # =====================================================

    def _build_rows(
        self,
        result: ComparisonResult,
    ) -> list[dict]:

        comparison_id = str(uuid.uuid4())

        timestamp = datetime.now().isoformat()

        rows = []

        for change in result.changes:

            rows.append(

                {

                    "comparison_id":
                        comparison_id,

                    "timestamp":
                        timestamp,

                    "baseline_hostname":
                        result.baseline_hostname,

                    "candidate_hostname":
                        result.candidate_hostname,

                    "category":
                        change.category.value,

                    "section":
                        change.section,

                    "change_type":
                        change.change_type.value,

                    "line_number":
                        change.line_number,

                    "old_value":
                        change.old_value,

                    "new_value":
                        change.new_value,

                    "risk_label":
                        change.risk_level.value,

                    "risk_weight":
                        change.risk_weight,

                    "confidence_score":
                        change.confidence_score,

                    "description":
                        change.description,

                    "recommendation":
                        change.recommendation,

                }

            )

        return rows

    # =====================================================

    @staticmethod
    def clear_dataset(
        output_file: str,
    ) -> None:
        """
        Create an empty dataset with headers.
        """

        df = pd.DataFrame(
            columns=CSVExporter.DEFAULT_COLUMNS
        )

        Path(output_file).parent.mkdir(
            parents=True,
            exist_ok=True,
        )

        df.to_csv(
            output_file,
            index=False,
        )