# Scope and Inventory Reconciliation — 2026-08-03

**Checkpoint:** V1 scope and documentation reconciled against the local inventory outputs.

## Decisions recorded

- Rice is removed from AgroVision V1. It is not a supported crop, disease-taxonomy crop,
  or crop-classifier target. The intended primary Rice dataset is unavailable.
- V1 supports Tomato, Potato, Corn, Apple, and Grape.
- The raw local copies may still contain Rice and other out-of-scope images. They are
  retained as source artifacts, not V1 training data.

## Evidence confirmed

- PlantVillage: 49,886 readable images.
- PlantDoc: 2,552 readable images.
- PlantWild: 11,358 readable images.
- PlantSeg: 11,458 readable JPG images and 11,458 readable PNG masks.
- The four local inventories contain all five V1 crops. PlantWild and PlantSeg remain
  evaluation-only under the license policy.

## Work that is still open

1. Decide whether `TOM007` (spider mites) is retained as a V1 diagnostic class.
2. Spot-check the ambiguous PlantDoc `Corn leaf blight` mapping.
3. Independently verify pathology names before user-facing use.
4. Collect out-of-scope crop images for `UNK` training.
5. Reconcile PlantSeg metadata and image/mask relationships.
6. Implement label mapping, quality filtering, duplicate detection, split assignment,
   and the versioned manifest.

No model training, backend implementation, or live mobile-to-backend integration has
started at this checkpoint.
