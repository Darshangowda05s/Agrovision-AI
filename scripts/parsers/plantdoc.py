"""PlantDoc folder-label parser."""

from pathlib import Path

from .base_parser import ParsedLabels

_CROP_PREFIXES = (
    "Bell_pepper", "Blueberry", "Strawberry", "Soyabean", "Apple", "Cherry",
    "Corn", "Peach", "Potato", "Raspberry", "Squash", "Tomato", "grape",
)


def parse(relative_path: Path) -> ParsedLabels:
    """Parse ``split/Class/image`` while preserving the native class label."""
    label = relative_path.parent.name
    crop = next(
        (prefix for prefix in _CROP_PREFIXES if label.startswith(f"{prefix} ")),
        "",
    )
    return ParsedLabels(crop=crop, disease=label)