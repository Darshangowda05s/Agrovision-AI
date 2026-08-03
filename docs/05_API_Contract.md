# 05 — API Contract (Draft)

This defines the request/response shape for the eventual FastAPI backend (Phase 7), so
the mobile app (Phase 8) and backend can be built against a stable contract instead of
whatever shape falls out of however the pipeline happens to be implemented. **No FastAPI
code exists yet** — this is a design document, not documentation of a running service.

## Design principle

Every response is keyed on stable IDs (`crop_id`, `disease_id`, `recommendation_id`),
never on display strings alone. Display strings can be localized, renamed, or restyled
without breaking any client that parses the response — clients should treat `disease`
and `crop` as human-readable labels for display, and `disease_id`/`crop_id` as what
they actually key logic on.

## `POST /predict`

### Request

```json
{
  "image": "<base64-encoded image data>",
  "crop": "tomato"
}
```

- `image` — required.
- `crop` — optional. If provided and it matches one of the five supported crops, the
  crop-classification stage is skipped entirely (see `01_Project_Scope.md`'s
  crop-selection UX decision). If omitted or unrecognized, auto-classification runs.

### Response — successful diagnosis

```json
{
  "status": "success",
  "taxonomy_version": "1.1",
  "crop": "tomato",
  "crop_id": "TOM",
  "disease": "late_blight",
  "disease_id": "TOM004",
  "confidence": 0.97,
  "domain_estimate": "field",
  "recommendation_id": null,
  "recommendation": null
}
```

- `recommendation_id` / `recommendation` are `null` until Phase 4 (Knowledge Base) and
  Phase 5 (LLM explanation layer) exist. The field is present now so clients don't need
  a schema migration later — they should already handle a null recommendation gracefully.
- `domain_estimate` is informational (was this image more lab-like or field-like in
  character) — not a hard gate, just useful for logging/analytics on real-world usage.
- `taxonomy_version` ties every response to the exact version of `04_Taxonomy.md` it was
  produced under, so if the taxonomy changes later, historical responses remain
  interpretable against the version that generated them.

### Response — unrecognized crop

```json
{
  "status": "unknown_crop",
  "taxonomy_version": "1.1",
  "crop": null,
  "crop_id": "UNK",
  "disease": null,
  "disease_id": null,
  "confidence": null,
  "message": "This crop is not supported by AgroVision v1."
}
```

### Response — recognized crop, unrecognized/low-confidence disease

```json
{
  "status": "unknown_disease",
  "taxonomy_version": "1.1",
  "crop": "tomato",
  "crop_id": "TOM",
  "disease": null,
  "disease_id": "TOM-UNK",
  "confidence": 0.31,
  "message": "The crop was recognized, but the disease is outside AgroVision v1's supported disease set for tomato."
}
```

### Response — image quality too low to proceed

```json
{
  "status": "low_confidence_recapture_needed",
  "taxonomy_version": "1.1",
  "crop": null,
  "disease": null,
  "confidence": null,
  "message": "The image quality is insufficient for reliable diagnosis. Please capture a clearer image of a single leaf in good lighting."
}
```

This response can occur before crop identification even runs (Stage 0 quality gate) —
it isn't specific to disease-detection confidence.

## Status enum (exhaustive — clients should handle all four, not just `success`)

| Status | Meaning |
|---|---|
| `success` | Full diagnosis produced above the confidence threshold |
| `unknown_crop` | Crop not in the supported five, or crop classifier confidence too low |
| `unknown_disease` | Crop recognized, disease not in that crop's taxonomy or below threshold |
| `low_confidence_recapture_needed` | Image quality gate failed — nothing downstream ran |

## Open items for this document

- [ ] Batch prediction endpoint (multiple leaves in one photo) — not designed yet;
      current contract assumes one leaf/prediction per request.
- [ ] Auth/rate-limiting scheme — out of scope for this document, belongs in a backend
      design doc once Phase 7 starts.
- [ ] Whether `recommendation` (once populated) is plain text, structured
      (symptoms/causes/treatment/organic-alternatives as separate fields), or both —
      revisit once Phase 4's knowledge base schema exists.
