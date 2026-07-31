"""PlantWild folder-label parser."""

from pathlib import Path

from .base_parser import ParsedLabels


def parse(relative_path: Path) -> ParsedLabels:
    """Record the native PlantWild class folder as the disease field."""
    return ParsedLabels(disease=relative_path.parent.name)