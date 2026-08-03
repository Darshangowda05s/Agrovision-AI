"""Canonical label normalization for AgroVision datasets."""

from __future__ import annotations

import re
from typing import Tuple

CROP_ALIASES = {
    "apple": "apple",
    "apl": "apple",
    "bell_pepper": "bell_pepper",
    "bell_pepper": "bell_pepper",
    "blueberry": "blueberry",
    "cherry": "cherry",
    "corn": "corn",
    "corn_maize": "corn",
    "corn_maize": "corn",
    "grape": "grape",
    "grapevine": "grape",
    "maize": "corn",
    "peach": "peach",
    "potato": "potato",
    "pot": "potato",
    "raspberry": "raspberry",
    "soyabean": "soybean",
    "soybean": "soybean",
    "squash": "squash",
    "strawberry": "strawberry",
    "tomato": "tomato",
    "tom": "tomato",
}

DISEASE_ALIASES = {
    "healthy": "healthy",
    "late_blight": "late_blight",
    "early_blight": "early_blight",
    "bacterial_spot": "bacterial_spot",
    "leaf_mold": "leaf_mold",
    "septoria_leaf_spot": "septoria_leaf_spot",
    "spider_mites": "spider_mites",
    "target_spot": "target_spot",
    "yellow_leaf_curl_virus": "yellow_leaf_curl_virus",
    "mosaic_virus": "mosaic_virus",
    "black_rot": "black_rot",
    "apple_scab": "apple_scab",
    "cedar_apple_rust": "cedar_apple_rust",
    "gray_leaf_spot": "gray_leaf_spot",
    "common_rust": "common_rust",
    "northern_leaf_blight": "northern_leaf_blight",
    "esca_black_measles": "esca_black_measles",
    "leaf_blight_isariopsis": "leaf_blight_isariopsis",
}


def normalize_token(value: str) -> str:
    """Convert an arbitrary label to lowercase snake_case."""
    if not value:
        return ""
    normalized = re.sub(r"[^a-z0-9]+", "_", value.lower()).strip("_")
    return re.sub(r"_+", "_", normalized)


def canonicalize_dataset_name(raw_dataset: str) -> str:
    """Normalize a dataset name to the lowercase snake_case form used by the manifest."""
    token = normalize_token(raw_dataset)
    if token in {"plantvillage", "plantdoc", "plantwild", "plantseg"}:
        return token
    return token


def canonicalize_crop(raw_crop: str) -> str:
    """Normalize a crop label to the canonical snake_case form used by the taxonomy."""
    token = normalize_token(raw_crop)
    if not token:
        return ""
    return CROP_ALIASES.get(token, token)


def canonicalize_disease(raw_disease: str, crop: str) -> str:
    """Normalize a disease label to the canonical snake_case form used by the taxonomy."""
    if not raw_disease:
        return ""

    token = normalize_token(raw_disease)
    if token in DISEASE_ALIASES:
        return DISEASE_ALIASES[token]

    if crop == "tomato":
        tomato_aliases = {
            "tomato_early_blight_leaf": "early_blight",
            "tomato_leaf_early_blight": "early_blight",
            "tomato_leaf_late_blight": "late_blight",
            "tomato_leaf_bacterial_spot": "bacterial_spot",
            "tomato_leaf_mosaic_virus": "mosaic_virus",
            "tomato_leaf_yellow_virus": "yellow_leaf_curl_virus",
            "tomato_mold_leaf": "leaf_mold",
            "tomato_leaf": "healthy",
            "tomato_leaf_healthy": "healthy",
            "tomato_septoria_leaf_spot": "septoria_leaf_spot",
            "tomato_yellow_leaf_curl_virus": "yellow_leaf_curl_virus",
            "tomato_mosaic_virus": "mosaic_virus",
        }
        return tomato_aliases.get(token, token)

    if crop == "potato":
        potato_aliases = {
            "potato_leaf_early_blight": "early_blight",
            "potato_leaf_late_blight": "late_blight",
            "potato_leaf": "healthy",
        }
        return potato_aliases.get(token, token)

    if crop == "corn":
        corn_aliases = {
            "corn_gray_leaf_spot": "gray_leaf_spot",
            "corn_leaf_blight": "northern_leaf_blight",
            "corn_rust_leaf": "common_rust",
        }
        return corn_aliases.get(token, token)

    if crop == "apple":
        apple_aliases = {
            "apple_scab_leaf": "apple_scab",
            "apple_leaf": "healthy",
            "apple_rust_leaf": "cedar_apple_rust",
        }
        return apple_aliases.get(token, token)

    if crop == "grape":
        grape_aliases = {
            "grape_leaf": "healthy",
            "grape_leaf_black_rot": "black_rot",
        }
        return grape_aliases.get(token, token)

    return token


def canonicalize_labels(raw_crop: str, raw_disease: str) -> Tuple[str, str]:
    """Return canonical crop and disease names for manifest and training use."""
    crop = canonicalize_crop(raw_crop)
    disease = canonicalize_disease(raw_disease, crop)
    return crop, disease
