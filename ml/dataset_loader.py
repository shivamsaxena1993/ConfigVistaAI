from __future__ import annotations

# ============================================================
# Imports
# ============================================================

import json

from pathlib import Path

import pandas as pd


# ============================================================
# Dataset Loader
# ============================================================

class DatasetLoader:
    """
    Loads and validates ConfigVista AI datasets.

    Responsibilities
    ----------------
    * Load train, validation and test datasets.
    * Load dataset metadata.
    * Load dataset manifest.
    * Validate dataset integrity.
    * Generate dataset statistics.
    * Produce dataset profile information.
    """

    # ========================================================
    # Constructor
    # ========================================================

    def __init__(
        self,
        dataset_directory: str | Path = "datasets/generated",
    ):
        """
        Initialize the dataset loader.

        Parameters
        ----------
        dataset_directory:
            Directory containing the exported datasets.
        """

        self.dataset_directory = Path(
            dataset_directory,
        )

        self.train_file = (
            self.dataset_directory
            / "train.csv"
        )

        self.validation_file = (
            self.dataset_directory
            / "validation.csv"
        )

        self.test_file = (
            self.dataset_directory
            / "test.csv"
        )

        self.metadata_file = (
            self.dataset_directory
            / "metadata.json"
        )

        self.manifest_file = (
            self.dataset_directory
            / "manifest.json"
        )

        self.train_df = pd.DataFrame()

        self.validation_df = pd.DataFrame()

        self.test_df = pd.DataFrame()

        self.metadata: dict = {}

        self.manifest: dict = {}

        # ========================================================
    # Dataset Loading
    # ========================================================

    def load_train(
        self,
    ) -> pd.DataFrame:
        """
        Load the training dataset.
        """

        self.train_df = pd.read_csv(
            self.train_file,
        )

        return self.train_df

    def load_validation(
        self,
    ) -> pd.DataFrame:
        """
        Load the validation dataset.
        """

        self.validation_df = pd.read_csv(
            self.validation_file,
        )

        return self.validation_df

    def load_test(
        self,
    ) -> pd.DataFrame:
        """
        Load the test dataset.
        """

        self.test_df = pd.read_csv(
            self.test_file,
        )

        return self.test_df
    
        # ========================================================
    # Package Loading
    # ========================================================

    def load_all(
        self,
    ) -> tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame]:
        """
        Load the complete dataset package.

        Returns
        -------
        tuple
            (train, validation, test)
        """

        return (

            self.load_train(),

            self.load_validation(),

            self.load_test(),

        )

    def load_metadata(
        self,
    ) -> dict:
        """
        Load dataset metadata.
        """

        with self.metadata_file.open(

            "r",

            encoding="utf-8",

        ) as file:

            self.metadata = json.load(

                file,

            )

        return self.metadata

    def load_manifest(
        self,
    ) -> dict:
        """
        Load dataset manifest.
        """

        with self.manifest_file.open(

            "r",

            encoding="utf-8",

        ) as file:

            self.manifest = json.load(

                file,

            )

        return self.manifest
    
        # ========================================================
    # Validation
    # ========================================================

    def validate(
        self,
    ) -> bool:
        """
        Validate that the dataset package has been loaded.
        """

        if self.train_df.empty:

            return False

        if self.validation_df.empty:

            return False

        if self.test_df.empty:

            return False

        if not self.metadata:

            return False

        if not self.manifest:

            return False

        return True

    # ========================================================
    # Statistics
    # ========================================================

    def statistics(
        self,
    ) -> dict:
        """
        Return dataset statistics.
        """

        return {

            "train_records": len(
                self.train_df,
            ),

            "validation_records": len(
                self.validation_df,
            ),

            "test_records": len(
                self.test_df,
            ),

            "total_records": (

                len(self.train_df)

                + len(self.validation_df)

                + len(self.test_df)

            ),

            "features": (

                len(self.train_df.columns)

                if not self.train_df.empty

                else 0

            ),

        }
    
        # ========================================================
    # Dataset Profile
    # ========================================================

    def profile(
        self,
    ) -> dict:
        """
        Generate a profile of the loaded dataset.

        Returns
        -------
        dict
            Dataset profile information.
        """

        if not self.validate():

            return {

                "train_records": 0,

                "validation_records": 0,

                "test_records": 0,

                "total_records": 0,

                "features": 0,

                "target_column": None,

                "missing_values": 0,

                "duplicate_rows": 0,

                "successful": 0,

                "failed": 0,

                "success_ratio": 0.0,

                "failure_ratio": 0.0,

            }

        dataset = pd.concat(

            [

                self.train_df,

                self.validation_df,

                self.test_df,

            ],

            ignore_index=True,

        )

        total_records = len(

            dataset,

        )

        missing_values = int(

            dataset.isna().sum().sum()

        )

        duplicate_rows = int(

            dataset.duplicated().sum()

        )

        target_column = self.metadata.get(

            "target_column",

            "deployment_successful",

        )

        successful = int(

            dataset[target_column].sum()

        )

        failed = (

            total_records

            - successful

        )

        success_ratio = round(

            (

                successful

                / total_records

                * 100

            )

            if total_records

            else 0,

            2,

        )

        failure_ratio = round(

            (

                failed

                / total_records

                * 100

            )

            if total_records

            else 0,

            2,

        )

        return {

            "train_records": len(

                self.train_df,

            ),

            "validation_records": len(

                self.validation_df,

            ),

            "test_records": len(

                self.test_df,

            ),

            "total_records": total_records,

            "features": len(

                dataset.columns,

            ),

            "target_column": target_column,

            "missing_values": missing_values,

            "duplicate_rows": duplicate_rows,

            "successful": successful,

            "failed": failed,

            "success_ratio": success_ratio,

            "failure_ratio": failure_ratio,

        }

    # ========================================================
    # Utility Methods
    # ========================================================

    def reset(
        self,
    ) -> None:
        """
        Reset loaded datasets.
        """

        self.train_df = pd.DataFrame()

        self.validation_df = pd.DataFrame()

        self.test_df = pd.DataFrame()

        self.metadata = {}

        self.manifest = {}

    def __len__(
        self,
    ) -> int:
        """
        Return total loaded records.
        """

        return (

            len(self.train_df)

            + len(self.validation_df)

            + len(self.test_df)

        )

    def __repr__(
        self,
    ) -> str:
        """
        Developer representation.
        """

        stats = self.statistics()

        return (

            "DatasetLoader("

            f"train={stats['train_records']}, "

            f"validation={stats['validation_records']}, "

            f"test={stats['test_records']}, "

            f"features={stats['features']})"

        )
    
