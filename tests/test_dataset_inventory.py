import csv
import json
import logging
from pathlib import Path

from PIL import Image

from scripts.utilities.dataset_inventory import (
    configure_logging,
    image_id,
    scan_dataset,
    write_outputs,
)


def test_scan_preserves_native_labels_and_reports_corrupt_images(tmp_path: Path) -> None:
    root = tmp_path / "plantvillage"
    image_path = root / "Tomato___Late_blight" / "leaf.jpg"
    image_path.parent.mkdir(parents=True)
    Image.new("RGB", (32, 24), color="green").save(image_path)
    corrupt_path = root / "Tomato___Late_blight" / "broken.png"
    corrupt_path.write_bytes(b"not an image")
    skipped_path = root / "README.txt"
    skipped_path.write_text("metadata", encoding="utf-8")

    log_path = tmp_path / "inventory.log"
    logger = configure_logging(log_path)
    records = scan_dataset("PlantVillage", root, logger)

    assert len(records) == 2
    readable = next(record for record in records if record.filename == "leaf.jpg")
    corrupt = next(record for record in records if record.filename == "broken.png")
    assert readable.crop == "tomato"
    assert readable.disease == "late_blight"
    assert readable.width == 32
    assert readable.height == 24
    assert readable.file_size_bytes > 0
    assert corrupt.readable is False
    assert corrupt.width is None
    assert corrupt.height is None
    assert image_id("PlantVillage", Path("Tomato___Late_blight/leaf.jpg")) == readable.image_id

    logger.handlers[0].close()
    log_text = log_path.read_text(encoding="utf-8")
    assert "Unreadable image" in log_text
    assert "Skipped non-image file" in log_text


def test_outputs_are_written_as_csv_and_json(tmp_path: Path) -> None:
    root = tmp_path / "plantdoc" / "train" / "Tomato Early blight leaf"
    root.mkdir(parents=True)
    image_path = root / "leaf.png"
    Image.new("RGB", (10, 11), color="green").save(image_path)

    logger = logging.getLogger("test_dataset_inventory")
    records = scan_dataset("PlantDoc", tmp_path / "plantdoc", logger)
    output_dir = tmp_path / "outputs"
    write_outputs("PlantDoc", records, output_dir, "2026-07-31T16:20:00Z")

    with (output_dir / "plantdoc_inventory.csv").open(encoding="utf-8", newline="") as file:
        rows = list(csv.DictReader(file))
    summary = json.loads((output_dir / "plantdoc_summary.json").read_text(encoding="utf-8"))
    assert rows[0]["crop"] == "tomato"
    assert rows[0]["disease"] == "early_blight"
    assert summary["total_images"] == 1
    assert summary["classes"] == {"tomato___early_blight": 1}