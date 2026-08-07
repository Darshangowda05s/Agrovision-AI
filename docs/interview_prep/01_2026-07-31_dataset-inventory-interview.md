# Session 01 - Dataset Inventory Interview Preparation

**Date:** 2026-07-31  
**Project:** AgroVision AI  
**Topic:** Dataset discovery, parser design, label preservation, and validation

## 1. One-Minute Project Summary

AgroVision AI is a confidence-aware crop disease detection system intended for real farmer-captured images. The planned pipeline separates image quality checks, leaf segmentation, crop identification, disease detection, and treatment guidance. This session focused on dataset engineering: building a read-only inventory that measures the downloaded datasets and preserves their native labels before later taxonomy standardization.

The main engineering lesson was that dataset documentation and local folder layouts cannot be treated as interchangeable. PlantVillage, PlantDoc, PlantSeg, and PlantWild use different conventions, so the inventory uses dataset-specific parsers.

## 2. Strong Interview Story

A good explanation of the session is:

> I started by validating the data instead of assuming the documented folder structure was correct. The inventory initially revealed that PlantDoc and PlantSeg split names were being reported as classes. I inspected the actual directories, identified the real label sources, updated the parsers to match those structures, regenerated the inventories, and ran the test suite. I kept raw labels unchanged because inventory is a provenance and discovery stage; canonical taxonomy mapping belongs later in ingestion.

## 2.5 Follow-up update: naming consistency and documentation sync (2026-08-03)

A strong add-on for the interview story is:

> I then tightened the naming contract so the inventory output is consistent end-to-end. The current code now normalizes dataset, crop, and disease names to lowercase snake_case before writing CSV and JSON outputs, using a shared normalization module. That prevents later stages from inheriting inconsistent values like `Tomato`, `late_blight`, or dataset names in mixed case.

This is evidence that the work moved beyond discovery and into pipeline hygiene: the inventory is now aligned with the manifest contract, the docs were updated to match the implementation, and the tests still pass.

## 2.6 Follow-up update: Phase 4 manifest ingestion and docs completion (2026-08-07)

I completed the Phase 4 canonical manifest ingestion work, generated `datasets/manifest/manifest.csv`, and updated the docs to record that the manifest is now the project’s single source of truth. This follow-up shows the work moved from inventory discovery into a stable, documented ingestion stage.

## 3. Questions an Interviewer May Ask

### Why did you build an inventory before training a model?

Because model quality depends on knowing what the data actually contains. An inventory exposes image counts, class distributions, unreadable files, extensions, dimensions, split structure, and unexpected labels. Training before this step could silently train on split names, masks, duplicate images, or labels that do not match the intended taxonomy.

### What was the first bug you found?

The first issue was not a scanner bug. The PlantVillage copy contained inconsistent Tomato folder names. Some used `Tomato___Disease`, while others used `Tomato_Disease` or `Tomato__Disease`. The parser correctly handled the documented format but lost crop information for the malformed variants. The fix recognized the observed Tomato prefix without changing the native disease text.

### What did PlantDoc teach you?

PlantDoc used `split/class/image`, not `split/crop/disease/image`. The original parser assumed the last two directories were crop and disease, so it interpreted `train` or `test` as the crop. Inspection showed that a single class folder, such as `Apple Scab Leaf`, contains the complete native class label. The corrected parser ignores the split and infers the crop from a known prefix while retaining the complete native class as the disease field.

### What did PlantSeg teach you?

PlantSeg uses `images/{train,val,test}/filename` and matching annotation directories. The split is not the class. Labels are encoded in filenames such as `apple_black_rot_15.jpg`, with additional source and ID suffixes. The parser extracts the crop and disease from the filename and removes only suffix patterns verified from the local data.

### Why did PlantSeg have more than one file per image?

The dataset contains source images and segmentation masks. The inventory currently scans both JPG and PNG files, so the total includes both. That is useful for discovery, but the future manifest should represent image-mask relationships explicitly instead of treating every PNG as an independent training image.

### Why not normalize every label immediately?

Normalization would hide useful evidence about the source data and mix two responsibilities. Inventory should preserve the raw label and provenance. Ingestion can later add canonical fields such as `crop=tomato` and `disease=bacterial_spot`, while retaining the original label for auditing and reproducibility.

### Why use separate parsers instead of one generic parser?

The datasets do not share one reliable structural convention. A generic parser would either encode many ambiguous rules or produce plausible but incorrect labels. Small dataset-specific parsers make assumptions explicit, testable, and easier to revise when a new dataset copy has a different layout.

### How did you validate the changes?

I ran the focused inventory tests after each parser edit and then ran the full test suite. I also regenerated each affected inventory and checked that PlantDoc and PlantSeg no longer emitted `train___`, `val___`, or `test___` class keys. All inventoried images were readable, and PlantVillage had no empty crop values after its parser fix.

### What are the final inventory numbers?

| Dataset | Images | Classes | Unreadable |
|---|---:|---:|---:|
| PlantVillage | 49,886 | 27 | 0 |
| PlantDoc | 2,552 | 27 | 0 |
| PlantSeg | 22,916 | 115 | 0 |
| PlantWild | 11,358 | 114 | 0 |

PlantSeg includes both source images and masks in that image total.

### Why is PlantSeg at 115 classes when another source may list 114?

The inventory reflects native filename-derived labels in this local copy. External category metadata can use slightly different naming or grouping, so the difference is a reconciliation task, not something to hide by forcing the count to match documentation. The next step is to compare filenames, `Metadatav2.csv`, and COCO categories before defining the authoritative ingestion label.

### What is the difference between inventory and ingestion?

Inventory is read-only discovery. It records what exists. Ingestion is the controlled transformation stage where labels can be standardized, taxonomy mappings can be applied, license tiers and splits can be assigned, masks can be paired, and manifest rows can be generated.

### What would you add next to make this production-ready?

I would first add targeted parser tests using real examples from every observed naming pattern. Then I would reconcile PlantSeg image and mask metadata, add crop counts to summaries, verify overlap with the five supported crops, define the manifest contract, and only after that implement label standardization, quality filtering, and duplicate detection.

### What design principle guided the work?

Do not guess silently. When the data disagrees with the documentation, inspect the data, make the parser behavior explicit, preserve provenance, and record unresolved ambiguity for the next stage.

## 4. Technical Deep-Dive Prompts

### Explain the summary generation flow.

`scan_dataset()` recursively walks the root, filters supported image extensions, calls the dataset parser, validates the image with Pillow, and creates an `ImageRecord`. `summarize()` counts native classes and readability. `write_outputs()` serializes the records to CSV and the summary to JSON.

### How are class keys constructed?

If a parsed crop exists, the summary uses `crop___disease`. If the crop is empty, it falls back to the disease field alone. This keeps the output useful while making missing crop information visible during debugging.

### What happens to corrupt images?

The scanner catches Pillow errors, marks the record as unreadable, leaves dimensions empty, logs a warning, and continues scanning. It does not silently discard the record.

### Why is continuing after a corrupt image useful?

A dataset inventory should report the complete state of the dataset. Stopping at the first bad file would hide the total number and location of additional problems.

### What makes the image IDs stable?

The ID is derived from the dataset name and relative path using a SHA-1 digest truncated to eight hexadecimal characters, with a dataset prefix. The raw relative path remains separately recorded for traceability.

### What is the main risk in the current PlantSeg parser?

Filename conventions are powerful but less authoritative than an explicit metadata join. A later ingestion step should join image filenames to `Metadatav2.csv` or COCO data and explicitly pair images with masks. The current parser is appropriate for inventory discovery but should not be treated as the final taxonomy authority.

## 5. Questions About Tradeoffs

### Why infer the PlantDoc crop instead of leaving it empty?

The class name clearly contains crop information, so retaining that information improves the inventory. The parser does not claim that the full class name is a canonical disease label; it preserves it as native text for later mapping.

### Why not rewrite the folders?

Changing raw folders would destroy source provenance and make it harder to reproduce the original dataset state. The inventory and future manifest can provide standardized views without mutating raw data.

### Why preserve case and underscores?

They are part of the source representation. Case folding, synonym handling, and snake-case conversion belong to an explicit standardization policy that can be reviewed and tested independently.

### Why are PlantWild and PlantSeg not automatically training datasets?

The project documentation treats their CC BY-NC-ND licensing as evaluation-only under the current policy. License handling should be recorded in the future manifest rather than inferred from image content.

## 6. Behavioral Questions

### What would you do if a new dataset copy changed its layout?

I would add or update a dataset-specific parser, inspect representative paths first, add fixtures for the observed patterns, regenerate the inventory, and compare counts. I would not weaken the existing parsers with broad heuristics unless the new format genuinely belongs to the same dataset contract.

### What if an image has no recognizable crop?

Keep the raw class or disease field, leave the crop empty or mark it unknown according to the ingestion contract, and report it for taxonomy review. Never force it into the nearest supported crop.

### What if two native labels map to one canonical class?

Keep both native labels and add the same canonical mapping in ingestion. The merge must be explicit so class counts, provenance, and auditability are preserved.

### What if the inventory count differs from a paper or README?

Treat the local files as the immediate source of truth for inventory, document the discrepancy, and investigate whether the difference comes from dataset version, masks, duplicates, excluded files, or split definitions.

## 7. Honest Limitations to Mention

- The crop-count field has not yet been added to the summary JSON.
- PlantSeg metadata and COCO categories still need a formal reconciliation.
- PlantSeg masks are currently included as image records rather than explicitly paired records.
- Taxonomy mapping and label standardization have intentionally not started.
- Duplicate detection and quality filtering have intentionally not started.
- The workspace has no Git metadata, so this session could not produce a commit.

## 8. Closing Answer

A strong closing statement is:

> The main result was not just four JSON files. It was a verified understanding of how each dataset encodes labels. That gives the next stage a reliable foundation: reconcile metadata, define canonical mappings, generate a provenance-rich manifest, and only then prepare data for training or evaluation.
