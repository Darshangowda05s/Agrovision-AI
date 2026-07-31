"""Read-only recursive dataset inventory generator.

Usage:
    python -m scripts.utilities.dataset_inventory \
        --dataset PlantVillage=datasets/raw/PlantVillage
"""

from __future__ import annotations

import argparse
import csv
import hashlib
import json
import logging
from collections import Counter
from dataclasses import asdict, dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Callable

try:
    from PIL import Image
except ImportError as exc:  # pragma: no cover - exercised without Pillow
    raise SystemExit("Pillow is required. Install it with: python -m pip install Pillow") from exc

from ..parsers import plantdoc, plantseg, plantvillage, plantwild
from ..parsers.base_parser import ParsedLabels, fallback_parse

IMAGE_EXTENSIONS = {".jpg", ".jpeg", ".png"}
CSV_FIELDS = [
    "image_id", "dataset", "relative_path", "filename", "crop", "disease",
    "extension", "file_size_bytes", "readable", "width", "height",
]
PARSERS: dict[str, Callable[[Path], ParsedLabels]] = {
    "plantvillage": plantvillage.parse,
    "plantdoc": plantdoc.parse,
    "plantwild": plantwild.parse,
    "plantseg": plantseg.parse,
}


@dataclass
class ImageRecord:
    image_id: str
    dataset: str
    relative_path: str
    filename: str
    crop: str
    disease: str
    extension: str
    file_size_bytes: int
    readable: bool
    width: int | None
    height: int | None


def image_id(dataset: str, relative_path: Path) -> str:
    key = f"{dataset}/{relative_path.as_posix()}".encode("utf-8")
    digest = hashlib.sha1(key).hexdigest()[:8]
    prefix = "".join(character for character in dataset.lower() if character.isalnum())[:3]
    return f"{prefix}_{digest}"


def get_parser(dataset: str):
    return PARSERS.get(dataset.lower(), fallback_parse)


def scan_dataset(dataset: str, root: Path, logger: logging.Logger) -> list[ImageRecord]:
    if not root.is_dir():
        raise NotADirectoryError(f"Dataset root does not exist or is not a directory: {root}")

    parser = get_parser(dataset)
    records: list[ImageRecord] = []
    for path in sorted(root.rglob("*")):
        if not path.is_file():
            continue
        relative_path = path.relative_to(root)
        if path.suffix.lower() not in IMAGE_EXTENSIONS:
            logger.info("Skipped non-image file: %s", path)
            continue

        labels = parser(relative_path)
        width = height = None
        readable = True
        try:
            with Image.open(path) as image:
                image.verify()
            with Image.open(path) as image:
                width, height = image.size
        except (OSError, ValueError) as exc:
            readable = False
            logger.warning("Unreadable image: %s (%s)", path, exc)

        records.append(ImageRecord(
            image_id=image_id(dataset, relative_path),
            dataset=dataset,
            relative_path=relative_path.as_posix(),
            filename=path.name,
            crop=labels.crop,
            disease=labels.disease,
            extension=path.suffix.lower(),
            file_size_bytes=path.stat().st_size,
            readable=readable,
            width=width,
            height=height,
        ))
    return records


def summarize(dataset: str, records: list[ImageRecord], generated_at: str) -> dict:
    classes = Counter(
        record.disease if not record.crop else f"{record.crop}___{record.disease}"
        for record in records
    )
    return {
        "dataset": dataset,
        "generated_at": generated_at,
        "total_images": len(records),
        "readable": sum(record.readable for record in records),
        "unreadable": sum(not record.readable for record in records),
        "classes": dict(sorted(classes.items())),
        "extensions": dict(sorted(Counter(record.extension for record in records).items())),
    }


def write_outputs(dataset: str, records: list[ImageRecord], output_dir: Path, generated_at: str) -> None:
    output_dir.mkdir(parents=True, exist_ok=True)
    slug = "".join(character for character in dataset.lower() if character.isalnum() or character == "_")
    csv_path = output_dir / f"{slug}_inventory.csv"
    json_path = output_dir / f"{slug}_summary.json"
    with csv_path.open("w", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames=CSV_FIELDS)
        writer.writeheader()
        writer.writerows(asdict(record) for record in records)
    with json_path.open("w", encoding="utf-8") as file:
        json.dump(summarize(dataset, records, generated_at), file, indent=2)
        file.write("\n")


def configure_logging(log_path: Path) -> logging.Logger:
    log_path.parent.mkdir(parents=True, exist_ok=True)
    logger = logging.getLogger("dataset_inventory")
    logger.setLevel(logging.INFO)
    logger.handlers.clear()
    handler = logging.FileHandler(log_path, encoding="utf-8")
    handler.setFormatter(logging.Formatter("%(asctime)s %(levelname)s %(message)s"))
    logger.addHandler(handler)
    return logger


def parse_dataset_argument(value: str) -> tuple[str, Path]:
    if "=" not in value:
        raise argparse.ArgumentTypeError("Dataset must use NAME=ROOT format")
    name, root = value.split("=", 1)
    if not name or not root:
        raise argparse.ArgumentTypeError("Dataset name and root are required")
    return name, Path(root)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--dataset", action="append", required=True, type=parse_dataset_argument,
                        help="Dataset root in NAME=ROOT format; repeat for multiple datasets")
    parser.add_argument("--output-dir", type=Path, default=Path("outputs/inventory"))
    parser.add_argument("--log-file", type=Path, default=Path("outputs/inventory/inventory.log"))
    args = parser.parse_args()
    logger = configure_logging(args.log_file)
    generated_at = datetime.now(timezone.utc).isoformat()
    for dataset, root in args.dataset:
        records = scan_dataset(dataset, root, logger)
        write_outputs(dataset, records, args.output_dir, generated_at)
        summary = summarize(dataset, records, generated_at)
        print(f"{dataset}: {summary['total_images']} images, "
              f"{len(summary['classes'])} classes, {summary['unreadable']} unreadable")


if __name__ == "__main__":
    main()