"""
csv_to_parquet.py

Regenerates the Parquet manifest from the CSV manifest. The CSV is the
human-editable canonical source; Parquet is generated, never hand-edited.

Usage:
    python scripts/utilities/csv_to_parquet.py <path_to_manifest.csv> <path_to_output.parquet>

This is a schema-enforcing conversion, not a blind pass-through: it fails loudly if the
CSV doesn't have exactly the columns defined in docs/03_AgroVision_Standards.md, rather
than silently writing whatever columns happen to be present.
"""

import sys
import pandas as pd

EXPECTED_COLUMNS = [
    "image_id", "image_path", "crop", "disease", "severity", "source",
    "domain", "quality", "split", "collection_id", "perceptual_hash",
    "license_tier", "mask_path", "notes",
]

DTYPES = {
    "image_id": "string", "image_path": "string", "crop": "string",
    "disease": "string", "severity": "float64", "source": "string",
    "domain": "string", "quality": "string", "split": "string",
    "collection_id": "string", "perceptual_hash": "string",
    "license_tier": "string", "mask_path": "string", "notes": "string",
}


def convert(csv_path: str, parquet_path: str) -> None:
    df = pd.read_csv(csv_path)

    missing = set(EXPECTED_COLUMNS) - set(df.columns)
    extra = set(df.columns) - set(EXPECTED_COLUMNS)
    if missing:
        raise ValueError(
            f"Manifest is missing required columns: {sorted(missing)}. "
            f"Update the CSV or docs/03_AgroVision_Standards.md before converting."
        )
    if extra:
        raise ValueError(
            f"Manifest has undocumented columns: {sorted(extra)}. "
            f"Add them to docs/03_AgroVision_Standards.md's manifest schema first, "
            f"so Parquet and the docs never disagree about what the data contains."
        )

    df = df[EXPECTED_COLUMNS].astype(DTYPES)
    df.to_parquet(parquet_path, index=False, engine="pyarrow")
    print(f"Wrote {len(df)} rows to {parquet_path}")


if __name__ == "__main__":
    if len(sys.argv) != 3:
        print(__doc__)
        sys.exit(1)
    convert(sys.argv[1], sys.argv[2])
