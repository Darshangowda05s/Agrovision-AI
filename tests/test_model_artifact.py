import json
from pathlib import Path

from models.training_config import TrainingConfig, load_training_config, save_training_config
from models.artifact_export import export_model_artifact


def test_training_config_round_trip(tmp_path):
    config = TrainingConfig(
        model_name="baseline_cnn",
        seed=42,
        batch_size=16,
        learning_rate=0.001,
        epochs=5,
        output_dir="outputs/test_run",
    )

    path = tmp_path / "config.json"
    save_training_config(config, path)

    loaded = load_training_config(path)

    assert loaded.model_name == config.model_name
    assert loaded.seed == config.seed
    assert loaded.batch_size == config.batch_size
    assert loaded.output_dir == config.output_dir


def test_export_model_artifact_creates_expected_files(tmp_path):
    config = TrainingConfig(
        model_name="baseline_cnn",
        seed=42,
        batch_size=16,
        learning_rate=0.001,
        epochs=5,
        output_dir="outputs/test_run",
    )
    weights_path = tmp_path / "model_weights.pth"
    weights_path.write_bytes(b"fake-weights")

    artifact_dir = tmp_path / "artifact"
    export_model_artifact(config, artifact_dir, weights_path)

    assert (artifact_dir / "config.json").exists()
    assert (artifact_dir / "metadata.json").exists()
    assert (artifact_dir / "labels.json").exists()
    assert (artifact_dir / "model_weights.pth").exists()

    metadata = json.loads((artifact_dir / "metadata.json").read_text())
    assert metadata["model_name"] == "baseline_cnn"
