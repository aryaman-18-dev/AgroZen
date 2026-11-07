"""Load and run the crop-yield model exported by cropYieldPrediction1.ipynb."""

from __future__ import annotations

from pathlib import Path
from typing import Any
import math

import joblib
import numpy as np
import pandas as pd


class YieldPredictionService:
    """Notebook-trained model plus the exact encoders, scaler, and feature schema."""

    BUNDLE_NAME = "crop_yield_model_bundle.joblib"

    def __init__(self, model_dir: Path | None = None):
        project_root = Path(__file__).resolve().parents[3]
        self.model_dir = Path(model_dir) if model_dir else (
            project_root / "Crop Yield Prediction" / "crop_yield_app" / "models"
        )
        bundle_path = self.model_dir / self.BUNDLE_NAME
        if not bundle_path.is_file():
            raise FileNotFoundError(
                "The crop-yield notebook model has not been exported yet. Run all cells in "
                "Crop Yield Prediction/cropYieldPrediction1.ipynb; expected artifact: "
                f"{bundle_path}"
            )

        bundle = joblib.load(bundle_path)
        required = {
            "model", "label_encoders", "scaler", "feature_names",
            "year_min", "year_max", "recent_year_threshold",
        }
        missing = required.difference(bundle)
        if missing:
            raise ValueError(f"Crop-yield model bundle is missing keys: {', '.join(sorted(missing))}")

        self.model = bundle["model"]
        self.label_encoders = bundle["label_encoders"]
        self.scaler = bundle["scaler"]
        self.feature_names = list(bundle["feature_names"])
        self.year_min = int(bundle["year_min"])
        self.training_year_max = int(bundle["year_max"])
        # Permit predictions through 2026 as requested. Years beyond the
        # training data are extrapolations and are flagged in the response.
        self.year_max = max(self.training_year_max, 2026)
        self.recent_year_threshold = float(bundle["recent_year_threshold"])
        self.model_name = str(bundle.get("best_model_name", "Notebook-trained model"))

        for column in ("Crop", "Season", "State"):
            if column not in self.label_encoders:
                raise ValueError(f"Crop-yield model bundle has no {column} encoder.")
        if not self.feature_names:
            raise ValueError("Crop-yield model bundle has no feature schema.")

    def choices(self) -> dict[str, Any]:
        """Return selectable values and the training year range for the UI."""
        return {
            "crops": [str(value).strip() for value in self.label_encoders["Crop"].classes_],
            "seasons": [str(value).strip() for value in self.label_encoders["Season"].classes_],
            "states": [str(value).strip() for value in self.label_encoders["State"].classes_],
            "year_min": self.year_min,
            "year_max": self.year_max,
            "training_year_max": self.training_year_max,
            "yield_unit": "dataset-reported units (may vary by crop)",
        }

    @staticmethod
    def _number(payload: dict[str, Any], name: str, *, integer: bool = False) -> float | int:
        try:
            raw = payload[name]
            value = int(raw) if integer else float(raw)
        except (KeyError, TypeError, ValueError) as exc:
            raise ValueError(f"Enter a valid {name.replace('_', ' ')}.") from exc
        if not math.isfinite(float(value)):
            raise ValueError(f"Enter a valid {name.replace('_', ' ')}.")
        return value

    def _encode_category(self, row: pd.DataFrame, column: str) -> None:
        value = str(row.at[0, column]).strip()
        encoder = self.label_encoders[column]
        lookup = {str(label).strip(): label for label in encoder.classes_}
        if value not in lookup:
            raise ValueError(f"Select a {column.lower()} from the provided list.")
        # Replace the full pandas string column with an integer column. Assigning
        # through .at fails with pandas versions that infer StringDtype here.
        row[column] = pd.Series(
            encoder.transform([lookup[value]]).astype(np.int64),
            index=row.index,
            dtype=np.int64,
        )

    def predict(self, payload: dict[str, Any]) -> dict[str, Any]:
        crop = str(payload.get("crop", "")).strip()
        season = str(payload.get("season", "")).strip()
        state = str(payload.get("state", "")).strip()
        row = pd.DataFrame([
            {
                "Crop": crop,
                "Crop_Year": self._number(payload, "year", integer=True),
                "Season": season,
                "State": state,
                "Area": self._number(payload, "area"),
                "Annual_Rainfall": self._number(payload, "rainfall"),
                "Fertilizer": self._number(payload, "fertilizer"),
                "Pesticide": self._number(payload, "pesticide"),
            }
        ])

        year = int(row.at[0, "Crop_Year"])
        if not self.year_min <= year <= self.year_max:
            raise ValueError(
                f"Choose a year between {self.year_min} and {self.year_max}."
            )
        if row.at[0, "Area"] <= 0:
            raise ValueError("Area must be greater than zero.")
        for column in ("Annual_Rainfall", "Fertilizer", "Pesticide"):
            if row.at[0, column] < 0:
                raise ValueError(f"{column.replace('_', ' ')} cannot be negative.")

        # Match the input-only feature engineering in cropYieldPrediction1.ipynb.
        row["Fertilizer_per_Area"] = row["Fertilizer"] / (row["Area"] + 1e-6)
        row["Pesticide_per_Area"] = row["Pesticide"] / (row["Area"] + 1e-6)
        row["Fertilizer_Pesticide_Ratio"] = row["Fertilizer"] / (row["Pesticide"] + 1e-6)
        row["Total_Inputs"] = row["Fertilizer"] + row["Pesticide"]
        row["Log_Area"] = np.log1p(row["Area"].clip(lower=0))
        row["Sqrt_Area"] = np.sqrt(row["Area"].clip(lower=0))
        row["Years_Since_Start"] = row["Crop_Year"] - self.year_min
        row["Is_Recent"] = (row["Crop_Year"] >= self.recent_year_threshold).astype(int)
        row["Area_Rainfall"] = row["Area"] * row["Annual_Rainfall"]
        row["Fertilizer_Rainfall"] = row["Fertilizer"] * row["Annual_Rainfall"]
        row["Area_Fertilizer"] = row["Area"] * row["Fertilizer"]

        for column in ("Crop", "Season", "State"):
            self._encode_category(row, column)

        # Same ordered feature columns and robust scaler used in notebook training.
        model_input = row.reindex(columns=self.feature_names, fill_value=0)
        if not np.isfinite(model_input.to_numpy(dtype=float)).all():
            raise ValueError("Enter finite numeric values for every field.")
        scaled = self.scaler.transform(model_input)
        prediction = float(np.asarray(self.model.predict(scaled)).reshape(-1)[0])
        if not math.isfinite(prediction):
            raise RuntimeError("The yield model returned an invalid prediction.")

        return {
            "crop": crop,
            "year": year,
            "is_extrapolation": year > self.training_year_max,
            "season": season,
            "state": state,
            "area": float(row.at[0, "Area"]),
            "rainfall": float(row.at[0, "Annual_Rainfall"]),
            "fertilizer": float(row.at[0, "Fertilizer"]),
            "pesticide": float(row.at[0, "Pesticide"]),
            "yield_value": round(max(0.0, prediction), 3),
            "yield_unit": "dataset-reported units (may vary by crop)",
            "model": self.model_name,
        }
