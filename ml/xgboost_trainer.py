"""
XGBoost Trainer

Trains and evaluates the XGBoost model used by
ConfigVista AI for deployment success prediction.
"""

from __future__ import annotations

# ============================================================
# Imports
# ============================================================

from pathlib import Path

import joblib
import pandas as pd

from xgboost import XGBClassifier

from sklearn.metrics import (

    accuracy_score,

    precision_score,

    recall_score,

    f1_score,

)


# ============================================================
# XGBoost Trainer
# ============================================================

class XGBoostTrainer:
    """
    Train and manage the XGBoost model.

    Responsibilities
    ----------------
    * Train the model.
    * Generate predictions.
    * Save/load the trained model.
    * Report training statistics.
    """

    # ========================================================
    # Constructor
    # ========================================================

    def __init__(
        self,
        model_directory: str | Path = "ml/trained_models",
        n_estimators: int = 300,
        max_depth: int = 6,
        learning_rate: float = 0.1,
        random_state: int = 42,
    ):

        self.model_directory = Path(
            model_directory,
        )

        self.model_directory.mkdir(
            parents=True,
            exist_ok=True,
        )

        self.n_estimators = n_estimators

        self.max_depth = max_depth

        self.learning_rate = learning_rate

        self.random_state = random_state

        self.model = XGBClassifier(

            n_estimators=self.n_estimators,

            max_depth=self.max_depth,

            learning_rate=self.learning_rate,

            subsample=0.8,

            colsample_bytree=0.8,

            random_state=self.random_state,

            eval_metric="logloss",

        )

        self.is_trained = False

        self.training_samples = 0

        self.feature_names: list[str] = []

        # ========================================================
    # Training
    # ========================================================

    def train(
        self,
        X_train: pd.DataFrame,
        y_train: pd.Series,
    ) -> None:
        """
        Train the XGBoost classifier.
        """

        self.model.fit(

            X_train,

            y_train,

        )

        self.is_trained = True

        self.training_samples = len(

            X_train,

        )

        self.feature_names = list(

            X_train.columns,

        )

    # ========================================================
    # Prediction
    # ========================================================

    def predict(
        self,
        X: pd.DataFrame,
    ) -> list[int]:
        """
        Predict deployment success.
        """

        if not self.is_trained:

            raise RuntimeError(

                "Model has not been trained.",

            )

        return self.model.predict(

            X,

        ).tolist()

    def predict_proba(
        self,
        X: pd.DataFrame,
    ) -> list[list[float]]:
        """
        Return prediction probabilities.
        """

        if not self.is_trained:

            raise RuntimeError(

                "Model has not been trained.",

            )

        return self.model.predict_proba(

            X,

        ).tolist()

        # ========================================================
    # Evaluation
    # ========================================================

    def evaluate(
        self,
        X: pd.DataFrame,
        y: pd.Series,
    ) -> dict:
        """
        Evaluate model performance.
        """

        predictions = self.model.predict(
            X,
        )

        return {

            "accuracy": round(
                accuracy_score(
                    y,
                    predictions,
                ),
                4,
            ),

            "precision": round(
                precision_score(
                    y,
                    predictions,
                    zero_division=0,
                ),
                4,
            ),

            "recall": round(
                recall_score(
                    y,
                    predictions,
                    zero_division=0,
                ),
                4,
            ),

            "f1_score": round(
                f1_score(
                    y,
                    predictions,
                    zero_division=0,
                ),
                4,
            ),

        }

    # ========================================================
    # Feature Importance
    # ========================================================

    def feature_importance(
        self,
    ) -> pd.DataFrame:
        """
        Return feature importance.
        """

        if not self.is_trained:

            raise RuntimeError(

                "Model has not been trained.",

            )

        dataframe = pd.DataFrame(

            {

                "feature": self.feature_names,

                "importance": self.model.feature_importances_,

            }

        )

        dataframe = dataframe.sort_values(

            by="importance",

            ascending=False,

        )

        dataframe.reset_index(

            drop=True,

            inplace=True,

        )

        return dataframe
    
        # ========================================================
    # Model Persistence
    # ========================================================

    def save_model(
        self,
        filename: str = "xgboost.pkl",
    ) -> Path:
        """
        Save the trained model.
        """

        if not self.is_trained:

            raise RuntimeError(

                "Model has not been trained.",

            )

        path = self.model_directory / filename

        joblib.dump(

            self.model,

            path,

        )

        return path

    def load_model(
        self,
        filename: str = "xgboost.pkl",
    ) -> None:
        """
        Load a trained model.
        """

        path = self.model_directory / filename

        if not path.exists():

            raise FileNotFoundError(

                path,

            )

        self.model = joblib.load(

            path,

        )

        self.is_trained = True


    # ========================================================
    # Utilities
    # ========================================================

    def summary(
        self,
    ) -> dict:
        """
        Return model summary.
        """

        return {

            "algorithm": "XGBoost",

            "trained": self.is_trained,

            "trees": self.n_estimators,

            "max_depth": self.max_depth,

            "learning_rate": self.learning_rate,

            "training_samples": self.training_samples,

            "features": len(

                self.feature_names,

            ),

            "random_state": self.random_state,

        }


    def reset(
        self,
    ) -> None:
        """
        Reset trainer.
        """

        self.model = XGBClassifier(

            n_estimators=self.n_estimators,

            max_depth=self.max_depth,

            learning_rate=self.learning_rate,

            subsample=0.8,

            colsample_bytree=0.8,

            random_state=self.random_state,

            eval_metric="logloss",

        )

        self.is_trained = False

        self.training_samples = 0

        self.feature_names.clear()


    def __len__(
        self,
    ) -> int:

        return self.training_samples


    def __repr__(
        self,
    ) -> str:

        return (

            f"XGBoostTrainer("

            f"trained={self.is_trained}, "

            f"trees={self.n_estimators}, "

            f"samples={self.training_samples}, "

            f"features={len(self.feature_names)})"

        )