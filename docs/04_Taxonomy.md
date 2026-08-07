# 04 — AgroVision Taxonomy (Version 1.1)

**Status: Evidence-backed draft — local PlantVillage, PlantDoc, PlantWild, and PlantSeg
inventories were checked on 2026-07-31.** Exact native labels and five-crop overlap are
now recorded from the local files. This remains a draft because ambiguous semantic
mappings, pathology attributions, `UNK` training data, and formal quality/deduplication
work have not yet been completed.

This document answers one question, exactly: **what can AgroVision diagnose?** If a
disease or crop isn't in this document, AgroVision does not diagnose it — it returns
`Unknown Crop` or `Unknown Disease` instead of guessing.

## Why every crop and disease has a stable ID

Names get renamed. IDs don't. If `yellow_leaf_curl_virus` is later renamed to
`tomato_yellow_leaf_curl_virus` for clarity, every downstream system (manifest rows,
trained model output layers, the recommendation knowledge base, analytics) keeps working
unchanged because it was keyed on `TOM009`, not the display string. Treat the ID column
as permanent once assigned; treat the name column as free to improve.

---

## Crop Information

| Crop ID | Crop | Scientific Name | Supported | Auto-Detect | Has PlantVillage coverage? |
|---|---|---|---|---|---|
| `APL` | Apple | *Malus domestica* | ✅ | ✅ | ✅ |
| `COR` | Corn (Maize) | *Zea mays* | ✅ | ✅ | ✅ |
| `GRA` | Grape | *Vitis vinifera* | ✅ | ✅ | ✅ (lab); weak field coverage — flagged risk |
| `POT` | Potato | *Solanum tuberosum* | ✅ | ✅ | ✅ |
| `TOM` | Tomato | *Solanum lycopersicum* | ✅ | ✅ | ✅ |
| `UNK` | *(any crop outside the five above)* | — | ❌ | — (falls out here as a rejection, not a prediction) | — |

Crop IDs are assigned alphabetically by crop name — an arbitrary but stable and
unambiguous convention, chosen so nobody has to remember why Tomato is "C001" instead of
"C006."

---

## Disease Taxonomy — Per Crop

Columns: `Disease ID | Canonical Label | Pathogen / Cause | Source Label(s) | Source
Dataset | Recommendation ID`.

`Recommendation ID` is a **reserved placeholder column, not yet populated** — Phase 4
(Knowledge Base) hasn't been built yet, so there's nothing to link to. The column exists
now so that when Phase 4 does exist, disease→recommendation mapping is a lookup, not a
schema change. Leave every `Recommendation ID` cell as `TBD` until Phase 4 starts.

Diseases marked `PEST` under Pathogen/Cause are flagged, not silently included — see the
note on `TOM007` (spider mites) below.

### Tomato (`TOM`)

| Disease ID | Canonical Label | Pathogen / Cause | Source Label(s) | Source Dataset | Recommendation ID |
|---|---|---|---|---|---|
| `TOM001` | `healthy` | — | `Tomato___healthy`; `Tomato___Tomato leaf` | PlantVillage; PlantDoc | TBD |
| `TOM002` | `bacterial_spot` | *Xanthomonas* spp. (*vesicatoria*/*perforans* complex) | `Tomato___Bacterial_spot`; `Tomato___Tomato leaf bacterial spot` | PlantVillage; PlantDoc | TBD |
| `TOM003` | `early_blight` | *Alternaria solani* | `Tomato___Early_blight`; `Tomato___Tomato Early blight leaf` | PlantVillage; PlantDoc | TBD |
| `TOM004` | `late_blight` | *Phytophthora infestans* | `Tomato___Late_blight`; `Tomato___Tomato leaf late blight`; `late-blight`; `LB` | PlantVillage; PlantDoc; generic/scraped | TBD |
| `TOM005` | `leaf_mold` | *Passalora fulva* (syn. *Fulvia fulva*) | `Tomato___Leaf_Mold`; `Tomato___Tomato mold leaf` | PlantVillage; PlantDoc | TBD |
| `TOM006` | `septoria_leaf_spot` | *Septoria lycopersici* | `Tomato___Septoria_leaf_spot` | PlantVillage | TBD |
| `TOM007` | `spider_mites` | *Tetranychus urticae* (**pest, not a pathogen** — see note below) | `Tomato___Spider_mites_Two_spotted_spider_mite` | PlantVillage | TBD |
| `TOM008` | `target_spot` | *Corynespora cassiicola* | `Tomato___Target_Spot` | PlantVillage | TBD |
| `TOM009` | `yellow_leaf_curl_virus` | Tomato yellow leaf curl virus (TYLCV) | `Tomato___Tomato_YellowLeaf__Curl_Virus`; `Tomato___Tomato leaf yellow virus` | PlantVillage; PlantDoc | TBD |
| `TOM010` | `mosaic_virus` | Tomato mosaic virus (ToMV) | `Tomato___Tomato_mosaic_virus`; `Tomato___Tomato leaf mosaic virus` | PlantVillage; PlantDoc | TBD |
| `TOM-UNK` | `unknown_disease` | — | *(anything not above)* | any | N/A |

**Note on `TOM007`:** spider mites are a pest, not a pathogen — carried over here
unchanged from PlantVillage/PlantDoc's own classification as a "disease" class, since
excluding it would break compatibility with those source datasets' existing labels.
Needs an explicit team decision: keep it as a classified "disease" class for V1
(pragmatic — the images exist and the visual pattern is distinct), or exclude it
and add a separate `pest` taxonomy category in a future version.

### Potato (`POT`)

| Disease ID | Canonical Label | Pathogen / Cause | Source Label(s) | Source Dataset | Recommendation ID |
|---|---|---|---|---|---|
| `POT001` | `healthy` | — | `Potato___healthy` | PlantVillage | TBD |
| `POT002` | `early_blight` | *Alternaria solani* | `Potato___Early_blight`; `Potato___Potato leaf early blight` | PlantVillage; PlantDoc | TBD |
| `POT003` | `late_blight` | *Phytophthora infestans* | `Potato___Late_blight`; `Potato___Potato leaf late blight` | PlantVillage; PlantDoc | TBD |
| `POT-UNK` | `unknown_disease` | — | *(anything not above)* | any | N/A |

### Corn / Maize (`COR`)

| Disease ID | Canonical Label | Pathogen / Cause | Source Label(s) | Source Dataset | Recommendation ID |
|---|---|---|---|---|---|
| `COR001` | `healthy` | — | `Corn_(maize)___healthy` | PlantVillage | TBD |
| `COR002` | `gray_leaf_spot` | *Cercospora zeae-maydis* | `Corn_(maize)___Cercospora_leaf_spot Gray_leaf_spot`; `Corn___Corn Gray leaf spot` | PlantVillage; PlantDoc | TBD |
| `COR003` | `common_rust` | *Puccinia sorghi* | `Corn_(maize)___Common_rust_`; `Corn___Corn rust leaf` | PlantVillage; PlantDoc | TBD |
| `COR004` | `northern_leaf_blight` | *Exserohilum turcicum* (syn. *Setosphaeria turcica*) | `Corn_(maize)___Northern_Leaf_Blight`; `Corn___Corn leaf blight` ⚠️ | PlantVillage; PlantDoc | TBD |
| `COR-UNK` | `unknown_disease` | — | *(anything not above)* | any | N/A |

⚠️ PlantDoc's generic `Corn leaf blight` label needs a manual image spot-check before
assuming it always maps to Northern Leaf Blight specifically. **Additional candidate
classes** seen in field-specific corn datasets (CD&S, "Disease of Maize in the Field") —
e.g. Maize Streak Virus or further rust/blight subtypes — are **not** added here until
someone has opened that dataset and confirmed the label set.

### Apple (`APL`)

| Disease ID | Canonical Label | Pathogen / Cause | Source Label(s) | Source Dataset | Recommendation ID |
|---|---|---|---|---|---|
| `APL001` | `healthy` | — | `Apple___healthy`; `Apple___Apple leaf` | PlantVillage; PlantDoc | TBD |
| `APL002` | `apple_scab` | *Venturia inaequalis* | `Apple___Apple_scab`; `Apple___Apple Scab Leaf` | PlantVillage; PlantDoc | TBD |
| `APL003` | `black_rot` | *Botryosphaeria obtusa* | `Apple___Black_rot` | PlantVillage | TBD |
| `APL004` | `cedar_apple_rust` | *Gymnosporangium juniperi-virginianae* | `Apple___Cedar_apple_rust`; `Apple___Apple rust leaf` | PlantVillage; PlantDoc | TBD |
| `APL-UNK` | `unknown_disease` | — | *(anything not above)* | any | N/A |

### Grape (`GRA`)

| Disease ID | Canonical Label | Pathogen / Cause | Source Label(s) | Source Dataset | Recommendation ID |
|---|---|---|---|---|---|
| `GRA001` | `healthy` | — | `Grape___healthy`; `grape___grape leaf` | PlantVillage; PlantDoc | TBD |
| `GRA002` | `black_rot` | *Guignardia bidwellii* | `Grape___Black_rot`; `grape___grape leaf black rot` | PlantVillage; PlantDoc | TBD |
| `GRA003` | `esca_black_measles` | Fungal complex (*Phaeomoniella chlamydospora*, *Phaeoacremonium* spp., *Fomitiporia mediterranea*) | `Grape___Esca_(Black_Measles)` | PlantVillage | TBD |
| `GRA004` | `leaf_blight_isariopsis` | *Pseudocercospora vitis* (syn. *Isariopsis* leaf spot) | `Grape___Leaf_blight_(Isariopsis_Leaf_Spot)` | PlantVillage | TBD |
| `GRA-UNK` | `unknown_disease` | — | *(anything not above)* | any | N/A |

**⚠️ Flagged risk (carried over from the data inventory):** Grape has the weakest
field-image count of the five crops. Confirm during Step 3 that there are enough real
field images per Grape disease class for a meaningful field test set — if not, this list
may need to shrink relative to what the lab data alone would suggest, or Grape's place
in the five may need revisiting per `01_Project_Scope.md`.

---

## Unknown Policy

### Unknown Crop

Any image the crop classifier assigns outside {`TOM`, `POT`, `COR`, `APL`, `GRA`}
— or that falls below the crop classifier's confidence threshold for all five — returns
`crop_id: "UNK"` and:

> "This crop is not supported by AgroVision v1."

Example out-of-scope crops a user might reasonably photograph: Mango, Coffee, Banana,
Cotton, Cassava, Wheat, Soybean, Chili. **None of these are silently mapped to the
nearest of the five supported crops** — a photo of a mango leaf must never be scored
against the Apple disease model just because both are tree fruit.

This category needs real negative training images to function — a classifier can't
learn to say "none of the above" without out-of-scope examples during training.
Sourcing those images is a Step 3 action item, not yet done.

### Unknown Disease

If the crop is correctly identified as one of the five but the disease model's top
prediction falls below the confidence threshold, or the true label genuinely isn't in
that crop's table above, the system returns the crop's `-UNK` disease ID (e.g.
`TOM-UNK`) and:

> "The crop was recognized, but the disease is outside AgroVision v1's supported disease
> set for [crop]."

This is deliberately per-crop rather than one global bucket: a per-crop unknown signal
is diagnostically more useful ("I know this is a tomato, I just don't recognize this
specific pattern") than a global one, and costs nothing extra since the pipeline already
knows the crop by the time disease detection runs.

---

## Evidence and sign-off checklist

- [x] Pull the actual class folder names / label files from PlantVillage and PlantDoc.
      Local inventory outputs confirm the native labels and exposed one label correction:
      PlantVillage uses `Tomato___Tomato_YellowLeaf__Curl_Virus`.
- [x] Confirm PlantWild and PlantSeg's class lists against the five V1 crops. Their
      matching existing labels are evidence for the current taxonomy but remain
      `eval_only`. New or ambiguous labels (for example Corn smut, Apple mosaic virus,
      and Grape downy mildew/leaf spot/leafroll) are explicitly excluded from V1 until
      a future taxonomy decision assigns stable IDs and validates their meaning.
- [ ] Resolve the pest-vs-disease decision for Tomato (`spider_mites`, `TOM007`) —
      team decision, not a data question.
- [ ] Verify the Corn "leaf blight" PlantDoc mapping (`COR004`) against sample images.
- [x] Record available Grape field-image counts. PlantDoc has 69 `grape leaf` and 64
      `grape leaf black rot` images; PlantWild has 122 black rot, 281 downy mildew, 91
      leaf spot, and 71 leafroll images. These counts document the risk but do not by
      themselves establish that every disease class is sufficient for a final test set.
- [ ] Source actual out-of-scope-crop images for the `UNK` crop training class.
- [ ] Double-check pathogen/cause names above against a plant-pathology reference before
      they're used in any user-facing content — they're standard textbook attributions,
      but this document hasn't independently re-verified each one against a primary
      source.

The completed items establish the local evidence base for Phase 4. The Phase 4 manifest
has been generated in `datasets/manifest/manifest.csv`, with raw source labels preserved
and canonical V1 mappings applied. The unchecked items remain required before this
taxonomy becomes the enforced source of truth for a frozen training manifest.
