# 02 — Data Inventory

This is the authoritative dataset inventory. **Do not download a dataset that is not
listed here with `Status: Approved`.** If you find a promising dataset elsewhere, add a
row with `Status: Candidate` and get it reviewed before pulling it into `datasets/raw/`.

## Current implementation note (2026-08-03)

The inventory generator now writes canonical snake_case values for `dataset`, `crop`, and
`disease` into the CSV and JSON outputs. This is enforced by the shared normalization
module in `scripts/utilities/label_normalization.py` and is used by the inventory pipeline
in `scripts/utilities/dataset_inventory.py`.

The main inventory fields are therefore now consistent with the manifest contract:

- `dataset`: `plantvillage`, `plantdoc`, `plantwild`, `plantseg`
- `crop`: `tomato`, `potato`, `corn`, `apple`, `grape`, etc.
- `disease`: `late_blight`, `early_blight`, `healthy`, etc.

The source path remains available via `relative_path` for provenance, but the downstream
inventory fields are normalized and should be treated as the canonical values for the next
phase.

## Phase 4 status update (2026-08-07)

The Phase 4 manifest ingestion work is complete. The canonical manifest file was generated
at `datasets/manifest/manifest.csv` and is now the authoritative source of truth for
pipeline ingestion. Raw source labels are preserved via `source_crop` and
`source_disease`, and PlantSeg masks are attached via `mask_path`.

A canonical Phase 4 manifest has now been generated at `datasets/manifest/manifest.csv`.
This CSV is the project’s current single source of truth for ingestion, with raw source
labels preserved via `source_crop` and `source_disease`, and PlantSeg masks attached via
`mask_path`.

## Active datasets

| Dataset | License | Download URL | Approx. Images | Crops (of our 5) | Domain | Status | Downloaded | Verified | Notes |
|---|---|---|---|---|---|---|---|---|---|
| PlantVillage | CC BY 4.0 | https://github.com/spMohanty/PlantVillage-Dataset (also mirrored on Kaggle, e.g. `abdallahalidev/plantvillage-dataset`) | 49,886 local images | Apple, Corn, Grape, Potato, Tomato | Lab | ✅ Approved | ✅ Yes | ✅ Yes | 49,886/49,886 readable. Baseline/pretraining only — do not use alone for the field-image test set. The local copy also contains out-of-scope Bell Pepper classes. |
| PlantDoc | CC BY 4.0 | https://github.com/pratikkayal/PlantDoc-Dataset (cropped) / https://public.roboflow.com/object-detection/plantdoc (annotated) | 2,552 local images | Apple, Corn, Grape, Potato, Tomato | Field | ✅ Approved | ✅ Yes | ✅ Yes | 2,552/2,552 readable. Small but real-world; core of the field-image test set. The local copy also contains out-of-scope classes. |
| PlantWild | **CC BY-NC-ND 4.0** | https://huggingface.co/datasets/uqtwei2/PlantWild | 11,358 local images | Apple, Corn, Grape, Potato, Tomato | Field | ⚠️ Approved — **evaluation/benchmarking only, not training** (see license_tier policy) | ✅ Yes | ✅ Yes | 11,358/11,358 readable. Exact native class list and five-crop overlap inventoried; includes other crops and disease labels outside V1. |
| PlantSeg | **CC BY-NC-ND 4.0** (one related preprint lists CC BY-NC; treat as NC either way) | https://github.com/tqwei05/PlantSeg (loader) → data on Zenodo | 11,458 JPG images + 11,458 PNG masks | Apple, Corn, Grape, Potato, Tomato | Field | ⚠️ Approved — **evaluation/benchmarking only, not training** | ✅ Yes | ✅ Yes | 22,916/22,916 files readable. Image/mask pairs are both included in the raw inventory; metadata reconciliation remains a Phase 4 task. |

**"Downloaded" vs. "Verified" are deliberately separate columns, not one status field.**
Downloaded means the files are on disk. Verified means someone has actually opened a
sample, confirmed the label format matches `04_Taxonomy.md`, and confirmed there are no
surprise classes. A dataset can sit at "Downloaded: Yes, Verified: No" for a while —
that's an expected, honest intermediate state, not a problem to hide. **No dataset moves
into `datasets/processed/` or gets rows added to the manifest until Verified is Yes.**

## Watch list (not usable yet)

| Dataset | Why it's not usable now | Revisit when |
|---|---|---|
| AgriPath-LF16 | Paper's own download link is an anonymized placeholder pending peer review — no public repo exists | A public GitHub/HF release appears |
| SAGE | No dataset repository or download link found anywhere as of this writing; very recent preprint (May 2026) | A public release appears |

Do not build anything in Phase 3 onward that assumes either of these exists. Mention them
in the final report as future work, nothing more.

## Rejected / not considered

(Empty for now — add anything explicitly evaluated and turned down, with a one-line
reason, so the decision doesn't get re-litigated later.)

## License policy — how `license_tier` gets set

Every image's manifest row gets a `license_tier` value of either `train_ok` or
`eval_only`, set at ingestion time based on this table:

- `train_ok`: PlantVillage, PlantDoc (both CC BY 4.0 — permissive)
- `eval_only`: PlantWild, PlantSeg (both CC BY-NC-ND — non-commercial, no-derivatives)

**Why `eval_only` and not excluded entirely:** NC-ND restricts *redistributing modified
versions* of the work, not simply looking at it privately. Using these for validation/test
evaluation, or as a source for RAG text descriptions, does not create a redistributed
derivative. Training a model on them and then **publicly releasing the resulting weights
or the merged dataset** would be a much closer call. Until there's a final decision on
whether AgroVision's model/dataset gets publicly released, treat `eval_only` as binding
for anything that touches the training set.

**To override this policy:** if the project decision becomes "no public release, ever,"
this restriction can be relaxed and this document should be updated with that decision
and its date, not just silently changed in code.

## Local inventory verification (2026-07-31)

The inventory script opened every enumerated image successfully and recorded exact native
class labels. This verifies local presence, readability, label strings, and crop overlap;
it does **not** validate disease truth, image quality, duplicate status, or the semantic
mapping of ambiguous labels.

| Dataset | Apple | Corn | Grape | Potato | Tomato | Notes |
|---|---:|---:|---:|---:|---:|---|
| PlantVillage | 3,171 | 3,852 | 4,062 | 4,304 | 28,022 | Remaining 2,475 images are out-of-scope Bell Pepper. |
| PlantDoc | 267 | 376 | 133 | 222 | 731 | Remaining 823 images are out-of-scope crops. |
| PlantWild | 569 | 616 | 565 | 243 | 902 | Counts cover all native labels for each crop, including labels not currently supported by the V1 taxonomy. |
| PlantSeg | 569 JPG images + matching masks | 616 + matching masks | 565 + matching masks | 243 + matching masks | 902 + matching masks | The raw inventory has twice these counts because it enumerates PNG masks as well as JPG images. |

The PlantWild and PlantSeg crop counts match at image level because the local PlantSeg
copy contains the corresponding image/mask material. Neither dataset is eligible for
training under the current `eval_only` policy.
