# 04 — AgroVision Taxonomy (Version 1.1)

**Status: Draft — populated from known public class lists (PlantVillage, PlantDoc,
Paddy Doctor, and related sources), not yet cross-checked against the literal files on
disk.** Before this taxonomy drives Step 4 (label standardization), do the verification
pass in the sign-off checklist at the bottom. Treat every table here as "almost
certainly right" rather than "verified."

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
| `RIC` | Rice | *Oryza sativa* | ✅ | ✅ | ❌ — field-only sources (Paddy Doctor, etc.) |
| `TOM` | Tomato | *Solanum lycopersicum* | ✅ | ✅ | ✅ |
| `UNK` | *(any crop outside the six above)* | — | ❌ | — (falls out here as a rejection, not a prediction) | — |

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
Rice section for the specific open decision this creates.

### Tomato (`TOM`)

| Disease ID | Canonical Label | Pathogen / Cause | Source Label(s) | Source Dataset | Recommendation ID |
|---|---|---|---|---|---|
| `TOM001` | `healthy` | — | `Tomato___healthy`; `Tomato leaf` | PlantVillage; PlantDoc | TBD |
| `TOM002` | `bacterial_spot` | *Xanthomonas* spp. (*vesicatoria*/*perforans* complex) | `Tomato___Bacterial_spot`; `Tomato leaf bacterial spot` | PlantVillage; PlantDoc | TBD |
| `TOM003` | `early_blight` | *Alternaria solani* | `Tomato___Early_blight`; `Tomato Early blight leaf` | PlantVillage; PlantDoc | TBD |
| `TOM004` | `late_blight` | *Phytophthora infestans* | `Tomato___Late_blight`; `Tomato leaf late blight`; `late-blight`; `LB` | PlantVillage; PlantDoc; generic/scraped | TBD |
| `TOM005` | `leaf_mold` | *Passalora fulva* (syn. *Fulvia fulva*) | `Tomato___Leaf_Mold`; `Tomato mold leaf` | PlantVillage; PlantDoc | TBD |
| `TOM006` | `septoria_leaf_spot` | *Septoria lycopersici* | `Tomato___Septoria_leaf_spot` | PlantVillage | TBD |
| `TOM007` | `spider_mites` | *Tetranychus urticae* (**pest, not a pathogen** — see note below) | `Tomato___Spider_mites Two-spotted_spider_mite`; `Tomato two spotted spider mites leaf` | PlantVillage; PlantDoc | TBD |
| `TOM008` | `target_spot` | *Corynespora cassiicola* | `Tomato___Target_Spot` | PlantVillage | TBD |
| `TOM009` | `yellow_leaf_curl_virus` | Tomato yellow leaf curl virus (TYLCV) | `Tomato___Tomato_Yellow_Leaf_Curl_Virus`; `Tomato leaf yellow virus` | PlantVillage; PlantDoc | TBD |
| `TOM010` | `mosaic_virus` | Tomato mosaic virus (ToMV) | `Tomato___Tomato_mosaic_virus`; `Tomato leaf mosaic virus` | PlantVillage; PlantDoc | TBD |
| `TOM-UNK` | `unknown_disease` | — | *(anything not above)* | any | N/A |

**Note on `TOM007`:** spider mites are a pest, not a pathogen — carried over here
unchanged from PlantVillage/PlantDoc's own classification as a "disease" class, since
excluding it would break compatibility with those source datasets' existing labels.
Flagged for the same team decision raised under Rice, since it's the same
pest-vs-disease question appearing in a second crop.

### Potato (`POT`)

| Disease ID | Canonical Label | Pathogen / Cause | Source Label(s) | Source Dataset | Recommendation ID |
|---|---|---|---|---|---|
| `POT001` | `healthy` | — | `Potato___healthy` | PlantVillage | TBD |
| `POT002` | `early_blight` | *Alternaria solani* | `Potato___Early_blight`; `Potato leaf early blight` | PlantVillage; PlantDoc | TBD |
| `POT003` | `late_blight` | *Phytophthora infestans* | `Potato___Late_blight`; `Potato leaf late blight` | PlantVillage; PlantDoc | TBD |
| `POT-UNK` | `unknown_disease` | — | *(anything not above)* | any | N/A |

### Corn / Maize (`COR`)

| Disease ID | Canonical Label | Pathogen / Cause | Source Label(s) | Source Dataset | Recommendation ID |
|---|---|---|---|---|---|
| `COR001` | `healthy` | — | `Corn_(maize)___healthy` | PlantVillage | TBD |
| `COR002` | `gray_leaf_spot` | *Cercospora zeae-maydis* | `Corn_(maize)___Cercospora_leaf_spot Gray_leaf_spot`; `Corn Gray leaf spot` | PlantVillage; PlantDoc | TBD |
| `COR003` | `common_rust` | *Puccinia sorghi* | `Corn_(maize)___Common_rust_`; `Corn rust leaf` | PlantVillage; PlantDoc | TBD |
| `COR004` | `northern_leaf_blight` | *Exserohilum turcicum* (syn. *Setosphaeria turcica*) | `Corn_(maize)___Northern_Leaf_Blight`; `Corn leaf blight` ⚠️ | PlantVillage; PlantDoc | TBD |
| `COR-UNK` | `unknown_disease` | — | *(anything not above)* | any | N/A |

⚠️ PlantDoc's generic `Corn leaf blight` label needs a manual image spot-check before
assuming it always maps to Northern Leaf Blight specifically. **Additional candidate
classes** seen in field-specific corn datasets (CD&S, "Disease of Maize in the Field") —
e.g. Maize Streak Virus or further rust/blight subtypes — are **not** added here until
someone has opened that dataset and confirmed the label set.

### Rice (`RIC`)

No PlantVillage coverage — this list is drawn entirely from field-condition sources
(primarily Paddy Doctor, cross-referenced against Roboflow Rice Disease Dataset).

| Disease ID | Canonical Label | Pathogen / Cause | Source Label(s) | Source Dataset | Recommendation ID |
|---|---|---|---|---|---|
| `RIC001` | `healthy` | — | `normal` | Paddy Doctor | TBD |
| `RIC002` | `bacterial_leaf_blight` | *Xanthomonas oryzae* pv. *oryzae* | `bacterial_leaf_blight` | Paddy Doctor | TBD |
| `RIC003` | `bacterial_leaf_streak` | *Xanthomonas oryzae* pv. *oryzicola* | `bacterial_leaf_streak` | Paddy Doctor | TBD |
| `RIC004` | `bacterial_panicle_blight` | *Burkholderia glumae* | `bacterial_panicle_blight` | Paddy Doctor | TBD |
| `RIC005` | `blast` | *Magnaporthe oryzae* (syn. *Pyricularia oryzae*) | `blast` | Paddy Doctor | TBD |
| `RIC006` | `brown_spot` | *Cochliobolus miyabeanus* (syn. *Bipolaris oryzae*) | `brown_spot` | Paddy Doctor | TBD |
| `RIC007` | `tungro` | Rice tungro virus complex (RTBV + RTSV) | `tungro` | Paddy Doctor | TBD |
| `RIC008` | `sheath_blight` | *Rhizoctonia solani* | `sheath_blight` | Roboflow Rice Disease Dataset | TBD |
| `RIC-UNK` | `unknown_disease` | — | *(anything not above)* | any | N/A |

**⚠️ Open decision — not yet resolved:** Paddy Doctor also includes `dead_heart` and
`hispa`, both **pest damage, not pathogen disease** (stem borer damage; a beetle
infestation). Currently **excluded** from this table on the reasoning that AgroVision v1
is scoped as disease detection, not pest-and-disease detection. Needs an explicit team
decision: if pests are in scope, add a parallel `pest` taxonomy category (never folded
into `disease` — treatment differs completely); if out of scope, exclude those images
from training entirely rather than mapping them to `unknown_disease`, which would wrongly
teach the model that pest damage looks like "no known disease."

### Apple (`APL`)

| Disease ID | Canonical Label | Pathogen / Cause | Source Label(s) | Source Dataset | Recommendation ID |
|---|---|---|---|---|---|
| `APL001` | `healthy` | — | `Apple___healthy`; `Apple leaf` | PlantVillage; PlantDoc | TBD |
| `APL002` | `apple_scab` | *Venturia inaequalis* | `Apple___Apple_scab`; `Apple Scab Leaf` | PlantVillage; PlantDoc | TBD |
| `APL003` | `black_rot` | *Botryosphaeria obtusa* | `Apple___Black_rot` | PlantVillage | TBD |
| `APL004` | `cedar_apple_rust` | *Gymnosporangium juniperi-virginianae* | `Apple___Cedar_apple_rust`; `Apple rust leaf` | PlantVillage; PlantDoc | TBD |
| `APL-UNK` | `unknown_disease` | — | *(anything not above)* | any | N/A |

### Grape (`GRA`)

| Disease ID | Canonical Label | Pathogen / Cause | Source Label(s) | Source Dataset | Recommendation ID |
|---|---|---|---|---|---|
| `GRA001` | `healthy` | — | `Grape___healthy`; `grape leaf` | PlantVillage; PlantDoc | TBD |
| `GRA002` | `black_rot` | *Guignardia bidwellii* | `Grape___Black_rot`; `grape leaf black rot` | PlantVillage; PlantDoc | TBD |
| `GRA003` | `esca_black_measles` | Fungal complex (*Phaeomoniella chlamydospora*, *Phaeoacremonium* spp., *Fomitiporia mediterranea*) | `Grape___Esca_(Black_Measles)` | PlantVillage | TBD |
| `GRA004` | `leaf_blight_isariopsis` | *Pseudocercospora vitis* (syn. *Isariopsis* leaf spot) | `Grape___Leaf_blight_(Isariopsis_Leaf_Spot)` | PlantVillage | TBD |
| `GRA-UNK` | `unknown_disease` | — | *(anything not above)* | any | N/A |

**⚠️ Flagged risk (carried over from the data inventory):** Grape has the weakest
field-image count of the six crops. Confirm during Step 3 that there are enough real
field images per Grape disease class for a meaningful field test set — if not, this list
may need to shrink relative to what the lab data alone would suggest, or Grape's place
in the six may need revisiting per `01_Project_Scope.md`.

---

## Unknown Policy

### Unknown Crop

Any image the crop classifier assigns outside {`TOM`, `POT`, `COR`, `RIC`, `APL`, `GRA`}
— or that falls below the crop classifier's confidence threshold for all six — returns
`crop_id: "UNK"` and:

> "This crop is not supported by AgroVision v1."

Example out-of-scope crops a user might reasonably photograph: Mango, Coffee, Banana,
Cotton, Cassava, Wheat, Soybean, Chili. **None of these are silently mapped to the
nearest of the six supported crops** — a photo of a mango leaf must never be scored
against the Apple disease model just because both are tree fruit.

This category needs real negative training images to function — a classifier can't
learn to say "none of the above" without out-of-scope examples during training.
Sourcing those images is a Step 3 action item, not yet done.

### Unknown Disease

If the crop is correctly identified as one of the six but the disease model's top
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

## Sign-off checklist (do before Step 4 begins)

- [ ] Pull the actual class folder names / label files from PlantVillage and PlantDoc
      and confirm they match the Source Label columns above exactly (spot-checked from
      memory/public documentation here, not from the literal files yet).
- [ ] Confirm PlantWild and PlantSeg's class lists against these six crops and either
      fold matching classes into the tables above (assigning new Disease IDs, noting
      `eval_only` license_tier) or explicitly exclude non-matching ones.
- [ ] Resolve the pest-vs-disease decision for Rice (`dead_heart`/`hispa`) and Tomato
      (`spider_mites`, `TOM007`) — team decision, not a data question.
- [ ] Verify the Corn "leaf blight" PlantDoc mapping (`COR004`) against sample images.
- [ ] Confirm field-image counts per Grape disease class are sufficient for a real test
      set; flag to revisit crop selection if not.
- [ ] Source actual out-of-scope-crop images for the `UNK` crop training class.
- [ ] Double-check pathogen/cause names above against a plant-pathology reference before
      they're used in any user-facing content — they're standard textbook attributions,
      but this document hasn't independently re-verified each one against a primary
      source.

Only once these are checked does this document stop being "draft" and start being the
enforced source of truth for Step 4.
