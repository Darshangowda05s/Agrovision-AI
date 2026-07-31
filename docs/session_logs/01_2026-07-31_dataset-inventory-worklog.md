# Session 01 - Dataset Inventory and Label Discovery

**Date:** 2026-07-31  
**Project:** AgroVision AI  
**Phase:** Dataset engineering and inventory  
**Checkpoint:** Raw dataset layout discovered and inventory parsing aligned with the downloaded copies

## 1. Executive Context

AgroVision AI is a confidence-aware crop disease detection system. The project is designed for real farmer-captured images rather than only curated laboratory images. The planned pipeline separates image quality checking, leaf segmentation, crop identification, disease detection, and treatment recommendation.

At the start of this session, the project was still in the dataset-engineering stage. The raw datasets existed locally, but their folder structures had not been verified against the assumptions in the parser code. The immediate objective was to create trustworthy inventories before any label standardization, preprocessing, manifest generation, or model training.

The key rule for this stage is:

> Inventory the data as it exists. Preserve native labels and raw files. Normalize labels only in a later ingestion stage.

## 2. Project Level-Up: Before and After

### Before this session

The project had:

- Raw dataset directories under `datasets/raw/`.
- A reusable inventory script at `scripts/utilities/dataset_inventory.py`.
- Dataset-specific parsers for PlantVillage, PlantDoc, PlantSeg, and PlantWild.
- Tests for scanning images, preserving labels, writing CSV/JSON output, and detecting corrupt images.
- Parser assumptions that were not yet verified against every downloaded dataset copy.
- Inventory output for PlantVillage, but PlantDoc and PlantSeg still reflected incorrect structural assumptions.
- No confirmed evidence about the exact folder and filename conventions in the local copies.

### After this session

The project now has:

- A repeatable inventory process for all four datasets.
- Verified image totals, readability, extensions, and class counts.
- PlantVillage parsing that handles both canonical `Crop___Disease` folders and the malformed Tomato variants present in the local copy.
- PlantDoc parsing aligned with its actual `split/Class/image` layout.
- PlantSeg parsing aligned with its actual `images/{train,val,test}/filename` layout and filename-encoded labels.
- Raw class text preserved in inventory outputs instead of being silently normalized.
- Tests passing after the parser behavior and test fixture were updated.
- A clear boundary between inventory discovery and future ingestion work.
- A concrete starting point for taxonomy verification, label standardization, and manifest generation.

In practical terms, the project moved from **“datasets are present and parser assumptions exist”** to **“the local dataset copies have been measured, their label layouts are understood, and inventory outputs can support the next engineering stage.”**

## 3. What Was Inspected

### PlantVillage

The local copy contained both canonical and inconsistent Tomato folder names.

Canonical examples:

```text
Apple___Black_rot
Tomato___Late_blight
```

Inconsistent examples:

```text
Tomato_Bacterial_spot
Tomato_Early_blight
Tomato__Target_Spot
Tomato__Tomato_mosaic_virus
```

The inconsistency belongs to the downloaded dataset copy, not to the inventory framework.

### PlantDoc

The actual layout was:

```text
PlantDoc/
  train/
    Apple Scab Leaf/
      image.jpg
  test/
    Apple Scab Leaf/
      image.jpg
```

The class folder contains the full native class label. The split folder is metadata and must not be treated as the crop.

Examples of native class folders include:

```text
Apple Scab Leaf
Tomato Early blight leaf
Tomato leaf bacterial spot
Bell_pepper leaf spot
```

### PlantSeg

The actual layout was:

```text
plantseg/
  images/
    train/
      apple_black_rot_15.jpg
  annotations/
    train/
      apple_black_rot_15.png
  Metadatav2.csv
  coco_annotations.json
```

The split folder is not the class. Image filenames encode the crop and disease, with source and ID suffixes. Examples include:

```text
apple_black_rot_15.jpg
apple_black_rot_google_0001.jpg
banana_black_leaf_streak_banana black sigatoka (1).jpg
```

The dataset also contains both source images and segmentation masks, which is why the inventory counts both JPG and PNG files.

### PlantWild

PlantWild already exposed native class folders directly. Its class inventory contained a broad set of native classes such as rice blast, tomato late blight, corn rust, and apple scab. No parser correction was required in this session.

## 4. Implementation Work

### Inventory architecture

The existing inventory flow was retained:

1. Recursively scan a dataset root.
2. Keep supported image extensions: `.jpg`, `.jpeg`, and `.png`.
3. Parse labels from the dataset-specific parser.
4. Validate image readability with Pillow.
5. Record dimensions, file size, extension, path, crop, and disease.
6. Count native classes.
7. Write an inventory CSV and a summary JSON.

The inventory remains read-only with respect to the raw dataset. It does not rename, move, normalize, or modify source images.

### PlantVillage parser

The parser continues to support:

```text
Crop___Disease
```

For labels without `___`, it now recognizes the malformed Tomato prefix and separates it without normalizing the disease text:

```text
Tomato_Bacterial_spot -> crop=Tomato, disease=Bacterial_spot
Tomato__Target_Spot -> crop=Tomato, disease=Target_Spot
Tomato_healthy -> crop=Tomato, disease=healthy
```

### PlantDoc parser

The parser now treats the immediate parent folder as the native class and ignores `train` or `test` as labels. It infers a crop from a known crop prefix while preserving the complete class folder as the disease field:

```text
train/Apple Scab Leaf/image.jpg
-> crop=Apple
-> disease=Apple Scab Leaf
```

This produces a class key such as:

```text
Apple___Apple Scab Leaf
```

### PlantSeg parser

The parser now uses the filename rather than the split directory. It recognizes crop prefixes, removes only observed source/ID suffixes, and keeps the remaining disease tokens native:

```text
apple_black_rot_15.jpg
-> crop=apple
-> disease=black_rot
```

Observed source suffixes handled include numeric IDs, Google/Baidu/Bing markers, copied filename suffixes, and the verified PlantSeg source-title variants.

This is parsing, not taxonomy normalization. Lowercase spelling and underscores remain because they are part of the native filename representation.

## 5. Generated Inventory Results

All outputs were regenerated with Python 3.13 because that environment had Pillow installed.

| Dataset | Images | Readable | Unreadable | Classes | Notes |
|---|---:|---:|---:|---:|---|
| PlantVillage | 49,886 | 49,886 | 0 | 27 | Tomato naming variants separated correctly |
| PlantDoc | 2,552 | 2,552 | 0 | 27 | No split-derived classes |
| PlantSeg | 22,916 | 22,916 | 0 | 115 | Includes JPG images and PNG masks |
| PlantWild | 11,358 | 11,358 | 0 | 114 | Native class folders preserved |

Generated files are under `outputs/inventory/`:

- `plantvillage_inventory.csv`
- `plantvillage_summary.json`
- `plantdoc_inventory.csv`
- `plantdoc_summary.json`
- `plantseg_inventory.csv`
- `plantseg_summary.json`
- `plantwild_inventory.csv`
- `plantwild_summary.json`

## 6. Validation Performed

Focused tests were run after each parser change:

```text
py -3.13 -m pytest tests/test_dataset_inventory.py
2 passed
```

The full test suite was also run:

```text
py -3.13 -m pytest
2 passed
```

Final summary checks confirmed:

- PlantDoc had zero `train___...`, `test___...`, or empty-disease class keys.
- PlantSeg had zero `train___...`, `val___...`, or `test___...` class keys.
- All inventoried images were readable.
- PlantVillage had zero empty crop values after the Tomato parser fix.
- Native label text was preserved in the outputs.

## 7. Important Decisions

### Preserve raw labels during inventory

The inventory captures what the dataset actually contains. It does not convert labels to the AgroVision taxonomy. This makes dataset quirks visible and prevents accidental loss of provenance.

### Use dataset-specific parsers

There is no universal folder convention across these datasets. A parser per dataset is simpler and more honest than forcing every dataset through one assumed layout.

### Treat split folders as metadata

`train`, `val`, and `test` describe dataset partitioning. They are not disease or crop labels. The corrected parsers avoid using them as classes.

### Keep PlantSeg masks visible in inventory

PlantSeg contains segmentation masks, and the current inventory records both image and mask files. A later ingestion or manifest stage should decide whether masks get a separate record type or are paired with source images.

### Do not normalize yet

Snake-case conversion, crop canonicalization, taxonomy mapping, duplicate detection, quality filtering, and manifest generation belong to later ingestion/preprocessing stages.

## 8. Current Limitations and Risks

- PlantDoc crop inference uses known crop prefixes because its class folder combines crop and disease information in one string.
- PlantSeg label parsing is based on observed filename conventions. Its metadata and COCO annotation files should be reconciled in a later validation step, especially because native filename variants produce 115 inventory classes while the COCO category list may differ.
- The inventory currently treats PlantSeg PNG masks as images because `.png` is a supported image extension. Pairing and record typing are future ingestion concerns.
- The inventory summary currently counts classes but does not yet include a `crop_counts` field.
- Dataset license and scope decisions still need to be reflected in a future manifest and verified against project policy.
- The workspace does not contain Git metadata, so no commit was created during this session.

## 9. Recommended Next Steps

The next work should build on this checkpoint in the following order:

1. **Add targeted parser tests.** Include real PlantDoc class-folder examples and PlantSeg filenames with normal IDs, Google/Baidu/Bing suffixes, masks, and source-title variants.
2. **Reconcile PlantSeg metadata.** Compare `Metadatav2.csv`, `coco_annotations.json`, JPG files, and PNG masks by filename. Decide which source is authoritative for crop, disease, split, and image-mask pairing.
3. **Add crop counts to summaries.** Count parsed crop values separately from native class counts. Keep empty or unknown crops visible during validation rather than silently dropping them.
4. **Verify taxonomy overlap.** Compare the discovered classes with the six AgroVision Version 1 crops: Tomato, Potato, Rice, Corn, Apple, and Grape.
5. **Define the ingestion contract.** Decide how native labels map to canonical `crop` and `disease` fields, while retaining the original label and dataset provenance.
6. **Generate the manifest.** Add stable image IDs, split, license tier, native labels, canonical labels, mask relationships, readability, and quality status.
7. **Run duplicate and quality checks.** Do this only after the manifest contract is stable.
8. **Update dataset documentation.** Mark downloaded and verified status separately in `docs/02_Data_Inventory.md` and record confirmed per-crop counts.
9. **Only then begin preprocessing and model work.** The inventory stage has now supplied the evidence needed to avoid training against accidental split labels or unverified taxonomy assumptions.

## 10. Session Exit Criteria

This session is complete when:

- The four local datasets have generated inventory CSV and JSON outputs.
- Dataset-specific layout assumptions have been corrected for PlantVillage, PlantDoc, and PlantSeg.
- PlantWild has been confirmed as already structurally usable for inventory.
- Tests pass.
- The raw datasets remain untouched.
- The next stage is clearly defined as metadata reconciliation, taxonomy verification, and ingestion design.
