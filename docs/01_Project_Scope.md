# 01 — Project Scope

## What AgroVision is

AgroVision is a modular AI system that:

1. Accepts a leaf photo from a user (mobile app).
2. Checks whether the image is usable (quality gate — not too blurry, dark, or
   leaf-absent).
3. Identifies the crop — either the user tells it directly, or a classifier infers it.
4. Detects the disease affecting that specific crop.
5. Reports a confidence level, and asks for a better photo instead of guessing when
   confidence is low.
6. Retrieves verified treatment information from a knowledge base and uses an LLM only to
   explain that retrieved information in plain language — the LLM does not diagnose and
   does not invent treatment advice.

## Supported crops — Version 1

AgroVision v1 is intentionally scoped to six crops to maximize dataset quality,
experimental reproducibility, and model reliability within the constraints of a
final-year project — not because six is a target number in itself, but because it's
the largest scope where every crop can still get properly verified data, a real
field-image test set, and a defensible per-crop taxonomy (see `04_Taxonomy.md`).

| Crop | Rationale |
|---|---|
| Tomato | Best dataset coverage across all sources; high disease diversity |
| Potato | Strong coverage; economically important |
| Rice | **Not present in PlantVillage** — deliberately included to force us to build
  a real field-image pipeline instead of leaning on lab data |
| Corn | Strong field-image coverage (FieldPlant, PlantDoc) |
| Apple | Good lab + field coverage |
| Grape | Weakest field-image coverage of the six — flagged as a risk to monitor,
  not a reason to drop it yet |

**Provisional, not final:** Apple's place in this list is not fully locked. If the
disease-level inventory (Step 4 below) shows a materially stronger public data situation
for an alternative crop with comparable relevance to target users, that swap will be
made *based on that evidence*, and documented here with the reasoning. Absent that
evidence, Apple stays.

Anything outside these six is labeled `Unknown Crop` at inference time — we do not force
an out-of-scope crop into the nearest of the six.

## Supported diseases

**Not yet finalized.** This is the subject of `docs/04_Taxonomy.md`, which is explicitly
the next task before any data collection or preprocessing begins. Locking crops before
diseases, and diseases before data collection, is deliberate: get the taxonomy wrong and
every downstream step (labeling, training, evaluation) has to be redone.

## What "Version 1" does NOT include

Explicitly out of scope for this phase, to prevent scope creep:

- **Severity estimation.** The manifest reserves a `severity` column, and the taxonomy
  should leave room for it conceptually, but no severity model is being built in V1.
  Reason: no source dataset in our inventory has severity ground truth — this needs a
  dedicated annotation effort that hasn't started.
- **Crops beyond the six above.**
- **Multi-language support** in the app (flagged as future work in Phase 6).
- **On-device/offline inference.** Assumed cloud-backend for V1; revisit if
  connectivity constraints in the target user base turn out to require it.

## Roadmap (high-level phases)

1. **Design** — architecture, scope, dataset inventory. *Mostly complete.*
2. **Document** — this doc set. *In progress (this sprint).*
3. **Collect & inventory data** — see `docs/02_Data_Inventory.md`.
4. **Engineer the dataset** — cleaning, deduplication, taxonomy mapping, splitting,
   freezing.
5. **Train baseline models** — image quality, leaf segmentation, crop classification,
   disease detection.
6. **Compare architectures** — universal vs. per-crop vs. shared-backbone disease models.
7. **Build the backend** — FastAPI service tying the pipeline together.
8. **Build the mobile app** — React Native client.
9. **Deploy and evaluate** — against the real-field-image test set specifically, not
   just aggregate validation accuracy.

We do not start phase N+1 with phase N still open. This has already changed the plan
several times (dataset architecture, crop-selection UX, licensing tiers) — that's
expected and healthy at the design stage. Once Phase 4 (dataset freeze) happens, changes
become expensive, which is exactly why phases 1–4 get this much scrutiny up front.

## Open decisions log

Track decisions that were revisited here, so the reasoning isn't lost:

| Decision | Original plan | Revised to | Why |
|---|---|---|---|
| Dataset organization | One merged dataset | One manifest, filterable per crop | Per-crop source mixes differ too much (e.g. Rice has no PlantVillage data) to justify physically separate folders, but Phase 6 (universal model experiment) needs all crops in one place anyway |
| Crop identification | Auto-classify every image | User confirms crop if known, auto-classify only as fallback | Most users already know their crop; removes an unnecessary failure mode |
| Licensing (PlantWild/PlantSeg) | Undecided | Evaluation-only, not training, by default | Both are CC BY-NC-ND; conservative default until final call is made on public release plans — **see `docs/03_AgroVision_Standards.md` for how to override this** |
