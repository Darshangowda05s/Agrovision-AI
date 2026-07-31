# AgroVision AI

A modular, confidence-aware crop disease detection and recommendation system, built to
work on **real-world farmer-captured images** rather than only on curated benchmark datasets.

## Why this project exists

Most crop disease classifiers report 95–99% accuracy on datasets like PlantVillage, then
perform poorly on real phone photos — because those photos have cluttered backgrounds,
inconsistent lighting, multiple leaves per frame, and blur. AgroVision is designed around
that gap from day one, not as an afterthought.

## Core design principles

1. **The AI should never guess confidently when it doesn't know.** Low-confidence
   predictions trigger a re-capture request, not a wrong diagnosis.
2. **Dataset engineering is a first-class deliverable**, not a side task before "the real
   work" of training models. See `docs/`.
3. **Modular pipeline over one monolithic classifier** — image quality check, leaf
   segmentation, crop identification, disease detection, and treatment recommendation are
   separate, independently-improvable stages.
4. **Real-world evaluation is mandatory.** The test set is built to reflect field
   conditions, not lab conditions, even if that means a smaller test set.

## Current status

📋 **Design phase — no models trained yet.** We are deliberately finishing dataset
engineering and documentation before writing any training code. See `docs/01_Project_Scope.md`
for the full roadmap and where we are on it.

## Repository structure

```
AgroVision-AI/
├── docs/                    Project documentation — read this first
│   ├── 01_Project_Scope.md
│   ├── 02_Data_Inventory.md
│   ├── 03_AgroVision_Standards.md
│   ├── 04_Taxonomy.md
│   └── 05_API_Contract.md
├── datasets/
│   ├── raw/                 Untouched downloaded datasets (gitignored — not committed)
│   ├── processed/           Cleaned, standardized images (gitignored — not committed)
│   └── manifest/            The CSV that tracks every image — see 03_AgroVision_Standards.md
├── scripts/
│   ├── preprocessing/       Label standardization, taxonomy mapping
│   ├── quality/             Blur/resolution/corruption filtering
│   ├── deduplication/       Perceptual hashing + near-duplicate detection
│   └── utilities/           Shared helpers
├── models/                  Model training code (not started yet)
├── experiments/             Experiment configs and results (not started yet)
└── backend/                 FastAPI service (not started yet)
```

## Supported crops (Version 1)

Tomato · Potato · Rice · Corn · Apple · Grape

Anything outside these six is classified as `Unknown Crop` rather than forced into the
nearest match. See `docs/01_Project_Scope.md` for why these six were chosen.


