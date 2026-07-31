"""Interfaces and shared types for dataset inventory parsers."""

from dataclasses import dataclass
from pathlib import Path
from typing import Protocol


@dataclass(frozen=True)
class ParsedLabels:
    """Native labels inferred from a dataset-relative image path."""

    crop: str = ""
    disease: str = ""


class DatasetParser(Protocol):
    """Parse native labels without normalizing or changing source files."""

    def parse(self, relative_path: Path) -> ParsedLabels:
        ...


def fallback_parse(relative_path: Path) -> ParsedLabels:
    """Use the image's immediate parent as a conservative native class label."""

    return ParsedLabels(disease=relative_path.parent.name)