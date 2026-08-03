# Naming Consistency and Documentation Sync — 2026-08-03

**Checkpoint:** The inventory pipeline and documentation were aligned around a canonical snake_case naming contract.

## What changed

- Added a shared normalization module at `scripts/utilities/label_normalization.py`.
- Updated the inventory writer in `scripts/utilities/dataset_inventory.py` to emit canonical values for:
  - `dataset`: `plantvillage`, `plantdoc`, `plantwild`, `plantseg`
  - `crop`: `tomato`, `potato`, `corn`, `apple`, `grape`, etc.
  - `disease`: `late_blight`, `early_blight`, `healthy`, etc.
- Kept `relative_path` as the provenance field so the raw source location remains available.
- Updated the docs in `docs/02_Data_Inventory.md` and `docs/03_AgroVision_Standards.md` to reflect the current implementation.
- Updated the interview prep notes in `docs/interview_prep/01_2026-07-31_dataset-inventory-interview.md` to include the naming-consistency follow-up.

## Why this matters

The next phase needs a single naming convention for manifest rows, inventory outputs, and downstream preprocessing. Mixing raw source labels with canonical labels creates drift and makes later steps harder to reason about. The inventory now writes the standardized names that the manifest and training pipeline can rely on.

## Verification

- Ran the focused inventory test suite: `pytest -q tests/test_dataset_inventory.py`
- Result: `2 passed in 0.34s`

## Open follow-up

- Apply the same canonical naming contract to the future manifest generation step.
- Ensure any preprocessing, deduplication, and splitting logic consumes the canonical fields rather than re-parsing raw labels.
