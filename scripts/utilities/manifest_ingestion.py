"""Manifest ingestion for AgroVision Phase 4.

Reads dataset inventory CSV outputs, preserves provenance, normalizes labels via
`label_normalization.py`, and writes a canonical `datasets/manifest/manifest.csv`.
"""

from __future__ import annotations

import csv
import logging
from dataclasses import dataclass, asdict
from pathlib import Path
from typing import Iterator

from .label_normalization import (
    canonicalize_dataset_name,
    canonicalize_supported_crop,
    canonicalize_supported_disease,
    canonicalize_mapping_status,
    normalize_domain,
    normalize_license_tier,
    normalize_split,
)

CSV_FIELDS = [
    "image_id",
    "dataset",
    "relative_path",
    "image_path",
    "mask_path",
    "source_crop",
    "source_disease",
    "crop",
    "disease",
    "severity",
    "source",
    "domain",
    "quality",
    "split",
    "collection_id",
    "license_tier",
    "mapping_status",
    "notes",
]

DATASET_INVENTORY_PATHS = {
    "plantvillage": Path("outputs/inventory/plantvillage_inventory.csv"),
    "plantdoc": Path("outputs/inventory/plantdoc_inventory.csv"),
    "plantwild": Path("outputs/inventory/plantwild_inventory.csv"),
    "plantseg": Path("outputs/inventory/plantseg_inventory.csv"),
}

PLANTSEG_METADATA_PATH = Path("datasets/raw/plantseg/Metadatav2.csv")

PLANTSEG_IMAGE_BASE = Path("datasets/raw/plantseg/images")
PLANTSEG_ANNOTATION_BASE = Path("datasets/raw/plantseg/annotations")


@dataclass
class ManifestRow:
    image_id: str
    dataset: str
    relative_path: str
    image_path: str
    mask_path: str | None
    source_crop: str
    source_disease: str
    crop: str
    disease: str
    severity: None = None
    source: str = ""
    domain: str = ""
    quality: str = ""
    split: str = "unassigned"
    collection_id: str = ""
    license_tier: str = ""
    mapping_status: str = ""
    notes: str = ""


def read_plantseg_metadata(metadata_path: Path | None = None) -> dict[str, str]:
    """Return a mapping from image filename to mask filename for PlantSeg."""
    if metadata_path is None:
        metadata_path = PLANTSEG_METADATA_PATH

    metadata: dict[str, str] = {}
    if not metadata_path.exists():
        return metadata

    with metadata_path.open(newline="", encoding="utf-8") as file:
        reader = csv.DictReader(file)
        for row in reader:
            image_name = row["Name"].strip()
            mask_name = row["Label file"].strip()
            if image_name and mask_name:
                metadata[image_name] = mask_name
    return metadata


def image_path_for_manifest(dataset: str, relative_path: str) -> str:
    dataset_slug = canonicalize_dataset_name(dataset)
    return Path(dataset_slug) / relative_path


def manifest_rows() -> Iterator[ManifestRow]:
    plantseg_masks = read_plantseg_metadata()
    for dataset, inventory_path in DATASET_INVENTORY_PATHS.items():
        if not inventory_path.exists():
            continue

        with inventory_path.open(newline="", encoding="utf-8") as file:
            reader = csv.DictReader(file)
            for raw in reader:
                dataset_name = canonicalize_dataset_name(dataset)
                relative_path = raw["relative_path"]
                if dataset_name == "plantseg" and not relative_path.startswith("images/"):
                    continue

                source_crop = raw.get("crop", "")
                source_disease = raw.get("disease", "")
                crop = canonicalize_supported_crop(source_crop)
                disease = canonicalize_supported_disease(source_disease, crop)
                mapping_status = canonicalize_mapping_status(source_crop, source_disease, crop, disease)
                image_path = image_path_for_manifest(dataset, relative_path).as_posix()
                mask_path = None
                if dataset_name == "plantseg":
                    image_filename = Path(relative_path).name
                    mask_name = plantseg_masks.get(image_filename)
                    if mask_name:
                        mask_path = (Path("plantseg") / "annotations" / mask_name).as_posix()

                yield ManifestRow(
                    image_id=raw["image_id"],
                    dataset=dataset,
                    relative_path=relative_path,
                    image_path=image_path,
                    mask_path=mask_path,
                    source_crop=source_crop,
                    source_disease=source_disease,
                    crop=crop,
                    disease=disease,
                    source=dataset_name,
                    domain=normalize_domain(dataset),
                    quality="pass" if str(raw.get("readable", "False")).lower() == "true" else "fail",
                    split=normalize_split("") ,
                    collection_id=dataset_name,
                    license_tier=normalize_license_tier(dataset),
                    mapping_status=mapping_status,
                    notes="",
                )


def write_manifest(output_path: Path) -> None:
    output_path.parent.mkdir(parents=True, exist_ok=True)
    with output_path.open("w", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames=CSV_FIELDS)
        writer.writeheader()
        for row in manifest_rows():
            writer.writerow(asdict(row))


def main() -> None:
    logging.basicConfig(level=logging.INFO)
    manifest_path = Path("datasets/manifest/manifest.csv")
    write_manifest(manifest_path)
    print(f"Wrote manifest to {manifest_path}")


if __name__ == "__main__":
    main()
