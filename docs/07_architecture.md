# AgroVision AI — System Architecture (Standalone)

**This file is intentionally kept outside the AgroVision-AI repository docs.** Use it for
presentations, reports, or onboarding — not as a source of truth for implementation
details (that lives in the repo's `docs/` set, particularly `01_Project_Scope.md` and
`05_API_Contract.md`).

## End-to-end pipeline

```
                              ┌───────────────┐
                              │      User      │
                              └───────┬────────┘
                                      │  captures / uploads leaf photo
                                      ▼
                              ┌───────────────┐
                              │  React Native  │
                              └───────┬────────┘
                                      │  POST /predict  (image [+ optional crop])
                                      ▼
                              ┌───────────────┐
                              │    FastAPI     │
                              └───────┬────────┘
                                      ▼
                          ┌───────────────────────┐
                          │     Quality Model      │
                          │ (blur / dark / no-leaf │
                          │   rejection gate)      │
                          └───────────┬───────────┘
                        fail ─────────┤─────────── pass
                          │                          │
                          ▼                          ▼
              ┌─────────────────────┐      ┌───────────────────┐
              │ status:             │      │   Segmentation      │
              │ low_confidence_     │      │  (isolate leaf(es)  │
              │ recapture_needed    │      │   from background)  │
              └─────────────────────┘      └──────────┬─────────┘
                                                         ▼
                                          ┌───────────────────────────┐
                                          │   User supplied crop?     │
                                          └─────────────┬─────────────┘
                                        yes ─────────────┤───────────── no
                                          │                            │
                                          ▼                            ▼
                                    ┌──────────┐          ┌─────────────────────┐
                                    │   Skip    │          │   Crop Classifier    │
                                    └─────┬────┘          └──────────┬──────────┘
                                          │                          │
                                          │             below threshold ──► status: unknown_crop
                                          │                          │
                                          └────────────┬─────────────┘
                                                        ▼
                                             ┌────────────────────┐
                                             │   Disease Model     │
                                             │ (crop-specific head  │
                                             │  or shared backbone) │
                                             └──────────┬─────────┘
                                                        │
                                          below threshold ──► status: unknown_disease
                                                        │
                                                        ▼
                                             ┌────────────────────┐
                                             │  Knowledge Base      │
                                             │      (RAG)           │
                                             └──────────┬─────────┘
                                                        ▼
                                             ┌────────────────────┐
                                             │        LLM           │
                                             │  (explains only —    │
                                             │  does not diagnose)  │
                                             └──────────┬─────────┘
                                                        ▼
                                             ┌────────────────────┐
                                             │      Response         │
                                             │  (see 05_API_Contract │
                                             │   for exact schema)   │
                                             └──────────┬─────────┘
                                                        ▼
                                              back to React Native
                                                 → shown to user
```

## Stage responsibilities (one line each)

| Stage | Responsibility | Failure mode it guards against |
|---|---|---|
| React Native | Capture/upload, display result | — |
| FastAPI | Orchestrate the pipeline, own the API contract | — |
| Quality Model | Reject unusable images before anything else runs | Garbage-in-garbage-out; wasted downstream compute |
| Segmentation | Isolate leaf(es) from background/soil/hands | Background noise corrupting crop/disease predictions |
| Crop Classifier | Identify crop *only if the user didn't already say* | Forcing every image through classification when the user already knows |
| Disease Model | Predict disease **for the confirmed crop only** | Cross-crop confusion from a single monolithic classifier |
| Knowledge Base (RAG) | Retrieve verified treatment info | LLM hallucinating treatment advice from nothing |
| LLM | Explain retrieved info in plain language | LLM diagnosing or inventing facts not in the knowledge base |

## Status quo

This diagram describes the **target** architecture. As of this writing, no stage beyond
dataset/taxonomy design has been implemented — see the AgroVision-AI repo's
`01_Project_Scope.md` roadmap for what phase the project is actually in.