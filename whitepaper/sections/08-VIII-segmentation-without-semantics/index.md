<!-- Auto-generated TOC-aligned file. Source of truth: A_World_Burning/26-whitepaper-skeleton.md -->

# VIII. Segmentation Without Semantics

[[whitepaper/DRAFT]] | [[whitepaper/MATERIALS_MAP]] | [[A_World_Burning/35-appendix-d-segmentation-methods-and-parameters]] | [[A_World_Burning/29-model-library]]

_TOC-aligned entrypoint. Master outline lives in `A_World_Burning/26-whitepaper-skeleton.md`._

---

## Draft (body text)

Segmentation is used here as an instrument for making variance measurable at sub-image scales. The guiding constraint is “segmentation without semantics”: we allow masks and regions, but we refuse to treat the model’s labels (or our own convenient names) as truth claims about the historical object.

### VIII.1 Why class-agnostic masks fit the method

Class-agnostic segmentation (SAM-style region proposals) aligns with the project’s epistemic discipline:

- it decomposes an image into parts without committing to a taxonomy;
- it supports part-level measurement (color drift, contrast, damage visibility, cropping differences);
- it reduces the risk that a pretrained semantic class ontology becomes a hidden editorial authority.

### VIII.2 What segmentation is allowed to claim

Segmentation outputs are allowed to claim only:

- “these pixels form a coherent region under this model/config,” and
- “this region has measured properties (area, bbox, color stats, embeddings).”

Segmentation is not allowed to claim:

- what the region “is” (bird, plant, sky) as documentary fact,
- that the mask is anatomically correct,
- that the model’s classes are stable across institutions or digitization regimes.

### VIII.3 Storage and auditability (masks as run artifacts)

Masks are stored as append-only run outputs (never overwritten), with explicit representation choices:

- inspectable raster masks (PNG) for human audit,
- compact encodings (RLE/JSON) for ledger/index use,
- optional polygons for vector regimes and downstream annotation.

Mask QC becomes part of the measurement layer: distribution of mask counts, fragmentation, dominance ratios, and stability signals are recorded as artifacts, not guessed.

### VIII.4 Segmentation’s role in the manifold

Segmentation is not a separate task; it is a mechanism that makes the manifold richer:

- segment-level embeddings create a part-based similarity space;
- background/text/border decomposition makes pipeline variance visible;
- outlier masks become evidence for digitization or restoration differences.

See: [[A_World_Burning/35-appendix-d-segmentation-methods-and-parameters]] for the full parameter and non-claim inventory.

---

## Sources (internal)

- [[A_World_Burning/35-appendix-d-segmentation-methods-and-parameters]]
- [[A_World_Burning/29-model-library]]
- [[A_World_Burning/27-strange-models-compendium]]

---

## Outline (preserved)
**Purpose:** extract structure without prematurely asserting meaning.

- VIII.1 Why class-agnostic masks (SAM-style) are methodologically aligned
- VIII.2 What segmentation is allowed to claim (and what it is not)
- VIII.3 Segmentation stacks considered
  - VIII.3.a SAM (vit-h primary; vit-l/vit-b fallback)
  - VIII.3.b Mask2Former (when semantic classes are required)
  - VIII.3.c Optional detection support (DETR, GroundingDINO) as scaffolding signals
- VIII.4 Mask representation choices
  - VIII.4.a PNG masks (inspectability)
  - VIII.4.b RLE JSON (compactness; ledger-friendly)
  - VIII.4.c Polygonization (vector regime; COCO polygons)
- VIII.5 Mask QC metrics
  - VIII.5.a segment count distribution
  - VIII.5.b fragmentation/stability measures
  - VIII.5.c largest-segment dominance ratio
  - VIII.5.d boundary uncertainty / â€œambiguous zonesâ€
- VIII.6 Segment-level measurement (stats and embeddings per mask)
- VIII.7 Storage: per-run artifacts + `segments.parquet`

