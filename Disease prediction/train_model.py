"""Train a more robust tomato leaf classifier for the AgroZen app.

Run from the project root with:
    python "Disease prediction/train_model.py"

The script uses only the locally stored labeled dataset and writes a state dict
compatible with the app's current CNN inference service.
"""

from __future__ import annotations

import json
import random
import sys
from pathlib import Path

import numpy as np
import torch
from sklearn.metrics import balanced_accuracy_score, classification_report
from torch import nn
from torch.utils.data import DataLoader, Subset
from torchvision import transforms
from torchvision.datasets import ImageFolder


PROJECT_ROOT = Path(__file__).resolve().parents[1]
DISEASE_DIR = Path(__file__).resolve().parent
DATASET_DIR = DISEASE_DIR / "tomato disease detection" / "Dataset"
MODEL_PATH = DISEASE_DIR / "plant_disease_model.pth"
CLASSES_PATH = DISEASE_DIR / "plant_disease_classes.json"
SEED = 42
IMAGE_SIZE = 256
EPOCHS = 15
BATCH_SIZE = 16
PATIENCE = 4

sys.path.insert(0, str(PROJECT_ROOT))
from backend.services.ml.plant_disease_classifier import CNNNeuralNet  # noqa: E402


def make_stratified_indices(targets: list[int], validation_fraction: float = 0.2):
    """Split each class independently so every class appears in validation."""
    rng = random.Random(SEED)
    by_class: dict[int, list[int]] = {}
    for index, label in enumerate(targets):
        by_class.setdefault(int(label), []).append(index)

    train_indices: list[int] = []
    validation_indices: list[int] = []
    for indices in by_class.values():
        rng.shuffle(indices)
        validation_count = max(1, round(len(indices) * validation_fraction))
        validation_indices.extend(indices[:validation_count])
        train_indices.extend(indices[validation_count:])
    rng.shuffle(train_indices)
    rng.shuffle(validation_indices)
    return train_indices, validation_indices


def main() -> None:
    if not DATASET_DIR.is_dir():
        raise FileNotFoundError(f"Labeled dataset folder not found: {DATASET_DIR}")

    random.seed(SEED)
    np.random.seed(SEED)
    torch.manual_seed(SEED)
    if torch.cuda.is_available():
        torch.cuda.manual_seed_all(SEED)
    torch.backends.cudnn.benchmark = torch.cuda.is_available()

    # Mild transformations preserve disease signs while varying orientation,
    # framing, and illumination to reduce dependence on studio-like images.
    train_transform = transforms.Compose([
        transforms.Resize((IMAGE_SIZE, IMAGE_SIZE)),
        transforms.RandomHorizontalFlip(),
        transforms.RandomVerticalFlip(),
        transforms.RandomRotation(15),
        transforms.ColorJitter(brightness=0.18, contrast=0.18, saturation=0.15, hue=0.025),
        transforms.ToTensor(),
    ])
    validation_transform = transforms.Compose([
        transforms.Resize((IMAGE_SIZE, IMAGE_SIZE)),
        transforms.ToTensor(),
    ])

    train_source = ImageFolder(str(DATASET_DIR), transform=train_transform)
    validation_source = ImageFolder(str(DATASET_DIR), transform=validation_transform)
    if train_source.classes != validation_source.classes:
        raise RuntimeError("Dataset class order changed while preparing the split.")

    train_indices, validation_indices = make_stratified_indices(train_source.targets)
    train_set = Subset(train_source, train_indices)
    validation_set = Subset(validation_source, validation_indices)
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    workers = 0 if sys.platform == "win32" else min(4, os_cpu_count())
    train_loader = DataLoader(
        train_set, batch_size=BATCH_SIZE, shuffle=True, num_workers=workers,
        pin_memory=device.type == "cuda",
    )
    validation_loader = DataLoader(
        validation_set, batch_size=BATCH_SIZE * 2, shuffle=False, num_workers=workers,
        pin_memory=device.type == "cuda",
    )

    counts = np.bincount(
        np.asarray(train_source.targets)[train_indices], minlength=len(train_source.classes)
    ).astype(np.float32)
    # Square-root inverse frequency dampens the large class imbalance without
    # letting the smallest classes dominate every update.
    class_weights = torch.tensor(np.sqrt(counts.max() / counts), dtype=torch.float32, device=device)
    criterion = nn.CrossEntropyLoss(weight=class_weights)
    model = CNNNeuralNet(in_channels=3, num_classes=len(train_source.classes)).to(device)
    optimizer = torch.optim.AdamW(model.parameters(), lr=3e-4, weight_decay=1e-4)
    scheduler = torch.optim.lr_scheduler.ReduceLROnPlateau(
        optimizer, mode="max", factor=0.5, patience=1, min_lr=1e-6
    )

    best_balanced_accuracy = -1.0
    best_state: dict[str, torch.Tensor] | None = None
    stale_epochs = 0
    use_amp = device.type == "cuda"
    scaler = torch.amp.GradScaler("cuda", enabled=use_amp)

    print(f"Dataset: {DATASET_DIR}")
    print(f"Classes: {len(train_source.classes)} | train: {len(train_set)} | validation: {len(validation_set)}")
    print(f"Device: {device} | workers: {workers}")

    for epoch in range(1, EPOCHS + 1):
        model.train()
        total_loss = 0.0
        for images, labels in train_loader:
            images = images.to(device, non_blocking=True)
            labels = labels.to(device, non_blocking=True)
            optimizer.zero_grad(set_to_none=True)
            with torch.autocast(device_type=device.type, enabled=use_amp):
                logits = model(images)
                loss = criterion(logits, labels)
            scaler.scale(loss).backward()
            scaler.unscale_(optimizer)
            nn.utils.clip_grad_norm_(model.parameters(), max_norm=2.0)
            scaler.step(optimizer)
            scaler.update()
            total_loss += float(loss.detach()) * labels.size(0)

        model.eval()
        all_labels: list[int] = []
        all_predictions: list[int] = []
        with torch.inference_mode():
            for images, labels in validation_loader:
                logits = model(images.to(device, non_blocking=True))
                all_predictions.extend(logits.argmax(dim=1).cpu().tolist())
                all_labels.extend(labels.tolist())

        score = balanced_accuracy_score(all_labels, all_predictions)
        scheduler.step(score)
        avg_loss = total_loss / len(train_set)
        print(
            f"Epoch {epoch:02d}/{EPOCHS} | train loss {avg_loss:.4f} | "
            f"validation balanced accuracy {score:.4f}"
        )

        if score > best_balanced_accuracy:
            best_balanced_accuracy = score
            best_state = {key: value.detach().cpu().clone() for key, value in model.state_dict().items()}
            stale_epochs = 0
        else:
            stale_epochs += 1
            if stale_epochs >= PATIENCE:
                print(f"Early stopping: validation score did not improve for {PATIENCE} epochs.")
                break

    if best_state is None:
        raise RuntimeError("Training did not produce a model checkpoint.")

    # Keep the existing artifact intact until training has completed successfully.
    temporary_model = MODEL_PATH.with_suffix(".pth.tmp")
    torch.save(best_state, temporary_model)
    temporary_model.replace(MODEL_PATH)
    temporary_classes = CLASSES_PATH.with_suffix(".json.tmp")
    temporary_classes.write_text(
        json.dumps(train_source.classes, ensure_ascii=False, indent=2), encoding="utf-8"
    )
    temporary_classes.replace(CLASSES_PATH)

    model.load_state_dict(best_state)
    model.eval()
    all_labels = []
    all_predictions = []
    with torch.inference_mode():
        for images, labels in validation_loader:
            predictions = model(images.to(device, non_blocking=True)).argmax(dim=1).cpu().tolist()
            all_predictions.extend(predictions)
            all_labels.extend(labels.tolist())
    print(f"Best validation balanced accuracy: {best_balanced_accuracy:.4f}")
    print(classification_report(all_labels, all_predictions, target_names=train_source.classes, zero_division=0))
    print(f"Saved checkpoint: {MODEL_PATH}")
    print(f"Saved class order: {CLASSES_PATH}")
    print("Restart Flask before trying the updated checkpoint.")


def os_cpu_count() -> int:
    import os
    return os.cpu_count() or 1


if __name__ == "__main__":
    main()
