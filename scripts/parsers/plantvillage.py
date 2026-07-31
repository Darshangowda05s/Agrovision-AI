"""PlantVillage folder-label parser."""

from pathlib import Path

from .base_parser import ParsedLabels


def parse(relative_path: Path) -> ParsedLabels:
    """Parse ``Crop___Disease/image`` while preserving native label text."""
    label = relative_path.parent.name
    if "___" not in label:
        if label.startswith("Tomato_"):
            return ParsedLabels(crop="Tomato", disease=label[len("Tomato_"):].lstrip("_"))
        return ParsedLabels(disease=label)
    crop, disease = label.split("___", 1)
    return ParsedLabels(crop=crop, disease=disease)