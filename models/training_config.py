from __future__ import annotations

import json
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any


@dataclass
class TrainingConfig:
    model_name: str
    seed: int = 42
    batch_size: int = 16
    learning_rate: float = 0.001
    epochs: int = 10
    output_dir: str = "outputs/training"

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


def save_training_config(config: TrainingConfig, path: str | Path | None = None) -> Path:
    target = Path(path) if path is not None else Path(config.output_dir) / "config.json"
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(json.dumps(config.to_dict(), indent=2))
    return target


def load_training_config(path: str | Path) -> TrainingConfig:
    data = json.loads(Path(path).read_text())
    return TrainingConfig(**data)
