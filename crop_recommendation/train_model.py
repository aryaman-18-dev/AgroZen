"""Train and activate the crop recommendation model from the bundled dataset."""

from __future__ import annotations

from datetime import datetime, timezone
from pathlib import Path
import sys

import joblib
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, f1_score
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder

PROJECT_ROOT = Path(__file__).resolve().parents[1]
DATA_PATH = Path(__file__).resolve().parent / "Crop_recommendation.csv"
sys.path.insert(0, str(PROJECT_ROOT))

from backend.ml_models import ModelType, get_model_manager

FEATURES = ["N", "P", "K", "temperature", "humidity", "ph", "rainfall"]
MODEL_NAME = "crop_recommendation"
MODEL_VERSION = "v1.1.0"


def train_and_activate() -> str:
    if not DATA_PATH.is_file():
        raise FileNotFoundError(f"Crop training dataset not found: {DATA_PATH}")

    data = pd.read_csv(DATA_PATH)
    missing = [column for column in [*FEATURES, "label"] if column not in data.columns]
    if missing:
        raise ValueError(f"Crop dataset is missing required columns: {missing}")

    data = data.dropna(subset=[*FEATURES, "label"])
    features = data[FEATURES].astype(float)
    encoder = LabelEncoder()
    labels = encoder.fit_transform(data["label"].astype(str))

    x_train, x_valid, y_train, y_valid = train_test_split(
        features,
        labels,
        test_size=0.2,
        random_state=42,
        stratify=labels,
    )
    validation_model = RandomForestClassifier(n_estimators=100, random_state=42, n_jobs=-1)
    validation_model.fit(x_train, y_train)
    accuracy = accuracy_score(y_valid, validation_model.predict(x_valid))
    weighted_f1 = f1_score(y_valid, validation_model.predict(x_valid), average="weighted")

    # Refit on all available examples after recording holdout metrics.
    model = RandomForestClassifier(n_estimators=100, random_state=42, n_jobs=-1)
    model.fit(features, labels)

    manager = get_model_manager()
    if not manager.create_version(
        MODEL_NAME,
        model,
        MODEL_VERSION,
        ModelType.SKLEARN,
        metadata={
            "training_date": datetime.now(timezone.utc).isoformat(),
            "training_samples": len(data),
            "validation_samples": len(y_valid),
            "features_used": FEATURES,
            "metrics": {"accuracy": float(accuracy), "f1_score_weighted": float(weighted_f1)},
            "scikit_learn_version": __import__("sklearn").__version__,
            "source_dataset": str(DATA_PATH.relative_to(PROJECT_ROOT)),
        },
        artifacts={"label_encoder": encoder},
        description="Retrained from the bundled crop recommendation dataset",
    ):
        raise RuntimeError(f"Could not save {MODEL_NAME}/{MODEL_VERSION}")

    if not manager.set_active_version(MODEL_NAME, MODEL_VERSION):
        raise RuntimeError(f"Could not activate {MODEL_NAME}/{MODEL_VERSION}")

    # Keep legacy model files in sync for older standalone routes/scripts.
    legacy_model_dir = Path(__file__).resolve().parent / "model"
    legacy_model_dir.mkdir(parents=True, exist_ok=True)
    joblib.dump(model, legacy_model_dir / "rf_model.pkl")
    joblib.dump(encoder, legacy_model_dir / "label_encoder.pkl")

    print(f"Activated {MODEL_NAME}/{MODEL_VERSION}")
    print(f"Training rows: {len(data)}; validation accuracy: {accuracy:.4f}; weighted F1: {weighted_f1:.4f}")
    return MODEL_VERSION


if __name__ == "__main__":
    train_and_activate()
