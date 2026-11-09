"""Train and evaluate the fertilizer recommendation model from the local CSV."""
from pathlib import Path
import json
import pandas as pd
import joblib
from sklearn.compose import ColumnTransformer
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, balanced_accuracy_score, classification_report
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder, LabelEncoder

ROOT = Path(__file__).resolve().parents[1]
DATA_PATH = ROOT / "data" / "fertilizer_dataset.csv"
MODEL_DIR = ROOT / "saved_model"
TARGET = "Fertilizer Name"
CATEGORICAL = ["Soil Type", "Crop Type"]
NUMERIC = ["Temparature", "Humidity ", "Moisture", "Nitrogen", "Potassium", "Phosphorous"]
FEATURES = NUMERIC[:3] + CATEGORICAL + NUMERIC[3:]


def main():
    df = pd.read_csv(DATA_PATH)
    required = set(FEATURES + [TARGET])
    missing = sorted(required.difference(df.columns))
    if missing:
        raise ValueError(f"Dataset is missing columns: {missing}")
    df = df[FEATURES + [TARGET]].dropna().copy()
    if len(df) < 40:
        raise ValueError(f"Need at least 40 complete rows; found {len(df)}")
    class_counts = df[TARGET].value_counts()
    if class_counts.min() < 2:
        raise ValueError("Each fertilizer class needs at least two examples for a stratified holdout.")

    X = df[FEATURES]
    target_encoder = LabelEncoder()
    y = target_encoder.fit_transform(df[TARGET].astype(str))
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.25, random_state=42, stratify=y
    )
    preprocessor = ColumnTransformer([
        ("categorical", OneHotEncoder(handle_unknown="ignore"), CATEGORICAL),
        ("numeric", "passthrough", NUMERIC),
    ])
    pipeline = Pipeline([
        ("preprocess", preprocessor),
        ("classifier", RandomForestClassifier(
            n_estimators=300,
            min_samples_leaf=2,
            class_weight="balanced_subsample",
            random_state=42,
        )),
    ])
    pipeline.fit(X_train, y_train)
    predictions = pipeline.predict(X_test)
    accuracy = float(accuracy_score(y_test, predictions))
    balanced = float(balanced_accuracy_score(y_test, predictions))
    report = classification_report(
        y_test, predictions, labels=list(range(len(target_encoder.classes_))),
        target_names=[str(x) for x in target_encoder.classes_],
        output_dict=True, zero_division=0,
    )
    MODEL_DIR.mkdir(parents=True, exist_ok=True)
    joblib.dump(pipeline, MODEL_DIR / "fertilizer_pipeline.pkl")
    joblib.dump(target_encoder, MODEL_DIR / "fertilizer_encoder.pkl")
    metrics = {
        "rows_total": int(len(df)),
        "rows_train": int(len(X_train)),
        "rows_holdout": int(len(X_test)),
        "classes": {str(k): int(v) for k, v in class_counts.items()},
        "accuracy": accuracy,
        "balanced_accuracy": balanced,
        "classification_report": report,
        "note": "Small dataset; holdout metrics are noisy and are not evidence of field performance.",
    }
    (MODEL_DIR / "evaluation.json").write_text(json.dumps(metrics, indent=2), encoding="utf-8")
    print(f"Rows: {len(df)} (train {len(X_train)}, holdout {len(X_test)})")
    print(f"Holdout accuracy: {accuracy:.3f}")
    print(f"Holdout balanced accuracy: {balanced:.3f}")
    print("Class counts:", class_counts.to_dict())
    print("Saved model and evaluation to", MODEL_DIR)


if __name__ == "__main__":
    main()
