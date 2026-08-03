from __future__ import annotations

# ============================================================
# Imports
# ============================================================

from pathlib import Path

import joblib

import pandas as pd

from sklearn.preprocessing import LabelEncoder

from pandas.api.types import (

    is_bool_dtype,

    is_numeric_dtype,

)


# ============================================================
# Feature Encoder
# ============================================================

class FeatureEncoder:
    """
    Encodes ConfigVista AI datasets for machine learning.

    Responsibilities
    ----------------
    * Separate features and target.
    * Encode categorical features.
    * Preserve feature names.
    * Save and load encoders.
    """

    # ========================================================
    # Constructor
    # ========================================================

    def __init__(
        self,
        model_directory: str | Path = "ml/trained_models",
    ):
        """
        Initialize the feature encoder.
        """

        self.model_directory = Path(
            model_directory,
        )

        self.model_directory.mkdir(

            parents=True,

            exist_ok=True,

        )

        self.label_encoders: dict[str, LabelEncoder] = {}

        self.feature_names: list[str] = []

        self.target_column = "deployment_successful"

        self.X_train = pd.DataFrame()

        self.y_train = pd.Series(
            dtype=int,
        )

        self.X_validation = pd.DataFrame()

        self.y_validation = pd.Series(
            dtype=int,
        )

        self.X_test = pd.DataFrame()

        self.y_test = pd.Series(
            dtype=int,
        )

        self.excluded_columns = (

            "feature_vector_id",

            "change_id",

            "device_id",

            "site_id",

            "business_service_id",

            "created_at",

            "updated_at",

        )

    # ========================================================
    # Feature / Target Separation
    # ========================================================

    def split_features_and_target(
        self,
        train_df: pd.DataFrame,
        validation_df: pd.DataFrame,
        test_df: pd.DataFrame,
    ) -> None:
        """
        Separate feature columns from the prediction target.
        """

        self.X_train = train_df.drop(

            columns=[

                self.target_column,

            ],

        )

        self.y_train = train_df[

            self.target_column

        ].astype(

            int,

        )

        self.X_validation = validation_df.drop(

            columns=[

                self.target_column,

            ],

        )

        self.y_validation = validation_df[

            self.target_column

        ].astype(

            int,

        )

        self.X_test = test_df.drop(

            columns=[

                self.target_column,

            ],

        )

        self.y_test = test_df[

            self.target_column

        ].astype(

            int,

        )

        self.feature_names = list(

            self.X_train.columns,

        )

    # ========================================================
    # Feature Discovery
    # ========================================================

    def _get_categorical_columns(
        self,
    ) -> list[str]:
        """
        Return categorical feature columns.
        """

        categorical_columns = []

        for column in self.X_train.columns:

            if is_numeric_dtype(
                self.X_train[column],
            ):
                continue

            if is_bool_dtype(
                self.X_train[column],
            ):
                continue

            categorical_columns.append(
                column,
            )

        return categorical_columns
    
    # ========================================================
    # Feature Selection
    # ========================================================

    def _drop_excluded_columns(
        self,
    ) -> None:
        """
        Remove non-predictive columns from all datasets.
        """

        columns = [

            column

            for column

            in self.excluded_columns

            if column in self.X_train.columns

        ]

        self.X_train = self.X_train.drop(
            columns=columns,
        )

        self.X_validation = self.X_validation.drop(
            columns=columns,
        )

        self.X_test = self.X_test.drop(
            columns=columns,
        )

        self.feature_names = list(
            self.X_train.columns,
        )

    # ========================================================
    # Encoding
    # ========================================================

    def fit_encoders(
        self,
    ) -> None:
        """
        Fit label encoders using the training dataset.
        """

        categorical_columns = self._get_categorical_columns()

        self.label_encoders.clear()

        for column in categorical_columns:

            encoder = LabelEncoder()

            encoder.fit(

                self.X_train[column].astype(str),

            )

            self.label_encoders[column] = encoder
    
    def transform(
            self,
        ) -> None:
            """
            Apply fitted encoders to all datasets.
            """

            for column, encoder in self.label_encoders.items():

                self.X_train[column] = encoder.transform(

                    self.X_train[column].astype(str),

                )

                self.X_validation[column] = encoder.transform(

                    self.X_validation[column].astype(str),

                )

                self.X_test[column] = encoder.transform(

                    self.X_test[column].astype(str),

                )
        
    def encode(
        self,
        train_df: pd.DataFrame,
        validation_df: pd.DataFrame,
        test_df: pd.DataFrame,
    ) -> None:
        """
        Complete feature encoding pipeline.
        """

        self.split_features_and_target(

            train_df,

            validation_df,

            test_df,

        )

        self._drop_excluded_columns()

        self.fit_encoders()

        self.transform()

        self.feature_names = list(

            self.X_train.columns,

        )
    # ========================================================
    # Persistence
    # ========================================================

    def save_encoders(
        self,
    ) -> None:
        """
        Save fitted label encoders.
        """

        for column, encoder in self.label_encoders.items():

            joblib.dump(

                encoder,

                self.model_directory / f"{column}_encoder.pkl",

            )
    
    def load_encoders(
        self,
    ) -> None:
        """
        Load previously saved encoders.
        """

        self.label_encoders.clear()

        for file in sorted(
            self.model_directory.glob("*_encoder.pkl")
        ):

            column = file.stem.replace(

                "_encoder",

                "",

            )

            self.label_encoders[column] = joblib.load(

                file,

            )
    
