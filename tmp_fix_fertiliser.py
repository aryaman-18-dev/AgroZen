from pathlib import Path

base = Path('Fertiliser Recommendation System')
(base/'src'/'model.py').write_text('''"""Load the fertilizer recommendation pipeline trained by src/train.py."""
from pathlib import Path
import joblib
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
MODEL_DIR = ROOT / "saved_model"
PIPELINE_PATH = MODEL_DIR / "fertilizer_pipeline.pkl"
TARGET_ENCODER_PATH = MODEL_DIR / "fertilizer_encoder.pkl"

model = None
target_encoder = None
load_error = None
try:
    model = joblib.load(PIPELINE_PATH)
    target_encoder = joblib.load(TARGET_ENCODER_PATH)
except FileNotFoundError as exc:
    load_error = f"Trained model files are missing. Run `{Path(__file__).parent / 'train.py'}` first. ({exc})"

FEATURES = [
    "Temparature", "Humidity ", "Moisture", "Soil Type", "Crop Type",
    "Nitrogen", "Potassium", "Phosphorous",
]


def predict_fertilizer(temparature, humidity, moisture, soil_type, crop_type,
                       nitrogen, potassium, phosphorous):
    """Return a preliminary class prediction and its uncalibrated model score."""
    if model is None or target_encoder is None:
        raise RuntimeError(load_error or "Fertilizer model is not loaded.")

    row = pd.DataFrame([{
        "Temparature": float(temparature),
        "Humidity ": float(humidity),
        "Moisture": float(moisture),
        "Soil Type": str(soil_type),
        "Crop Type": str(crop_type),
        "Nitrogen": float(nitrogen),
        "Potassium": float(potassium),
        "Phosphorous": float(phosphorous),
    }], columns=FEATURES)
    try:
        encoded_prediction = int(model.predict(row)[0])
        score = float(model.predict_proba(row).max())
        recommendation = str(target_encoder.inverse_transform([encoded_prediction])[0])
    except ValueError as exc:
        raise ValueError(f"Unsupported input. Choose a soil and crop type from the listed options. {exc}") from exc

    # This tiny dataset does not support reliable probability calibration.
    # Abstain when the class score is weak instead of presenting a guess as advice.
    if score < 0.45:
        return {
            "recommendation": None,
            "score": score,
            "message": "The model is not confident enough to suggest a fertilizer. Use a soil test and consult a local agronomist.",
        }
    return {
        "recommendation": recommendation,
        "score": score,
        "message": "Preliminary model suggestion only; confirm nutrient needs with a soil test.",
    }
''', encoding='utf-8')
(base/'src'/'train.py').write_text('''"""Train and evaluate the fertilizer recommendation model from the local CSV."""
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
''', encoding='utf-8')
(base/'app.py').write_text('''"""Streamlit UI for the fertilizer recommendation model."""
from pathlib import Path
import pandas as pd
import streamlit as st
from src.model import predict_fertilizer, load_error

ROOT = Path(__file__).resolve().parent
DATA_PATH = ROOT / "data" / "fertilizer_dataset.csv"

st.set_page_config(page_title="Fertilizer Recommendation System", page_icon="🌿", layout="centered")
st.title("🌾 Fertilizer Recommendation System")
st.write("Enter observed conditions to get a preliminary model suggestion.")
st.info("This prototype uses only 99 training rows. Confirm fertilizer needs with a recent soil test and local agronomy advice.")

if load_error:
    st.error(load_error)
    st.code(f'python "{ROOT / "src" / "train.py"}"', language="powershell")
    st.stop()

try:
    dataset = pd.read_csv(DATA_PATH)
    soil_options = sorted(dataset["Soil Type"].dropna().astype(str).unique())
    crop_options = sorted(dataset["Crop Type"].dropna().astype(str).unique())
except Exception as exc:
    st.error(f"Could not load the fertilizer dataset choices: {exc}")
    st.stop()

with st.form("fertilizer_form"):
    st.subheader("Environmental conditions")
    c1, c2, c3 = st.columns(3)
    temperature = c1.number_input("Temperature (°C)", min_value=0.0, max_value=60.0, value=25.0)
    humidity = c2.number_input("Humidity (%)", min_value=0.0, max_value=100.0, value=60.0)
    moisture = c3.number_input("Moisture (%)", min_value=0.0, max_value=100.0, value=50.0)
    st.subheader("Soil and crop")
    soil_type = st.selectbox("Soil type", soil_options)
    crop_type = st.selectbox("Crop type", crop_options)
    c4, c5, c6 = st.columns(3)
    nitrogen = c4.number_input("Nitrogen (N)", min_value=0, max_value=140, value=60)
    potassium = c5.number_input("Potassium (K)", min_value=0, max_value=140, value=50)
    phosphorous = c6.number_input("Phosphorus (P)", min_value=0, max_value=140, value=40)
    submitted = st.form_submit_button("Recommend fertilizer")

if submitted:
    try:
        result = predict_fertilizer(
            temperature, humidity, moisture, soil_type, crop_type,
            nitrogen, potassium, phosphorous,
        )
        if result["recommendation"] is None:
            st.warning(result["message"])
        else:
            st.success(f"Preliminary suggestion: {result['recommendation']}")
            st.caption(f"Raw model score: {result['score']:.1%} (not calibrated). {result['message']}")
    except Exception as exc:
        st.error(f"Could not generate a recommendation: {exc}")
''', encoding='utf-8')
