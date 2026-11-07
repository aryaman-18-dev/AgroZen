"""Inference wrapper for the CNN_NeuralNet trained by Disease prediction notebook."""

from __future__ import annotations

import base64
import binascii
import io
import json
from functools import lru_cache
from pathlib import Path
from typing import Any

import numpy as np
from PIL import Image, UnidentifiedImageError
import torch
from torch import nn


class CNNNeuralNet(nn.Module):
    """State-dict-compatible architecture from Disease prediction notebook."""

    def __init__(self, in_channels: int, num_classes: int):
        super().__init__()

        def conv_block(input_channels: int, output_channels: int, pool: bool = False):
            layers: list[nn.Module] = [
                nn.Conv2d(input_channels, output_channels, kernel_size=3, padding=1),
                nn.BatchNorm2d(output_channels),
                nn.ReLU(inplace=True),
            ]
            if pool:
                layers.append(nn.MaxPool2d(4))
            return nn.Sequential(*layers)

        self.conv1 = conv_block(in_channels, 64)
        self.conv2 = conv_block(64, 128, pool=True)
        self.res1 = nn.Sequential(conv_block(128, 128), conv_block(128, 128))
        self.conv3 = conv_block(128, 256, pool=True)
        self.conv4 = conv_block(256, 512, pool=True)
        self.res2 = nn.Sequential(conv_block(512, 512), conv_block(512, 512))
        self.classifier = nn.Sequential(nn.MaxPool2d(4), nn.Flatten(), nn.Linear(512, num_classes))

    def forward(self, x):
        x = self.conv1(x)
        x = self.conv2(x)
        x = self.res1(x) + x
        x = self.conv3(x)
        x = self.conv4(x)
        x = self.res2(x) + x
        return self.classifier(x)


SUPPORTED_CROPS = {
    "tomato": "Tomato",
    "potato": "Potato",
    "grape": "Grape",
    "orange": "Orange",
    "soybean": "Soybean",
    "squash": "Squash",
    "corn": "Corn_(maize)",
    "strawberry": "Strawberry",
    "peach": "Peach",
    "apple": "Apple",
    "blueberry": "Blueberry",
    "cherry": "Cherry_(including_sour)",
    "pepper": "Pepper,_bell",
    "raspberry": "Raspberry",
}


class PlantDiseaseClassifier:
    """Loads the local checkpoint once and runs CPU/GPU inference without network calls."""

    MODEL_PATH = (
        Path(__file__).resolve().parents[3]
        / "Disease prediction"
        / "plant_disease_model.pth"
    )
    CLASSES_PATH = MODEL_PATH.with_name("plant_disease_classes.json")

    def __init__(self, model_path: Path | None = None, classes_path: Path | None = None):
        self.model_path = Path(model_path) if model_path else self.MODEL_PATH
        self.classes_path = Path(classes_path) if classes_path else self.CLASSES_PATH
        if not self.model_path.is_file():
            raise FileNotFoundError(
                "Trained Disease prediction checkpoint is missing. Run the training notebook, "
                f"then place plant_disease_model.pth at {self.model_path}."
            )
        if not self.classes_path.is_file():
            raise FileNotFoundError(
                "Disease model class metadata is missing. Export plant_disease_classes.json "
                f"beside the checkpoint: {self.classes_path}."
            )
        with self.classes_path.open("r", encoding="utf-8") as classes_file:
            self.class_names = json.load(classes_file)
        if not isinstance(self.class_names, list) or not self.class_names or not all(
            isinstance(label, str) and "___" in label for label in self.class_names
        ):
            raise ValueError("Disease model class metadata must be a JSON list of ImageFolder class names.")

        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        state_dict = torch.load(self.model_path, map_location=self.device, weights_only=True)
        self.model = CNNNeuralNet(in_channels=3, num_classes=len(self.class_names))
        self.model.load_state_dict(state_dict, strict=True)
        self.model.to(self.device)
        self.model.eval()

    @staticmethod
    def _tensor(image_bytes: bytes) -> torch.Tensor:
        try:
            with Image.open(io.BytesIO(image_bytes)) as image:
                image = image.convert("RGB").resize((256, 256), Image.Resampling.BILINEAR)
                array = np.asarray(image, dtype=np.float32) / 255.0
        except (UnidentifiedImageError, OSError, ValueError) as exc:
            raise ValueError("That file is not a readable image. Choose a clear JPG, PNG, or WebP photo.") from exc

        tensor = torch.from_numpy(array.transpose(2, 0, 1).copy())
        # The training notebook uses torchvision.transforms.ToTensor() only:
        # keep RGB values in [0, 1] and do not apply ImageNet normalization.
        return tensor.unsqueeze(0)

    @staticmethod
    def _crop_matches(class_name: str, requested_crop: str) -> bool:
        class_crop = class_name.split("___", 1)[0]
        expected = SUPPORTED_CROPS.get(requested_crop.strip().lower())
        return expected is not None and class_crop == expected

    def predict(self, image_value: str, crop_type: str = "Unknown") -> dict[str, Any]:
        if image_value.startswith("data:"):
            try:
                _, image_value = image_value.split(",", 1)
            except ValueError as exc:
                raise ValueError("The selected image could not be read.") from exc
        try:
            image_bytes = base64.b64decode(image_value, validate=True)
        except (binascii.Error, ValueError) as exc:
            raise ValueError("The selected image could not be decoded.") from exc
        if not image_bytes:
            raise ValueError("Choose an image to analyze.")
        if len(image_bytes) > 10 * 1024 * 1024:
            raise ValueError("Image must be under 10 MB.")

        normalized_crop = (crop_type or "Unknown").strip()
        if normalized_crop.lower() not in {"unknown", "not sure", ""} and normalized_crop.lower() not in SUPPORTED_CROPS:
            supported = ", ".join(crop.title() for crop in SUPPORTED_CROPS)
            raise ValueError(f"This trained model supports: {supported}.")

        tensor = self._tensor(image_bytes).to(self.device)
        with torch.inference_mode():
            probabilities = torch.softmax(self.model(tensor)[0], dim=0).cpu()

        candidates = list(range(len(self.class_names)))
        if normalized_crop.lower() not in {"unknown", "not sure", ""}:
            candidates = [i for i, name in enumerate(self.class_names) if self._crop_matches(name, normalized_crop)]
            if not candidates:
                raise ValueError("No trained classes are available for that crop.")

        best_index = max(candidates, key=lambda i: float(probabilities[i]))
        top_indices = sorted(candidates, key=lambda i: float(probabilities[i]), reverse=True)[:3]
        class_name = self.class_names[best_index]
        crop_label, disease_label = class_name.split("___", 1)
        return {
            "class_name": class_name,
            "crop": crop_label,
            "disease": disease_label,
            "confidence": round(float(probabilities[best_index]) * 100, 1),
            "alternatives": [
                {"class_name": self.class_names[i], "confidence": round(float(probabilities[i]) * 100, 1)}
                for i in top_indices
            ],
            "model": "Disease prediction CNN_NeuralNet",
            "device": str(self.device),
        }


@lru_cache(maxsize=1)
def get_plant_disease_classifier() -> PlantDiseaseClassifier:
    return PlantDiseaseClassifier()
