"""
Random Forest Trainer

Trains and evaluates the Random Forest model used by
ConfigVista AI for deployment success prediction.
"""

from __future__ import annotations

# ============================================================
# Imports
# ============================================================

from pathlib import Path

import joblib
import pandas as pd

from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import (

    accuracy_score,

    precision_score,

    recall_score,

    f1_score,

)


# ============================================================
# Random Forest Trainer
# ============================================================

class RandomForestTrainer:
    """
    Train and manage the Random Forest model.

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
        random_state: int = 42,
    ):
        """
        Initialize the trainer.
        """
        self.n_estimators = n_estimators

        self.random_state = random_state

        self.model_directory = Path(
            model_directory,
        )

        self.model_directory.mkdir(

            parents=True,

            exist_ok=True,

        )

        self.model = RandomForestClassifier(

            n_estimators=self.n_estimators,
        
            random_state=self.random_state,
        
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
        Train the Random Forest classifier.
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
    ) -> list[bool]:
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
        filename: str = "random_forest.pkl",
    ) -> Path:
        """
        Save the trained model.
        """

        if not self.is_trained:

            raise RuntimeError(
                "Model has not been trained.",
            )

        output_path = self.model_directory / filename

        joblib.dump(
            self.model,
            output_path,
        )

        return output_path

    def load_model(
        self,
        filename: str = "random_forest.pkl",
    ) -> None:
        """
        Load a trained model.
        """

        input_path = self.model_directory / filename

        if not input_path.exists():

            raise FileNotFoundError(
                input_path,
            )

        self.model = joblib.load(
            input_path,
        )

        self.is_trained = True

        # ========================================================
    # Training Summary
    # ========================================================

    def summary(
        self,
    ) -> dict:
        """
        Return a summary of the trained model.
        """

        return {

            "algorithm": "Random Forest",

            "trained": self.is_trained,

            "trees": self.model.n_estimators,

            "training_samples": self.training_samples,

            "features": len(self.feature_names),

            "random_state": self.random_state,

        }

    # ========================================================
    # Utilities
    # ========================================================

    def reset(
        self,
    ) -> None:
        """
        Reset the trainer to its initial state.
        """

        self.model = RandomForestClassifier(

            n_estimators=self.n_estimators,

            random_state=self.random_state,

        )

        self.is_trained = False

        self.training_samples = 0

        self.feature_names.clear()

    def __len__(
        self,
    ) -> int:
        """
        Return number of training samples.
        """

        return self.training_samples

    def __repr__(
        self,
    ) -> str:
        """
        String representation.
        """

        return (

            "RandomForestTrainer("

            f"trained={self.is_trained}, "

            f"trees={self.n_estimators}, "

            f"samples={self.training_samples}, "

            f"features={len(self.feature_names)}"

            ")"

        )