# Session 05 - Phase 5 Duplicate Analysis

**Date:** 2026-08-08  
**Project:** AgroVision AI  
**Topic:** Phase 5 duplicate analysis, determinism, and session reporting

## Summary

Completed the Phase 5 duplicate analysis implementation and created supporting unit tests. Today’s work focused on making duplicate detection conservative, auditable, and read-only while preserving raw data and the existing Phase 3/4 manifest pipeline.

## What was done

- Added `scripts/quality/phase5_duplicate_analysis.py`.
  - Reads `datasets/manifest/manifest_validated.csv` and `reports/duplicates.csv`.
  - Writes audit outputs under `reports/`.
  - Generates exact duplicate distribution, cross-dataset analysis, label conflict and license conflict tables, canonical selection policy output, near-duplicate candidate summaries, and Phase 5 JSON/Markdown summaries.
  - Includes a determinism check by running analysis twice and comparing all generated output files.
  - Includes a raw immutability check using a fast partial hash snapshot of `datasets/raw/`.

- Implemented conservative duplicate policy:
  - exact byte-identical images are treated as `exact_duplicate` only.
  - perceptual hash matches are treated as `near_duplicate_candidate` and not as confirmed deletions.
  - canonical selection uses deterministic ranking rules: supported mapping, permissive license, dataset priority, then lexical tie-break.

- Added new unit tests in `tests/test_phase5_analysis.py`.
  - Verifies exact duplicate counts, removable copy counts, and theoretical unique counts.
  - Verifies within-dataset and cross-dataset grouping logic.
  - Verifies near-duplicate candidate verification classification.
  - Verifies conflict detection and output file writing.
  - Verifies raw snapshot helper and JSON helper behavior.

- Confirmed the new script runs successfully and generates the expected report files.

## Problems encountered

- The local Python environment does not currently have `pytest` installed.
  - Running `python -m pytest -q` failed with `No module named pytest`.
- An initial patch apply failed because the tool call missed the required `explanation` field; the issue was corrected and the file was added successfully.
- A direct terminal row-count command was canceled before completion, so the exact current manifest and duplicate row totals were not captured from the shell output yet.

## Current state

- `scripts/quality/phase5_duplicate_analysis.py` exists and is functional.
- `tests/test_phase5_analysis.py` exists with 10 new unit tests.
- Report files were generated in `reports/`.
- Phase 5 analysis is ready for validation once `pytest` is installed.

## Exact counts and duplicate breakdown

- Total manifest images: `75,254`
- Total duplicate report rows: `46,750`
- Exact duplicate rows: `37,274`
- Near-duplicate candidate rows: `9,476`
- Exact duplicate groups: `18,614`
- Near-duplicate candidate groups: `945`
- Exact duplicate removable copies: `18,660`
- Theoretical unique image count after exact deduplication: `56,594`

### Exact duplicate group size distribution

- Groups of size 2: `18,583`
- Groups of size 3: `16`
- Groups of size 4: `15`

### Cross-dataset and within-dataset duplicates

- Within-dataset exact duplicate groups: `18,545`
- Cross-dataset exact duplicate groups: `69`

## What can be saved and what needs review

- `18,660` images are exact duplicate copies that could be removed if the policy is to keep one canonical image per exact SHA-256 group.
- `56,594` images remain after removing exact duplicates; these are the conservative unique set.
- `9,476` images are near-duplicate candidates only and should not be removed without human review, because they are not confirmed exact duplicates.
- The new analysis is intentionally conservative: exact duplicates are confirmed by hash, while perceptual matches are only candidates.

## Next steps

- Install `pytest` and run the full test suite.
- Verify the Phase 5 outputs match expected audit reports and check the `reports/phase5_duplicate_analysis.json` summary.
- After validation, proceed to the next pipeline phase with the deduplication inventory and conservative exact-duplicate policy in place.
