"""Load the fertilizer recommendation pipeline trained by src/train.py."""
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
