# 03 — AgroVision Standards

This is the rulebook every preprocessing script must follow. If a script's output
disagrees with this document, the document wins — fix the script, don't special-case it.

## Naming conventions

- **Crop names:** lowercase, snake_case. `tomato`, `bell_pepper` — not `Tomato`, `Bell Pepper`.
- **Disease names:** lowercase, snake_case. `late_blight`, `early_blight`,
  `healthy` — not `Late Blight`, `Late_Blight`, `late-blight`.
- **Combined crop-disease labels** (when needed): `crop__disease`, double underscore as
  separator, e.g. `tomato__late_blight`. This avoids ambiguity if a crop or disease name
  itself contains an underscore.
- Every raw dataset's original label gets mapped to this convention during Step 4
  (label standardization) — never train directly on a dataset's native label strings.

## Image format standards

- **Accepted formats:** JPG, JPEG, PNG. Anything else gets converted or rejected during
  ingestion, never passed through silently.
- **Minimum resolution:** 512×512. This is a placeholder default — revisit once we know
  the actual resolution distribution across our approved datasets; don't reject a large
  fraction of a small dataset (e.g. PlantDoc) over a resolution cutoff picked arbitrarily.
- **Color mode:** RGB. Grayscale or CMYK images get converted or flagged for manual
  review, not silently coerced.

## Quality requirements (auto-reject list)

An image fails the quality gate and does not enter `datasets/processed/` if it is:

- Blurry (define the actual metric/threshold in `scripts/quality/` — e.g. variance of
  Laplacian below a chosen cutoff — and record the threshold here once chosen, so it's
  reproducible, not tribal knowledge)
- Corrupted / fails to decode
- A screenshot (has UI chrome, browser frame, obvious app screenshot artifacts)
- Watermarked (visible text/logo overlay)
- Showing multiple leaves in one frame, **for the disease classification training set
  specifically** — this constraint does not apply to leaf segmentation training data,
  where multiple leaves are expected and useful
- Unreadable / label-ambiguous (a human reviewer cannot tell what disease, if any, is
  shown)

Anything auto-rejected still gets a manifest row with `quality: fail` and a `notes` entry
explaining why — don't just delete it. This makes the filtering auditable and reversible
if a threshold turns out to be wrong later.

## Deduplication method

"Remove duplicates" is not itself a method — this is the actual procedure:

1. **Exact duplicates:** file-level hash (SHA-256). Catches byte-identical files only.
2. **Near-duplicates (resized/recompressed/cropped copies):** perceptual hashing (pHash
   or dHash) with a similarity threshold — needed because datasets crowd-sourced from
   Google/Baidu Images (e.g. PlantWild) frequently re-scrape the same underlying photos
   at different resolutions.
3. **Visually similar but not identical (same plant, different angle/moment):** CNN
   embedding cosine-similarity pass using a pretrained feature extractor, flagged for
   manual review above a similarity threshold rather than auto-removed — these are
   borderline and shouldn't be silently dropped without a human glance.

Store the `perceptual_hash` in the manifest for every image so re-running dedup doesn't
require re-hashing from scratch.

## Dataset versioning

```
v0.1  → raw datasets ingested, manifest created, no cleaning yet
v0.2  → labels standardized against the taxonomy
v0.3  → duplicates removed
v0.4  → quality filtered
v0.5  → pilot training run completed, labeling/class issues fixed
v1.0  → frozen — this is what every experiment in Phase 6 onward trains/evaluates on
```

Each version bump gets a git tag and a one-paragraph changelog entry in this file. Once
`v1.0` is tagged, **the dataset does not change** without a new major version and a
re-run of every experiment that depended on the old one.

## Splitting rules

- Split at the **`collection_id` level, not the image level.** If two images came from
  the same farm visit, the same scraping session, or the same source dataset's
  train/test split, they move together. This prevents near-duplicate leakage across
  train/test that survives deduplication (e.g. two photos of the same leaf from
  slightly different angles).
- The **test set is deliberately weighted toward field-domain images**, even if this
  means a smaller test set than a random 80/10/10 split would give. Users submit field
  photos; a test set dominated by lab images overstates real-world accuracy.
- Stratify by crop and by class within crop, so a rare disease class isn't accidentally
  wiped out of the test set entirely.

## Experiment Standards

Every model trained under this project — the pilot run in Step 10, and every model in
Phase 6's universal-vs-per-crop-vs-shared-backbone comparison — uses these fixed
conditions, so results are comparable across experiments rather than confounded by
different setups:

- **Random seed:** `42`, set for every library involved (Python's `random`, NumPy,
  the deep learning framework, and any data-loader shuffling) — not just one of them.
- **Split ratios:** 80% train / 10% validation / 10% test, applied at the
  `collection_id` level per the splitting rules above — never a naive random row split.
- **Required evaluation metrics, reported for every model, every run:**
  - Accuracy
  - Precision (macro-averaged, since class counts are imbalanced across crops/diseases)
  - Recall (macro-averaged)
  - F1 (both per-class and macro F1 — macro F1 is the headline number given class
    imbalance; per-class F1 catches a model quietly failing on rare classes)
  - Confusion matrix (full, not just summary numbers — this is where per-crop or
    per-disease failure patterns actually show up)
  - Inference time (per image, on a stated reference device/hardware — record what
    that hardware is, since "50ms" means nothing without it)
  - **End-to-end pipeline accuracy**, not just per-stage accuracy — if a model is one
    stage in a multi-stage pipeline, also report accuracy after chaining it with the
    other stages, since per-stage numbers alone overstate real-world performance in a
    cascade (see `01_Project_Scope.md`'s design principles on this).
- **Report field-domain and lab-domain accuracy separately**, not just a blended
  number — a model that's 95% overall but 70% on field images is a materially
  different result than one that's 90% on both, even though the blended average might
  look similar.

Any experiment that deviates from these settings (e.g. a different seed to test
sensitivity to initialization) must say so explicitly in its results — never silently.

## Manifest schema

The manifest (`datasets/manifest/`) is the single source of truth. One row per image.

`manifest_template.csv` is the **only** hand-edited template. Once real ingestion starts,
run `scripts/utilities/csv_to_parquet.py` to generate a Parquet copy for anything code
touches (training pipelines, dedup scripts, etc.) — typed columns, smaller on disk,
faster to load at the row counts this project will reach once all six crops are
ingested. **Never hand-author or hand-edit a `.parquet` manifest file** — it's a build
artifact of the CSV, not a second source of truth. If the two ever disagree, the CSV
wins and the Parquet gets regenerated.

| Column | Type | Description |
|---|---|---|
| `image_id` | string | Unique identifier, stable across pipeline re-runs |
| `image_path` | string | File location relative to `datasets/processed/` |
| `crop` | string | snake_case crop name, must exist in `04_Taxonomy.md` |
| `disease` | string | snake_case disease name, must exist in `04_Taxonomy.md`, or `unknown` |
| `severity` | float or null | Reserved for future use — leave null until an annotation effort exists |
| `source` | string | Which dataset this image came from (e.g. `plantvillage`, `plantdoc`) |
| `domain` | enum | `lab` or `field` |
| `quality` | enum | `pass` or `fail` |
| `split` | enum | `train`, `val`, or `test` |
| `collection_id` | string | Groups images from the same acquisition session/source-split, for leak-safe splitting |
| `perceptual_hash` | string | pHash value, for deduplication |
| `license_tier` | enum | `train_ok` or `eval_only` — see `02_Data_Inventory.md` |
| `mask_path` | string or null | Path to segmentation mask if one exists (currently only PlantSeg) |
| `notes` | string | Free text — rejection reasons, manual review flags, anything not captured elsewhere |

This schema is the contract every preprocessing script writes against. If a script needs
a column that isn't here, add it here first, then update the script — not the reverse.
