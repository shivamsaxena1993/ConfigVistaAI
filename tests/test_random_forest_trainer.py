"""
Unit tests for RandomForestTrainer.
"""

from ml.dataset_loader import DatasetLoader
from ml.feature_encoder import FeatureEncoder
from ml.random_forest_trainer import RandomForestTrainer

import pandas as pd
# ============================================================
# Test Helpers
# ============================================================

def build_environment():
    """
    Load the dataset.
    """

    loader = DatasetLoader()

    return loader.load_all()


def build_encoder():
    """
    Build and return an encoded dataset.
    """

    train, validation, test = build_environment()

    encoder = FeatureEncoder()

    encoder.encode(
        train,
        validation,
        test,
    )

    return encoder


def build_trainer():
    """
    Return a RandomForestTrainer instance.
    """

    return RandomForestTrainer()


# ============================================================
# Constructor
# ============================================================

def test_constructor():

    trainer = build_trainer()

    assert trainer.is_trained is False

    assert trainer.training_samples == 0

    assert trainer.n_estimators == 300

    assert trainer.random_state == 42

    assert trainer.feature_names == []


def test_model_directory_exists():

    trainer = build_trainer()

    assert trainer.model_directory.exists()

    assert trainer.model_directory.is_dir()

# ============================================================
# Training
# ============================================================

def test_train():

    encoder = build_encoder()

    trainer = build_trainer()

    trainer.train(

        encoder.X_train,

        encoder.y_train,

    )

    assert trainer.is_trained is True


def test_training_samples():

    encoder = build_encoder()

    trainer = build_trainer()

    trainer.train(

        encoder.X_train,

        encoder.y_train,

    )

    assert trainer.training_samples == 951


def test_feature_names():

    encoder = build_encoder()

    trainer = build_trainer()

    trainer.train(

        encoder.X_train,

        encoder.y_train,

    )

    assert len(

        trainer.feature_names,

    ) == 37

    assert (

        trainer.feature_names

        ==

        list(

            encoder.X_train.columns,

        )

    )


def test_model_type():

    trainer = build_trainer()

    assert (

        trainer.model.__class__.__name__

        ==

        "RandomForestClassifier"

    )

# ============================================================
# Prediction
# ============================================================

import pytest


def test_predict():

    encoder = build_encoder()

    trainer = build_trainer()

    trainer.train(

        encoder.X_train,

        encoder.y_train,

    )

    predictions = trainer.predict(

        encoder.X_test,

    )

    assert len(

        predictions,

    ) == len(

        encoder.X_test,

    )

    assert all(

        isinstance(

            prediction,

            int,

        )

        for prediction

        in predictions

    )

    assert set(

        predictions,

    ).issubset(

        {0, 1},

    )


def test_predict_before_training():

    encoder = build_encoder()

    trainer = build_trainer()

    with pytest.raises(

        RuntimeError,

    ):

        trainer.predict(

            encoder.X_test,

        )


def test_predict_proba():

    encoder = build_encoder()

    trainer = build_trainer()

    trainer.train(

        encoder.X_train,

        encoder.y_train,

    )

    probabilities = trainer.predict_proba(

        encoder.X_test,

    )

    assert len(

        probabilities,

    ) == len(

        encoder.X_test,

    )

    assert len(

        probabilities[0],

    ) == 2


def test_predict_proba_before_training():

    encoder = build_encoder()

    trainer = build_trainer()

    with pytest.raises(

        RuntimeError,

    ):

        trainer.predict_proba(

            encoder.X_test,

        )

# ============================================================
# Evaluation
# ============================================================

def test_evaluate():

    encoder = build_encoder()

    trainer = build_trainer()

    trainer.train(

        encoder.X_train,

        encoder.y_train,

    )

    metrics = trainer.evaluate(

        encoder.X_test,

        encoder.y_test,

    )

    assert isinstance(

        metrics,

        dict,

    )

    assert set(

        metrics.keys(),

    ) == {

        "accuracy",

        "precision",

        "recall",

        "f1_score",

    }


def test_evaluation_metric_ranges():

    encoder = build_encoder()

    trainer = build_trainer()

    trainer.train(

        encoder.X_train,

        encoder.y_train,

    )

    metrics = trainer.evaluate(

        encoder.X_test,

        encoder.y_test,

    )

    for value in metrics.values():

        assert 0.0 <= value <= 1.0


# ============================================================
# Feature Importance
# ============================================================

def test_feature_importance():

    encoder = build_encoder()

    trainer = build_trainer()

    trainer.train(

        encoder.X_train,

        encoder.y_train,

    )

    importance = trainer.feature_importance()

    assert isinstance(

        importance,

        pd.DataFrame,

    )

    assert len(

        importance,

    ) == 37


def test_feature_importance_columns():

    encoder = build_encoder()

    trainer = build_trainer()

    trainer.train(

        encoder.X_train,

        encoder.y_train,

    )

    importance = trainer.feature_importance()

    assert list(

        importance.columns,

    ) == [

        "feature",

        "importance",

    ]


def test_feature_importance_sorted():

    encoder = build_encoder()

    trainer = build_trainer()

    trainer.train(

        encoder.X_train,

        encoder.y_train,

    )

    importance = trainer.feature_importance()

    values = importance[

        "importance"

    ].tolist()

    assert values == sorted(

        values,

        reverse=True,

    )


def test_feature_importance_before_training():

    trainer = build_trainer()

    with pytest.raises(

        RuntimeError,

    ):

        trainer.feature_importance()

# ============================================================
# Model Persistence
# ============================================================

def test_save_model():

    encoder = build_encoder()

    trainer = build_trainer()

    trainer.train(

        encoder.X_train,

        encoder.y_train,

    )

    path = trainer.save_model()

    assert path.exists()

    assert path.name == "random_forest.pkl"


def test_load_model():

    encoder = build_encoder()

    trainer = build_trainer()

    trainer.train(

        encoder.X_train,

        encoder.y_train,

    )

    trainer.save_model()

    loaded = build_trainer()

    loaded.load_model()

    assert loaded.is_trained is True


def test_load_missing_model():

    trainer = build_trainer()

    with pytest.raises(

        FileNotFoundError,

    ):

        trainer.load_model(

            "does_not_exist.pkl",

        )


# ============================================================
# Summary
# ============================================================

def test_summary():

    encoder = build_encoder()

    trainer = build_trainer()

    trainer.train(

        encoder.X_train,

        encoder.y_train,

    )

    summary = trainer.summary()

    assert summary["algorithm"] == "Random Forest"

    assert summary["trained"] is True

    assert summary["trees"] == 300

    assert summary["training_samples"] == 951

    assert summary["features"] == 37

    assert summary["random_state"] == 42


# ============================================================
# Reset
# ============================================================

def test_reset():

    encoder = build_encoder()

    trainer = build_trainer()

    trainer.train(

        encoder.X_train,

        encoder.y_train,

    )

    trainer.reset()

    assert trainer.is_trained is False

    assert trainer.training_samples == 0

    assert trainer.feature_names == []


# ============================================================
# Magic Methods
# ============================================================

def test_len():

    encoder = build_encoder()

    trainer = build_trainer()

    trainer.train(

        encoder.X_train,

        encoder.y_train,

    )

    assert len(

        trainer,

    ) == 951


def test_repr():

    encoder = build_encoder()

    trainer = build_trainer()

    trainer.train(

        encoder.X_train,

        encoder.y_train,

    )

    representation = repr(

        trainer,

    )

    assert "RandomForestTrainer" in representation

    assert "trained=True" in representation

    assert "trees=300" in representation

    assert "samples=951" in representation

    assert "features=37" in representation