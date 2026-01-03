# Appendix D: Segmentation Methods and Parameters (No Semantic Overreach)

[[A_World_Burning/README]] | [[A_World_Burning/30-whitepaper-toc]] | [[A_World_Burning/26-whitepaper-skeleton]]

This appendix defines how segmentation is used in _The Burning World_ as a **structural instrument**: it decomposes plates into regions so that variance becomes measurable, without prematurely asserting “what the regions mean.”

Segmentation outputs are treated as **derived artifacts** produced by **sealed runs**. No segmentation result is ever an identity record.

Related:

- Filesystem + run sealing: `33-appendix-b-filesystem-naming-run-ids.md`
- Feature inventory (what segmentation enables downstream): `34-appendix-c-feature-extraction-inventory.md`
- Model registry: `29-model-library.md`

---

## D.1 Principles (what segmentation is and is not here)

Segmentation is used to:

- isolate **foreground/background** to stabilize measurements (color, texture, embeddings)
- generate **region proposals** for region-level statistics
- enable “whole vs part” comparisons (plate embedding vs bird-only vs flora-only)
- expose **variance modes** that are invisible in global features (border, paper tone, damage visibility)

Segmentation is not used to:

- claim authoritative semantic labels (species, object identity, intent)
- retroactively “restore” or correct a plate
- collapse multiple variants into a single “best” mask

---

## D.2 Model families (registry + admissibility)

Models enter the pipeline only under the admission rules in `29-model-library.md`:

- pinned weights (model sha / revision)
- license recorded (or explicitly unknown)
- preprocessing declared
- failure modes declared

### D.2.1 Class-agnostic mask generation (preferred first layer)

Primary family:

- SAM v1 (mask-generation)
- SAM-HQ (mask-generation; optional upgrade)

Output: many overlapping candidate masks, each with geometry + quality metrics where available.

Use: **structure extraction without semantics**.

### D.2.2 Semantic segmentation (only when classes are required)

Optional family:

- Mask2Former (ADE20K semantic; “sky/ground/water”-style channels)

Use: additional weak channels when you need them (e.g., “sky-dominant plates”), but keep it explicitly separate from the class-agnostic pipeline.

### D.2.3 Lightweight foreground/background baselines (sanity checks)

Optional:

- U2-Net–style foreground extraction

Use: fast baseline and failure detector (when SAM explodes into thousands of fragments due to engraving texture).

---

## D.3 Input policies (the segmentation “geometry contract”)

Segmentation becomes meaningless if image geometry is inconsistent. Every segmentation run must declare:

### D.3.1 Which pixels were segmented

One of:

- source image bytes (recommended for “truth runs”)
- standardized working raster (if you adopt a fixed working-resolution regime)
- tile set (for ultra-large plates)

Declare:

- source/variant checksum used
- any resize policy (fit/cover, interpolation)
- any border policy (none / crop to content / mask border)

### D.3.2 Resizing and tiling policy

Constraints (practical):

- Many segmentation backbones expect a canonical input scale (often ~1024 on the long side for SAM-like families).
- Very large plates may require tiling to avoid VRAM explosion.

Policy must specify:

- max edge length for segmentation input
- tiling grid and overlap (if tiling)
- merge strategy across tiles (NMS/dedup or union-of-masks with provenance preserved)

### D.3.3 Color management and dtype

Declare:

- colorspace conversion policy (ICC handling)
- dtype and precision (fp16/bf16/fp32)

Reason: these choices measurably affect mask boundaries on engraving textures.

---

## D.4 SAM-style mask generation parameters (record, don’t improvise)

SAM pipelines expose a parameter surface that strongly affects:

- mask count (explosion vs under-segmentation)
- fragmentation (engraving texture sensitivity)
- boundary tightness

Every SAM-style run must record its mask generator parameters (names depend on implementation, but the conceptual parameters recur):

### D.4.1 Sampling density and proposal strategy

- points sampling density (e.g., “points_per_side”)
- crop pyramid settings (if using multi-crop generation)
- overlap settings between crops

### D.4.2 Quality thresholds

- predicted IoU threshold
- stability score threshold
- minimum region area (in pixels)

### D.4.3 Deduplication / suppression

- NMS threshold (box or mask IoU)
- near-identical mask collapse policy (keep-best vs keep-all-with-rank)

---

## D.5 Post-processing and canonical segment sets

Raw mask sets are not the end state. The project needs a disciplined way to create:

- **a preserved raw mask set** (evidence of what the instrument output)
- **a canonical usable mask set** (for downstream measurement and browsing)

### D.5.1 Required: preserve raw output

For each segmentation run, store the raw outputs as produced, with no destructive edits:

- mask files (PNG/RLE) + checksums
- mask metadata (area, bbox, any confidence/stability fields)

### D.5.2 Optional: derive a pruned mask set (separate run)

If you prune or select masks, treat pruning as a separate derived run so you can:

- change pruning policy without falsifying the raw instrument output

Common pruning strategies (declare the one used):

- keep top-k masks by area
- keep masks above a stability threshold
- keep a stratified set (small/medium/large)
- reject masks that are mostly border/paper (if border policy exists)

---

## D.6 Output formats and storage

### D.6.1 Segment identifiers

Within a run:

- `segment_id` is stable and deterministic (e.g., `mask-0001`, `mask-0002`, …)
- segment IDs are not stable across runs; stability is provided by run provenance

### D.6.2 Recommended mask encodings

Store at least one:

- PNG binary mask (simple, debuggable)
- COCO RLE (compact, standard)
- polygon approximations (only as derived; see vectorization in Appendix C)

### D.6.3 Required ledger linkage

Every mask must be resolvable from `segments.parquet`:

- `mask_ref` (relative path)
- `mask_sha256`
- geometry fields (bbox, area)

---

## D.7 Known failure modes (Audubon-specific)

Audubon plates are an adversarial domain for generic segmenters because they contain:

- dense engraving micro-lines
- paper borders and tone fields
- printed inscriptions
- foxing/staining that looks like texture/foreground

Common failure patterns:

- **mask fragmentation**: tiny masks covering engraving strokes
- **border capture**: large masks that treat mat/border as object
- **text confusion**: inscription treated as “object” repeatedly
- **variant drift**: different digitizations change contrast, shifting mask boundaries

Mitigations (all must be recorded as policy, not informal tweaks):

- standardize input geometry (border policy)
- gate masks by minimum area and stability
- run a dedicated “text/border mask” detector if needed, but keep it explicitly separate

---

## D.8 Integration: segmentation as a measurement multiplier

Once segmentation exists, the extraction inventory expands safely:

- compute region-level color/texture/frequency stats
- compute region-level embeddings (CLIP/DINO/SigLIP) with declared crop policy
- compute compositional ratios (bird-like region vs flora-like region vs paper)

The important discipline is that segmentation outputs are never treated as meaning; they are treated as **registered structure** that makes variance comparable.
