# AgroVision AI — Project Phases Checklist

**Document type:** Implementation roadmap
**Project:** AgroVision AI
**Version:** 1.1
**Scope:** Aligned to the current repository state and current V1 crop scope.

## Current V1 scope

AgroVision V1 currently targets five crops:

- Tomato
- Potato
- Corn
- Apple
- Grape

Anything outside these five is treated as `Unknown Crop` rather than forced into the nearest supported class.

## Current repository evidence

The codebase already contains:

- documentation and scope files under [docs](docs)
- dataset inventory parsing for PlantVillage, PlantDoc, PlantWild, and PlantSeg
- inventory tests under [tests/test_dataset_inventory.py](tests/test_dataset_inventory.py)
- shared normalization logic in [scripts/utilities/label_normalization.py](scripts/utilities/label_normalization.py)

The repository does not yet contain a completed manifest-ingestion pipeline, training pipeline, backend service, or mobile app implementation.

---

## Phase checklist

### Phase 0 — Scope and architecture definition
- [x] Project purpose and scope are documented.
- [x] Supported crops and out-of-scope features are described.
- [x] The system flow is described in the docs.
- [x] The mobile, backend, model, and knowledge-base roles are separated conceptually.

Evidence: [docs/01_Project_Scope.md](docs/01_Project_Scope.md), [docs/05_API_Contract.md](docs/05_API_Contract.md), [docs/07_architecture.md](docs/07_architecture.md)

### Phase 1 — Repository and documentation setup
- [x] Repository structure is established.
- [x] Core documentation files exist.
- [x] The project has a clear docs and scripts layout.

Evidence: [README.md](README.md), [docs](docs), [scripts](scripts), [tests](tests)

### Phase 2 — Dataset acquisition and read-only inventory
- [x] Inventory pipeline exists.
- [x] Dataset-specific parsers exist for the approved sources.
- [x] Inventory tests pass.
- [x] Inventory outputs are generated for the local datasets.
- [x] Canonical snake_case naming is now enforced for inventory outputs.
- [ ] Final parser edge cases and metadata reconciliation are fully closed.

Evidence: [scripts/utilities/dataset_inventory.py](scripts/utilities/dataset_inventory.py), [scripts/parsers](scripts/parsers), [outputs/inventory](outputs/inventory)

### Phase 3 — Taxonomy verification and label mapping
- [ ] Source labels have been fully verified against the taxonomy.
- [ ] Canonical mapping rules exist for all approved datasets.
- [ ] Ambiguous labels have been resolved or explicitly excluded.
- [ ] The taxonomy is promoted from draft to verified for ingestion.

### Phase 4 — Unified manifest ingestion
- [ ] A manifest builder or ingestion pipeline exists.
- [ ] Inventory rows are converted into manifest rows with canonical labels, IDs, license tiers, and provenance.
- [ ] CSV and Parquet manifest outputs are generated.
- [ ] The manifest is treated as the single source of truth.

### Phase 5 — Dataset engineering
- [ ] Quality filtering is implemented.
- [ ] Deduplication is implemented.
- [ ] Splits are assigned safely at the collection level.
- [ ] A frozen dataset version is created.
- [ ] A pilot baseline run is completed.

### Phase 6 — Baseline vision models
- [ ] A simple crop or disease baseline model exists.
- [ ] Training configuration and metrics reporting exist.
- [ ] Confidence behavior and abstention handling are evaluated.

### Phase 7 — Architecture comparison
- [ ] Multiple architecture variants are compared on the same frozen dataset.
- [ ] A production candidate is selected with evidence.

### Phase 8 — Model packaging and cloud inference preparation
- [ ] Model weights and metadata are versioned.
- [ ] Class mappings and calibration metadata are saved.
- [ ] A repeatable inference entry point exists.

### Phase 9 — FastAPI backend
- [ ] A backend service exists.
- [ ] The prediction endpoint is implemented.
- [ ] Model inference and response formatting are wired together.

### Phase 10 — Knowledge base and RAG
- [ ] Verified recommendation records exist for supported diseases.
- [ ] Retrieval and explanation flow are implemented.
- [ ] The LLM is constrained to explain retrieved information rather than invent it.

### Phase 11 — React Native mobile app
- [ ] The mobile app can capture or upload images.
- [ ] The app calls the backend and displays results.
- [ ] Failure states and low-confidence behavior are handled.

### Phase 12 — Cloud deployment
- [ ] The backend is deployed over HTTPS.
- [ ] Model packages and environment configuration are deployed securely.
- [ ] The mobile app can reach the deployed API.

### Phase 13 — End-to-end evaluation
- [ ] Field-image evaluation is performed.
- [ ] End-to-end accuracy and latency are reported.
- [ ] Known limitations are documented.

### Phase 14 — Final documentation and submission
- [ ] The final report, architecture summary, and demo assets are prepared.
- [ ] The repository is submission-ready and documented for others to run.

---

## Recommended next milestone

The next logical milestone is to move from Phase 2 into Phase 3:

1. finalize taxonomy mapping rules
2. define manifest ingestion requirements
3. start manifest generation using canonical labels
4. document unresolved labels before training begins

Do not start model training until the manifest and taxonomy mapping are in place.
