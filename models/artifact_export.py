from __future__ import annotations

import json
from pathlib import Path
from shutil import copyfile
from typing import Any

from models.training_config import TrainingConfig


def export_model_artifact(
    config: TrainingConfig,
    artifact_dir: str | Path,
    weights_path: str | Path,
    labels: list[str] | None = None,
) -> Path:
    artifact_path = Path(artifact_dir)
    artifact_path.mkdir(parents=True, exist_ok=True)

    config_path = artifact_path / "config.json"
    metadata_path = artifact_path / "metadata.json"
    labels_path = artifact_path / "labels.json"
    target_weights_path = artifact_path / Path(weights_path).name

    config_path.write_text(json.dumps(config.to_dict(), indent=2))

    metadata: dict[str, Any] = {
        "model_name": config.model_name,
        "seed": config.seed,
        "batch_size": config.batch_size,
        "learning_rate": config.learning_rate,
        "epochs": config.epochs,
        "output_dir": config.output_dir,
    }
    metadata_path.write_text(json.dumps(metadata, indent=2))

    labels_payload = labels or []
    labels_path.write_text(json.dumps(labels_payload, indent=2))

    copyfile(weights_path, target_weights_path)
    return artifact_path
