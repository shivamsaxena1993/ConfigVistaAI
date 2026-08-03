from __future__ import annotations

# ============================================================
# Imports
# ============================================================

from pathlib import Path
from datetime import UTC
from datetime import datetime

import json
import pandas as pd

from enterprise.models import FeatureVector


# ============================================================
# Dataset Exporter
# ============================================================

class DatasetExporter:
    """
    Exports FeatureVector objects into machine learning datasets.

    Responsibilities
    ----------------
    * Convert FeatureVector objects into pandas DataFrames.
    * Export datasets to CSV.
    * Validate exported datasets.
    * Provide export statistics.
    """

    # ========================================================
    # Constructor
    # ========================================================

    def __init__(self):
        """
        Initialize the exporter.
        """

        self.dataset: list[FeatureVector] = []

    # ========================================================
    # DataFrame Export
    # ========================================================

    def export_dataframe(
        self,
        features: list[FeatureVector],
    ) -> pd.DataFrame:
        """
        Convert FeatureVector objects into a pandas DataFrame.

        Parameters
        ----------
        features:
            Feature vectors produced by the FeatureGenerator.

        Returns
        -------
        pandas.DataFrame
            Machine-learning-ready dataset.
        """

        self.dataset = list(features)

        records = [

            feature.to_dict()

            for feature

            in self.dataset

        ]

        dataframe = pd.DataFrame(records)

        dataframe = dataframe.reindex(

            sorted(dataframe.columns),

            axis=1,

        )

        return dataframe
    
    # ========================================================
    # CSV Export
    # ========================================================

    def export_csv(
        self,
        features: list[FeatureVector],
        output_path: str | Path,
    ) -> pd.DataFrame:
        """
        Export feature vectors to a CSV file.

        Parameters
        ----------
        features:
            Feature vectors produced by the FeatureGenerator.

        output_path:
            Destination CSV file.

        Returns
        -------
        pandas.DataFrame
            Exported DataFrame.
        """

        dataframe = self.export_dataframe(
            features,
        )

        output_path = Path(
            output_path,
        )

        output_path.parent.mkdir(
            parents=True,
            exist_ok=True,
        )

        dataframe.to_csv(
            output_path,
            index=False,
        )

        return dataframe

    # ========================================================
    # Internal Helpers
    # ========================================================

    def _ensure_dataset_loaded(
        self,
    ):
        """
        Ensure that a dataset has been exported before
        generating additional artifacts.
        """

        if not self.dataset:

            raise ValueError(

                "No dataset available. Call export_dataframe() first."

            )
        
    # ========================================================
    # Metadata Export
    # ========================================================

    def export_metadata(
        self,
        output_path: str | Path,
    ) -> dict:
        """
        Export dataset metadata as JSON.

        Parameters
        ----------
        output_path:
            Destination metadata file.

        Returns
        -------
        dict
            Metadata dictionary.
        """

        self._ensure_dataset_loaded()

        stats = self.statistics()

        high_risk = sum(

            feature.predicted_risk == "High"

            for feature

            in self.dataset

        )

        medium_risk = sum(

            feature.predicted_risk == "Medium"

            for feature

            in self.dataset

        )

        low_risk = sum(

            feature.predicted_risk == "Low"

            for feature

            in self.dataset

        )

        metadata = {

            "dataset_name": "ConfigVista AI",

            "dataset_version": "1.0",

            "generated_at": datetime.now(
                UTC,
            ).isoformat(),

            "records": stats["records"],

            "features": stats["columns"],

            "target_column": "deployment_successful",

            "high_risk": high_risk,

            "medium_risk": medium_risk,

            "low_risk": low_risk,

            "successful": stats["successful"],

            "failed": stats["failed"],

            "average_risk": stats["average_risk"],

            "average_confidence": stats["average_confidence"],

        }

        output_path = Path(
            output_path,
        )

        output_path.parent.mkdir(

            parents=True,

            exist_ok=True,

        )

        with output_path.open(

            "w",

            encoding="utf-8",

        ) as file:

            json.dump(

                metadata,

                file,

                indent=4,

            )

        return metadata

    # ========================================================
    # Dataset Summary Export
    # ========================================================

    def export_summary(
        self,
        output_path: str | Path,
    ) -> str:
        """
        Export a human-readable dataset summary.

        Parameters
        ----------
        output_path:
            Destination summary file.

        Returns
        -------
        str
            Summary text.
        """

        self._ensure_dataset_loaded()

        output_path = Path(
            output_path,
        )

        metadata = self.export_metadata(

            output_path.parent
            / "metadata.json"

        )

        summary = f"""
==================================================
ConfigVista AI Dataset Summary
==================================================

Dataset Name         : {metadata["dataset_name"]}
Dataset Version      : {metadata["dataset_version"]}
Generated At         : {metadata["generated_at"]}

--------------------------------------------------

Total Records        : {metadata["records"]}
Total Features       : {metadata["features"]}

Prediction Target    : {metadata["target_column"]}

--------------------------------------------------

Risk Distribution

High                 : {metadata["high_risk"]}
Medium               : {metadata["medium_risk"]}
Low                  : {metadata["low_risk"]}

--------------------------------------------------

Deployment Outcomes

Successful           : {metadata["successful"]}
Failed               : {metadata["failed"]}

--------------------------------------------------

Average Risk Score   : {metadata["average_risk"]}
Average Confidence   : {metadata["average_confidence"]}

==================================================
""".strip()

        output_path.parent.mkdir(

            parents=True,

            exist_ok=True,

        )

        output_path.write_text(

            summary,

            encoding="utf-8",

        )

        return summary

    # ========================================================
    # Train / Validation / Test Export
    # ========================================================

    def export_train_validation_test_split(
        self,
        output_directory: str | Path,
        train_ratio: float = 0.70,
        validation_ratio: float = 0.15,
        test_ratio: float = 0.15,
        random_state: int = 42,
    ) -> dict[str, pd.DataFrame]:
        """
        Export deterministic train, validation and test datasets.

        Parameters
        ----------
        output_directory:
            Directory where split datasets will be written.

        train_ratio:
            Fraction of records assigned to the training dataset.

        validation_ratio:
            Fraction of records assigned to the validation dataset.

        test_ratio:
            Fraction of records assigned to the test dataset.

        random_state:
            Random seed used for deterministic shuffling.

        Returns
        -------
        dict[str, pandas.DataFrame]
            Dictionary containing the three datasets.
        """

        self._ensure_dataset_loaded()

        if round(

            train_ratio
            + validation_ratio
            + test_ratio,

            5,

        ) != 1.0:

            raise ValueError(

                "Split ratios must add up to 1.0."

            )

        dataframe = self.export_dataframe(

            self.dataset,

        )

        dataframe = dataframe.sample(

            frac=1,

            random_state=random_state,

        ).reset_index(

            drop=True,

        )

        total_records = len(

            dataframe,

        )

        train_end = int(

            total_records
            * train_ratio,

        )

        validation_end = train_end + int(

            total_records
            * validation_ratio,

        )

        train_df = dataframe.iloc[
            :train_end
        ]

        validation_df = dataframe.iloc[
            train_end:validation_end
        ]

        test_df = dataframe.iloc[
            validation_end:
        ]

        output_directory = Path(
            output_directory,
        )

        output_directory.mkdir(

            parents=True,

            exist_ok=True,

        )

        train_df.to_csv(

            output_directory / "train.csv",

            index=False,

        )

        validation_df.to_csv(

            output_directory / "validation.csv",

            index=False,

        )

        test_df.to_csv(

            output_directory / "test.csv",

            index=False,

        )

        return {

            "train": train_df,

            "validation": validation_df,

            "test": test_df,

        }
    
    # ========================================================
    # Manifest Export
    # ========================================================

    def export_manifest(
        self,
        output_path: str | Path,
    ) -> dict:
        """
        Export a manifest describing the generated dataset package.

        Parameters
        ----------
        output_path:
            Destination manifest JSON file.

        Returns
        -------
        dict
            Manifest dictionary.
        """

        self._ensure_dataset_loaded()

        output_path = Path(
            output_path,
        )

        output_path.parent.mkdir(

            parents=True,

            exist_ok=True,

        )

        metadata = self.export_metadata(

            output_path.parent
            / "metadata.json"

        )

        manifest = {

            "dataset_name": metadata["dataset_name"],

            "dataset_version": metadata["dataset_version"],

            "generated_at": metadata["generated_at"],

            "records": metadata["records"],

            "features": metadata["features"],

            "target_column": metadata["target_column"],

            "exports": {

                "dataset": "feature_dataset.csv",

                "metadata": "metadata.json",

                "summary": "dataset_summary.txt",

                "train": "train.csv",

                "validation": "validation.csv",

                "test": "test.csv",

            },

        }

        with output_path.open(

            "w",

            encoding="utf-8",

        ) as file:

            json.dump(

                manifest,

                file,

                indent=4,

            )

        return manifest
    
    # ========================================================
    # Statistics
    # ========================================================

    def statistics(
        self,
    ) -> dict:
        """
        Return dataset export statistics.
        """

        total_records = len(
            self.dataset,
        )

        successful = sum(

            feature.deployment_successful

            for feature

            in self.dataset

        )

        failed = (

            total_records

            - successful

        )

        if total_records:

            average_risk = round(

                sum(

                    feature.risk_score

                    for feature

                    in self.dataset

                )

                / total_records,

                2,

            )

            average_confidence = round(

                sum(

                    feature.confidence_score

                    for feature

                    in self.dataset

                )

                / total_records,

                2,

            )

        else:

            average_risk = 0.0

            average_confidence = 0.0

        return {

            "records": total_records,

            "columns": (

                len(
                    self.dataset[0].to_dict(),
                )

                if self.dataset

                else 0

            ),

            "successful": successful,

            "failed": failed,

            "average_risk": average_risk,

            "average_confidence": average_confidence,

        }
    # ========================================================
    # Dataset Validation
    # ========================================================

    def validate_dataset(
        self,
    ) -> bool:
        """
        Validate the exported dataset.

        Returns
        -------
        bool
            True if the dataset passes all validation checks.
        """

        if not self.dataset:

            return False

        feature_ids = {

            feature.feature_vector_id

            for feature

            in self.dataset

        }

        if len(feature_ids) != len(self.dataset):

            return False

        for feature in self.dataset:

            if not feature.feature_vector_id:

                return False

            if not feature.change_id:

                return False

            if not feature.device_id:

                return False

            if not feature.site_id:

                return False

            if not feature.business_service_id:

                return False

            if feature.deployment_successful is None:

                return False

        return True

    # ========================================================
    # Reset
    # ========================================================

    def reset(
        self,
    ):
        """
        Clear the exported dataset.
        """

        self.dataset.clear()

    # ========================================================
    # Length
    # ========================================================

    def __len__(
        self,
    ) -> int:
        """
        Return the number of exported records.
        """

        return len(
            self.dataset,
        )

    # ========================================================
    # Representation
    # ========================================================

    def __repr__(
        self,
    ) -> str:
        """
        String representation of the exporter.
        """

        stats = self.statistics()

        return (

            "DatasetExporter("

            f"records={stats['records']}, "

            f"successful={stats['successful']}, "

            f"failed={stats['failed']}, "

            f"avg_risk={stats['average_risk']:.2f}, "

            f"avg_confidence={stats['average_confidence']:.2f}"

            ")"

        )
    

