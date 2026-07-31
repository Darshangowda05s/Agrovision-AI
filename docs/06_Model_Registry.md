# 06 — Model Registry (Standalone)

**Kept outside the AgroVision-AI repository, same as the architecture file.** Once
Phase 5 (baseline training) actually starts, decide whether this content moves into the
repo as `docs/06_Model_Registry.md` — it will need to live somewhere version-controlled
once real entries exist, since "Git Commit" only means something if this file itself is
tracked alongside the code it references.

## Purpose

Every trained model — baseline, experiment, or final candidate — gets exactly one row.
This is what makes Phase 6's universal-vs-per-crop-vs-shared-backbone comparison
reproducible: given a Model ID, anyone should be able to find the exact code, data
version, and weights that produced a given accuracy number, months later.

## Rules

- **Append-only.** Never edit or delete a row after a training run is recorded. If a
  model gets retrained, it gets a new Model ID and a new row — this preserves the
  ability to compare across experiments honestly, rather than quietly overwriting a
  disappointing result.
- **No row without a Git Commit.** If the training code that produced a model isn't
  committed, the run isn't reproducible and shouldn't be recorded as a real entry yet
  (a scratch/exploratory run can go in a personal notebook, not here).
- **No row without a stated dataset version.** Reference the exact
  `AgroVision Dataset` version tag (e.g. `v1.0`) from `03_AgroVision_Standards.md`'s
  versioning scheme — never "the dataset" unqualified, since the whole point of freezing
  versions was to make this comparison meaningful.
- **Weights are never stored in this file or in git directly** (binary weight files
  don't belong in a git repo). Store a path or URL to external storage (cloud bucket,
  Hugging Face Hub, Git LFS if you must) — the registry tracks *where to find* the
  weights, not the weights themselves.
- **Report metrics per `03_AgroVision_Standards.md`'s Experiment Standards section** —
  same seed, same split methodology, same metric set — so accuracy numbers across rows
  are actually comparable to each other, not apples-to-oranges.

## Model ID convention

```
{stage}-{architecture-family}-{sequence}

Examples:
disease-universal-001
disease-percrop-tomato-001
disease-sharedbackbone-001
segment-yolov8seg-001
cropclf-effnet-001
quality-mobilenet-001
```

Stage prefixes: `quality`, `segment`, `cropclf`, `disease`. For `disease`, the
architecture family also encodes which of the three Phase 6 approaches produced it
(`universal`, `percrop-{crop}`, `sharedbackbone`) so rows are filterable by approach
without parsing free text.

---

## Candidate Architecture Catalog

This is the list of architectures under consideration, **not a record of what's been
trained**. Nothing in this section is a registry entry — think of it as the menu the
registry table below gets populated from.

### Disease detection — the Phase 6 experiment itself

| Approach | Description | Hypothesis being tested |
|---|---|---|
| **Universal** | One model, all crops and diseases in a single output head | Simplicity and cross-crop transfer learning may outweigh the "two questions at once" problem for crops with less data |
| **Per-Crop** | One independently trained model per crop (6 total) | Lower per-model complexity and easier incremental updates, at the cost of no cross-crop transfer for data-poor crops |
| **Shared Backbone** | One shared feature extractor, crop-conditioned or crop-specific classification heads | Middle ground — specialization without N fully independent models; candidate added specifically to address Per-Crop's low-data-crop weakness |

### Backbone / feature-extractor candidates (apply to Universal, Per-Crop, and Shared-Backbone approaches)

| Architecture | Typical role here | Notes |
|---|---|---|
| **EfficientNet** (B0–B4) | Disease/crop classification backbone | Strong accuracy-per-parameter; a reasonable default starting point given likely mobile-adjacent deployment constraints |
| **ConvNeXt** (Tiny/Small) | Disease/crop classification backbone | Modernized CNN, competitive with vision transformers at moderate compute cost |
| **Vision Transformer (ViT) / DeiT** | Disease/crop classification backbone | Candidate if dataset size (post Phase 3 freeze) turns out large enough to benefit from it — flag as needing more data than the CNN options to perform well |
| **MobileNet (V2/V3)** | Lightweight backbone, esp. for the Quality Model or on-device scenarios | Fastest inference option; lowest ceiling on accuracy |

### Detection / segmentation candidates

| Architecture | Typical role here | Notes |
|---|---|---|
| **YOLOv8-seg** | Leaf segmentation (Stage 1) | Already the working assumption from earlier architecture discussion; fast, well-supported |
| **Segment Anything (SAM) — pseudo-labeling only** | Generating segmentation masks for datasets that lack them (most of ours besides PlantSeg) | Not a deployed model — a data-engineering tool for Phase 4, not itself a registry-eligible production model |
| **U-Net variants** | Alternative leaf segmentation architecture | Worth a comparison point against YOLOv8-seg specifically on field-image accuracy, not just lab accuracy |

### Crop classifier candidates

Same backbone list as disease detection (EfficientNet/ConvNeXt/MobileNet) — a much
smaller output space (6 classes + unknown) than disease detection, so a lighter backbone
than the disease model may be entirely sufficient. Confirm with the pilot run (Step 10
in the dataset roadmap) rather than assuming.

### Quality model candidates

Lightweight binary/multi-class classifier (blurry / dark / no-leaf / acceptable) —
MobileNet-class backbone is almost certainly sufficient; this stage doesn't need
disease-detection-grade capacity.

---

## Registry

*(Empty — no models trained yet. First row gets added once the Step 10 pilot training
run in the dataset roadmap actually happens.)*

| Model ID | Architecture | Stage / Role | Training Data Version | Accuracy (macro F1) | Date | Git Commit | Weights |
|---|---|---|---|---|---|---|---|
| | | | | | | | |

### Example row (illustrative only — not a real entry, delete before first real use)

| Model ID | Architecture | Stage / Role | Training Data Version | Accuracy (macro F1) | Date | Git Commit | Weights |
|---|---|---|---|---|---|---|---|
| `disease-percrop-tomato-001` | EfficientNet-B0 | Disease detection — Per-Crop approach, Tomato | AgroVision Dataset v1.0 | 0.87 (macro F1); field-only subset: 0.79 | 2026-08-15 | `a1b2c3d` | `s3://agrovision-models/disease-percrop-tomato-001.pt` |

Note the row reports **both blended and field-only accuracy** — consistent with
`03_AgroVision_Standards.md`'s Experiment Standards requirement to report domains
separately, not just a blended number.