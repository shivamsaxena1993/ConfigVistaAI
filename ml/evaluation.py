"""
Evaluation Framework

Evaluates machine learning models used by ConfigVista AI
and generates reports for comparison.
"""

from __future__ import annotations

# ============================================================
# Imports
# ============================================================

import json

from pathlib import Path

import matplotlib.pyplot as plt

import pandas as pd

from sklearn.metrics import (

    accuracy_score,

    precision_score,

    recall_score,

    f1_score,

    roc_auc_score,

    confusion_matrix,

    ConfusionMatrixDisplay,

    classification_report,

)


# ============================================================
# Evaluation Framework
# ============================================================

class EvaluationFramework:
    """
    Evaluate trained ML models.
    """

    # ========================================================
    # Constructor
    # ========================================================

    def __init__(

        self,

        report_directory: str | Path = "ml/reports",

    ):

        self.report_directory = Path(

            report_directory,

        )

        self.report_directory.mkdir(

            parents=True,

            exist_ok=True,

        )

        self.metrics: dict = {}

        self.algorithm = ""

        self.last_report = None
    
        # ========================================================
    # Evaluation
    # ========================================================

    def evaluate(

        self,

        algorithm: str,

        y_true: pd.Series,

        predictions,

        probabilities,

    ) -> dict:
        """
        Evaluate a trained model.
        """

        self.algorithm = algorithm

        self.metrics = {

            "algorithm": algorithm,

            "accuracy": round(

                accuracy_score(

                    y_true,

                    predictions,

                ),

                4,

            ),

            "precision": round(

                precision_score(

                    y_true,

                    predictions,

                    zero_division=0,

                ),

                4,

            ),

            "recall": round(

                recall_score(

                    y_true,

                    predictions,

                    zero_division=0,

                ),

                4,

            ),

            "f1_score": round(

                f1_score(

                    y_true,

                    predictions,

                    zero_division=0,

                ),

                4,

            ),

            "roc_auc": round(

                roc_auc_score(

                    y_true,

                    [

                        probability[1]

                        for probability

                        in probabilities

                    ],

                ),

                4,

            ),

        }

        return self.metrics


    # ========================================================
    # Accessors
    # ========================================================

    def roc_auc(

        self,

    ) -> float:
        """
        Return the most recently computed ROC-AUC score.
        """

        if not self.metrics:

            raise RuntimeError(

                "No evaluation has been performed.",

            )

        return self.metrics[

            "roc_auc"

        ]

        # ========================================================
    # Confusion Matrix
    # ========================================================

    def confusion_matrix(

        self,

        y_true: pd.Series,

        predictions,

    ) -> Path:
        """
        Generate and save a confusion matrix.
        """

        matrix = confusion_matrix(

            y_true,

            predictions,

        )

        display = ConfusionMatrixDisplay(

            confusion_matrix=matrix,

        )

        display.plot()

        output_path = (

            self.report_directory

            /

            f"confusion_matrix_{self.algorithm.lower().replace(' ', '_')}.png"

        )

        plt.savefig(

            output_path,

            dpi=300,

            bbox_inches="tight",

        )

        plt.close()

        return output_path


    # ========================================================
    # Classification Report
    # ========================================================

    def classification_report(

        self,

        y_true: pd.Series,

        predictions,

    ) -> pd.DataFrame:
        """
        Generate and save a classification report.
        """

        report = classification_report(

            y_true,

            predictions,

            output_dict=True,

            zero_division=0,

        )

        dataframe = pd.DataFrame(

            report,

        ).transpose()

        output_path = (

            self.report_directory

            /

            f"classification_report_{self.algorithm.lower().replace(' ', '_')}.csv"

        )

        dataframe.to_csv(

            output_path,

            index=True,

        )

        self.last_report = dataframe

        return dataframe
    
        # ========================================================
    # Metrics Export
    # ========================================================

    def export_metrics(
        self,
    ) -> Path:
        """
        Export evaluation metrics to JSON.
        """

        if not self.metrics:

            raise RuntimeError(

                "No evaluation has been performed.",

            )

        output_path = (

            self.report_directory

            /

            f"{self.algorithm.lower().replace(' ', '_')}_metrics.json"

        )

        with output_path.open(

            "w",

            encoding="utf-8",

        ) as file:

            json.dump(

                self.metrics,

                file,

                indent=4,

            )

        return output_path


    # ========================================================
    # Feature Importance Export
    # ========================================================

    def export_feature_importance(
        self,
        importance: pd.DataFrame,
    ) -> Path:
        """
        Export feature importance to CSV.
        """

        output_path = (

            self.report_directory

            /

            f"feature_importance_{self.algorithm.lower().replace(' ', '_')}.csv"

        )

        importance.to_csv(

            output_path,

            index=False,

        )

        return output_path

    
