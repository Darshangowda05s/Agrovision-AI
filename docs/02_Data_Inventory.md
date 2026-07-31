# 02 — Data Inventory

This is the authoritative dataset inventory. **Do not download a dataset that is not
listed here with `Status: Approved`.** If you find a promising dataset elsewhere, add a
row with `Status: Candidate` and get it reviewed before pulling it into `datasets/raw/`.

## Active datasets

| Dataset | License | Download URL | Approx. Images | Crops (of our 6) | Domain | Status | Downloaded | Verified | Notes |
|---|---|---|---|---|---|---|---|---|---|
| PlantVillage | CC BY 4.0 | https://github.com/spMohanty/PlantVillage-Dataset (also mirrored on Kaggle, e.g. `abdallahalidev/plantvillage-dataset`) | ~54,300 | Apple, Corn, Grape, Potato, Tomato (**no Rice**) | Lab | ✅ Approved | ❌ No | ❌ No | Baseline/pretraining only — do not use alone for the field-image test set |
| PlantDoc | CC BY 4.0 | https://github.com/pratikkayal/PlantDoc-Dataset (cropped) / https://public.roboflow.com/object-detection/plantdoc (annotated) | ~2,600 | Apple, Corn, Grape, Potato, Tomato (**no Rice**) | Field | ✅ Approved | ❌ No | ❌ No | Small but real-world; core of our field-image test set |
| PlantWild | **CC BY-NC-ND 4.0** | https://huggingface.co/datasets/uqtwei2/PlantWild | 18,542 (v1) / more in v2 | Not yet crop-verified against our 6 | Field | ⚠️ Approved — **evaluation/benchmarking only, not training** (see license_tier policy) | ❌ No | ❌ No | Includes per-class text descriptions — usable for the RAG knowledge base regardless of the image-training restriction, since text and image licensing are handled separately |
| PlantSeg | **CC BY-NC-ND 4.0** (one related preprint lists CC BY-NC; treat as NC either way) | https://github.com/tqwei05/PlantSeg (loader) → data on Zenodo | ~11,400–7,774 (sources vary on exact count) | Not yet crop-verified | Field | ⚠️ Approved — **evaluation/benchmarking only, not training** | ❌ No | ❌ No | Only source in our inventory with segmentation masks — valuable for Phase 5's leaf segmentation model *evaluation*, not training, under current policy |

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

## Per-dataset crop/disease verification status

This still needs to happen for PlantWild and PlantSeg specifically — we know their
approximate class counts but haven't confirmed exact overlap with our six target crops.

**Action item:** before Step 4 (taxonomy) is finalized, spot-check PlantWild and PlantSeg
class lists against {Tomato, Potato, Rice, Corn, Apple, Grape} and update this table with
confirmed per-crop image counts.
