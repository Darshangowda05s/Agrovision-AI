"""PlantSeg folder-label parser."""

from pathlib import Path
import re

from .base_parser import ParsedLabels

_CROP_PREFIXES = (
    "bell_pepper", "blueberry", "grapevine", "strawberry", "cauliflower",
    "cucumber", "eggplant", "zucchini", "apple", "banana", "basil", "bean",
    "broccoli", "cabbage", "carrot", "celery", "cherry", "citrus", "coffee",
    "corn", "garlic", "ginger", "grape", "lettuce", "maple", "peach", "plum",
    "potato", "raspberry", "rice", "soybean", "squash", "tobacco", "tomato",
    "wheat",
)


def parse(relative_path: Path) -> ParsedLabels:
    """Parse ``crop_disease_source-id/image`` from the native filename."""
    label = relative_path.stem
    label = re.sub(r"_(?:google_)?\d+$", "", label)
    label = re.sub(r"_(?:Baidu|Bing|Google)$", "", label)
    label = re.sub(r"_[^_]+ \(\d+\)$", "", label)
    label = re.sub(r"_google(?:_.*)?$", "", label)
    label = re.sub(r"_black_chaff \(\d+\)$", "", label)
    label = re.sub(r"_Bing_\d+ - Copy$", "", label)
    label = re.sub(r"_black$", "", label)
    crop = next(
        (prefix for prefix in _CROP_PREFIXES if label == prefix or label.startswith(f"{prefix}_")),
        "",
    )
    if not crop:
        return ParsedLabels(disease=label)
    disease = label[len(crop):].lstrip("_")
    return ParsedLabels(crop=crop, disease=disease)