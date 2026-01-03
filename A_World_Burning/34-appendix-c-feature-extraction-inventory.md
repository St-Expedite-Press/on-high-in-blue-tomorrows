# Appendix C: Feature Extraction Inventory (Exhaustive)

[[A_World_Burning/README]] | [[A_World_Burning/30-whitepaper-toc]] | [[A_World_Burning/26-whitepaper-skeleton]]

This appendix is a deliberately exhaustive catalog of the **measured and derived features** that _The Burning World_ may compute during preprocessing, grounded in the project’s two core constraints:

1. **Provenance-first ingestion**: source images are immutable evidence; nothing overwrites them.  
2. **Sealed runs**: every computation is a run that emits append-only artifacts + manifests; ledgers are derived views.

It is intentionally redundant with `A_World_Burning/00_preprocessing_assay.md`, but rewritten as a **paper-ready inventory**: each feature family states (a) what is computed, (b) what artifacts/tables store it, and (c) what it captures and fails to capture.

Related:
- `A_World_Burning/33-appendix-b-filesystem-naming-run-ids.md` (filesystem + run/ID law)
- `A_World_Burning/29-model-library.md` (model registry for embeddings/segmentation)
- `A_World_Burning/00_preprocessing_assay_addendum.md` (prompt registry and packaging/versioning addenda)

---

## C.0 Storage objects referenced by this appendix

This appendix references three kinds of storage objects:

### C.0.1 Plate-local truth (authoritative)

Within `plates_structured/plate-###/`:

- `manifest.json` (identity + provenance pointers; schema-validated)
- `source/` + `source.sha256` (immutable bytes + checksum)
- `derived/…` (deterministic per-plate derived facts; optional but recommended)
- `runs/<run_id>/…` (sealed run artifacts)

### C.0.2 Ledgers (derived, rebuildable)

Within `ledger/` (or `ledgers/` in the formal layout):

- `plates.parquet` (plate-level facts + pointers)
- `runs.parquet` (run provenance)
- `embeddings.parquet` (vectors or vector pointers + model metadata)
- `segments.parquet` (mask geometry + pointers + region stats)

Optional (large-surface-area) ledgers implied by the corpus:

- `tiles.parquet`
- `ocr.parquet`
- `captions.parquet`
- `quality.parquet`
- `forensics.parquet`
- `vectors.parquet`
- `indices.parquet` (or `indices/` folder + `indices.manifest.json`)

### C.0.3 Figures (derived, disposable)

Under `viz/` or `runs/<run_id>/outputs/visuals/`:

- QC sheets
- histograms
- projections (PCA/UMAP/t-SNE)
- exemplar grids

Rule: figures are never the only home of a measurement; they render from JSON/Parquet.

---

## C.1 Naming and units conventions (so features stay comparable)

### C.1.1 Scalar conventions

- Ratios are float in `[0, 1]` and end with `_ratio` (e.g., `clipped_high_ratio`).
- Counts are integers and end with `_count`.
- Angles are degrees unless explicitly stated (`_deg`).
- Pixel areas are absolute pixels (`_px`) unless normalized (`_ratio`).

### C.1.2 Vector conventions

- Store `vector_dim` explicitly for every embedding.
- If vectors are normalized, store:
  - `is_normalized = true`
  - `raw_l2_norm` (computed before normalization) or store raw vector separately.

### C.1.3 Color conventions

- State the working colorspace for each metric (sRGB vs linear RGB vs Lab).
- If an ICC profile exists, record:
  - presence + hash
  - whether conversion to sRGB occurred (and by what library)

---

## C.2 Feature families (inventory)

The categories below mirror the extraction surface area in `A_World_Burning/00_preprocessing_assay.md` (A–M), but each is expressed as:

- **What** (measurements)
- **Where** (artifacts/tables)
- **Captures / ignores** (interpretability + failure modes)

---

## C.A File- and container-level features (even when “no metadata”)

These features treat the image file as an object with bytes, headers, and compression structure. They are crucial for multi-source variance mode because they help detect pipeline drift and silent replacement.

### C.A.1 Byte-level / format signatures

What:

- file size (bytes)
- MIME/container type
- extension vs detected container mismatch
- magic bytes signature
- decode success/failure flags

Where:

- plate-local: `derived/file_signatures.json` (optional)
- ledger: `plates.parquet` columns (recommended):
  - `source_file_bytes`
  - `source_mime`
  - `source_extension`
  - `source_decode_ok`
  - `source_decode_error` (nullable)

Captures / ignores:

- captures packaging differences and corruptions
- ignores image content; purely structural

### C.A.2 Integrity / duplication / lineage

What:

- `sha256` of the immutable source bytes (required)
- optional secondary hashes for dedup/similarity:
  - perceptual hashes (aHash, pHash, dHash, wHash)
  - blockwise hashes (for partial duplicates)
- duplicate candidates (global)

Where:

- plate-local: `source.sha256` (required)
- ledger:
  - `plates.parquet`: `source_sha256`
  - optional `plates.parquet` columns: `phash`, `ahash`, `dhash`, `whash`
- dataset-level:
  - `quality.parquet` or `forensics.parquet` for “near-dup graph”
  - optional `duplicates.parquet` (edge list of near-duplicates)

Captures / ignores:

- captures exact identity and near-duplicate structure
- ignores semantics; useful for variant drift and recompression detection

### C.A.3 Pipeline fingerprints (forensics-lite)

What (JPEG-oriented examples):

- JPEG quantization table fingerprints (hash)
- ICC profile presence + hash
- EXIF/XMP presence flags (often absent for institutional scans)
- progressive vs baseline encoding flags
- chroma subsampling flags

Where:

- plate-local: `derived/container_fingerprints.json` (optional)
- ledger: `plates.parquet` columns (recommended):
  - `jpeg_is_progressive`
  - `jpeg_subsampling`
  - `jpeg_quant_hash`
  - `icc_present`, `icc_hash`

Captures / ignores:

- captures “institution/pipeline signature” drift
- ignores image content except insofar as encoding choices affect it

---

## C.B Global pixel statistics (cheap, surprisingly powerful)

These measurements are computed from the decoded pixel array (possibly at a standardized working resolution, which must be recorded).

### C.B.1 Color / tone / contrast

What:

- per-channel mean/std/min/max (RGB)
- global histograms (optional but repeatedly referenced):
  - RGB histograms (per-channel, fixed bins)
  - luminance histogram
  - optional HSV/Lab histograms (if you need perceptual bins)
- palette summaries (optional):
  - dominant colors (k-means in Lab, etc.)
  - “paper tone” estimate (if border/background is detected)
- luminance stats (mean/std, percentile range)
- clipping ratios near 0 and 255 (`clipped_low_ratio`, `clipped_high_ratio`)
- gamma/tonal curve heuristics (optional)
- dynamic range and contrast proxies:
  - RMS contrast
  - Michelson contrast (optional)
- global entropy and channel entropies

Where:

- plate-local: `derived/input_image.json` (recommended canonical per-plate scalar pack)
- plate-local (if histograms are computed): `derived/input_color_histograms.json`
- ledger: `plates.parquet` columns (recommended):
  - `rgb_mean_r/g/b`, `rgb_std_r/g/b`
  - `luma_mean`, `luma_std`, `luma_p01`, `luma_p99`
  - `clipped_low_ratio`, `clipped_high_ratio`
  - `entropy_global`
  - `working_width_px`, `working_height_px`, `working_colorspace`
  - histogram fields (if stored inline) OR histogram pointers (if stored as JSON blobs)

Captures / ignores:

- captures institutional color/contrast divergence and damage visibility shifts
- ignores spatial structure (where the dark pixels are)

### C.B.2 Texture / sharpness / noise

What:

- Laplacian variance (blur proxy)
- gradient magnitude summary stats
- noise estimates (simple, auditable approximations)
- “paper grain” proxies (optional; engraving-sensitive)

Where:

- plate-local: `derived/input_image.json` or `derived/quality.json`
- ledger: `quality.parquet` (recommended) or `plates.parquet` (if kept minimal)
  - `laplacian_var`
  - `grad_mean`, `grad_std`
  - `noise_sigma_est`

Captures / ignores:

- captures scan focus differences and JPEG smoothing
- confounds engraving texture with noise; must be interpreted comparatively

### C.B.3 Frequency-domain

What:

- radially-averaged power spectrum (summary bins)
- slope/rolloff metrics (high-frequency decay)
- band energy ratios (low/mid/high)

Where:

- plate-local: `derived/frequency.json` (optional)
- ledger: `plates.parquet` or `forensics.parquet`:
  - `fft_slope`
  - `band_energy_low/mid/high`

Captures / ignores:

- captures compression/denoise signatures and “softness”
- ignores semantics; sensitive to borders/mats unless masked or cropped consistently

### C.B.4 Composition geometry (still global)

What:

- edge density
- saliency proxy (classical saliency; optional)
- negative space ratio (proxy; often derived from segmentation later)
- aspect ratio and framing ratios (if borders present)

Where:

- plate-local: `derived/composition.json` (optional)
- ledger: `plates.parquet`:
  - `edge_density`
  - `aspect_ratio`
  - `border_ratio_est` (optional)

Captures / ignores:

- captures framing differences and “blankness”
- weak without segmentation; best treated as pre-segmentation proxies

### C.B.5 Canonical derived working images (standardized resolutions)

What:

- one or more standardized “working” rasters derived from the immutable source:
  - `work_512` (thumbnail)
  - `work_2k` (analysis-friendly)
  - `work_4k` (optional)
- optional border-cropped variants (if a border policy is adopted)
- preview sheets (contact-sheet style)

Where:

- plate-local (recommended):
  - `derived/work_512.png`
  - `derived/work_2048.png`
  - `derived/work_4096.png` (optional)
- or dataset-level caches (allowed but must remain rebuildable):
  - `cache/work_2k.png` (appears in the corpus as an example)
- figures:
  - `viz/input_preview.png`, `viz/qc_sheet.png` (examples referenced in the corpus)

Required provenance fields (store in `derived/input_image.json` or run config):

- source checksum (`source_sha256`)
- resize policy (fit/cover; interpolation)
- colorspace conversion policy (ICC handling)
- border/crop policy (if any)

Captures / ignores:

- captures a stable computational “working surface” that makes runs comparable across machines
- ignores true full-resolution information; do not pretend “work_2k” is the canonical source

---

## C.C Classical CV local features (pre-deep, still useful)

These are optional but can be surprisingly informative in engraving-heavy images, and they are comparatively cheap.

### C.C.1 Keypoints and descriptors

What:

- SIFT/ORB keypoints count and descriptor summaries (if used)
- matchability statistics across variants (optional)

Where:

- run outputs (if computed): `runs/<run_id>/outputs/metrics/keypoints.json`
- optional ledger: `quality.parquet` or `forensics.parquet`

Captures / ignores:

- captures local structure and repeat patterns
- sensitive to scale and border content; must be standardized

### C.C.2 Contours and shape summaries

What:

- edge map thresholds + connected component summaries
- contour count, convexity/solidity proxies

Where:

- plate-local: `derived/contours.json` (optional)
- ledger: `plates.parquet` (optional columns)

Captures / ignores:

- captures “busyness” and fragmentation
- easily dominated by engraving micro-lines; needs careful thresholds

---

## C.D Foundation-model embeddings (the “universal backbone”)

This family defines the canonical manifold geometry. See `A_World_Burning/29-model-library.md` for the pinned model ID set.

### C.D.1 Whole-plate embeddings (global)

What:

- embedding vectors for the full plate image for multiple backbones (CLIP, DINOv2, SigLIP, etc.)
- optional multi-crop embeddings and crop-stability metrics

Where:

- run outputs:
  - `runs/<run_id>/outputs/embeddings/<plate_id>__<run_id>__embedding__<model_alias>.npy`
  - `runs/<run_id>/outputs/metrics/<plate_id>__<run_id>__metric__embedding_norms.json`
- ledger: `embeddings.parquet` (one row per (plate, model, scope))

Minimum `embeddings.parquet` fields (recommended):

- `run_id`, `plate_id`, `variant_id` (nullable)
- `scope` (`plate`)
- `model_id`, `model_sha`
- `preprocess_tag` (resize/crop/mask policy)
- `vector_dim`
- `vector` (inline) OR `vector_ref` (path)
- `is_normalized`, `raw_l2_norm`

Captures / ignores:

- captures broad similarity structure; enables retrieval/clustering
- CLIP-like models import text/web priors; DINOv2 reduces that but has its own biases

### C.D.2 Segment-level embeddings (region embeddings)

What:

- compute an embedding per segment mask:
  - crop policy (tight bbox vs padded vs masked alpha)
  - optionally both “masked” and “unmasked” crops

Where:

- segmentation run produces masks (see C.E), then embedding run consumes masks
- outputs under `runs/<run_id>/outputs/embeddings/` with segment descriptors
- ledger: `embeddings.parquet` rows with `scope = segment` and `segment_id`

Additional fields (recommended):

- `segment_id`
- `bbox_*`
- `mask_ref` (or join key into `segments.parquet`)

Captures / ignores:

- captures “bird-only vs flora-only vs paper-only” manifold structure
- sensitive to mask quality; must record mask provenance

### C.D.3 Tile-level embeddings (patch library)

What:

- compute embeddings on a fixed tiling grid (multi-scale optional)
- store a patch library for searching recurring motifs (beaks, eggs, branches, clouds)

Where:

- optional `tiles.parquet` describing the grid
- embedding records in `embeddings.parquet` with `scope = tile`

Captures / ignores:

- captures motif recurrence and local variance
- very sensitive to tiling scheme; tiling policy becomes part of canon constraints

### C.D.4 Caption/text embeddings (cross-modal retrieval)

What:

- embed generated captions (or OCR text) using a text embedding model
- enables query-by-text and concept browsing without asserting truth

Where:

- `captions.parquet` for text
- `embeddings.parquet` for text vectors (or `text_embeddings.parquet` if separated)

Captures / ignores:

- captures language priors; heavily dependent on prompts and model choice
- must be treated as weak signal

---

## C.E Dense semantics (objects, masks, parts, relationships)

This family ranges from weak detectors to full segmentation. The project preference is to begin with **segmentation without semantics** (class-agnostic masks), then optionally layer semantics later.

### C.E.1 Object detection (open-vocabulary if possible)

What:

- boxes + class logits (DETR) and/or text-conditioned boxes (GroundingDINO)
- counts and spatial relation proxies derived from boxes

Where:

- run outputs: `runs/<run_id>/outputs/metrics/<plate_id>__<run_id>__metric__detections.json`
- optional ledger: `detections.parquet` (if boxes are numerous) or `quality.parquet` (if only scalars)

Captures / ignores:

- captures weak “count” and “where” signals
- imports strong taxonomy priors; treat as scaffolding, not truth

### C.E.2 Instance/semantic segmentation (class maps)

What:

- per-pixel class map (Mask2Former ADE20K or similar)

Where:

- run outputs: `runs/<run_id>/outputs/segments/<plate_id>__<run_id>__segment__<model>__classes.png` (or RLE)
- ledger: `segments.parquet` rows may include `class_id` and `class_name` when semantic

Captures / ignores:

- captures coarse scene classes (sky/ground/water) as weak channels
- ignores domain specificity; ADE20K labels may not map cleanly to engraving plates

### C.E.3 “Segment Anything” masks (class-agnostic; preferred first)

What:

- set of masks per plate, each with:
  - mask encoding (PNG or RLE)
  - bbox, area, centroid
  - stability/quality metrics if available
- post-processing:
  - deduplicate near-identical masks
  - rank/prune (top-k by area, stability, etc.)

Where:

- run outputs:
  - `runs/<run_id>/outputs/segments/<plate_id>__<run_id>__segment__sam-vit-<size>__mask-0001.png`
  - optional: `runs/<run_id>/outputs/metrics/<plate_id>__<run_id>__metric__sam_mask_stats.json`
- ledger: `segments.parquet` (one row per mask)

Minimum `segments.parquet` fields (recommended):

- `run_id`, `plate_id`, `variant_id` (nullable)
- `segment_id` (stable within run; e.g., `mask-0001`)
- `mask_ref` + `mask_sha256`
- bbox fields: `x_min`, `y_min`, `x_max`, `y_max`
- `area_px`, `area_ratio`
- `centroid_x`, `centroid_y` (normalized 0–1 recommended)
- quality fields (optional): `stability_score`, `fragmentation_score`

Captures / ignores:

- captures region decomposition without asserting meaning
- mask sets can explode in count; pruning policy must be recorded

### C.E.4 Keypoints / pose / layout (optional)

What:

- keypoints (if bird pose estimation is attempted)
- layout heuristics (text region boxes, border boxes)

Where:

- optional `metrics/pose.json` and corresponding ledger rows

Captures / ignores:

- captures pose structure if a relevant keypoint model exists
- likely brittle on engraving plates; treat as experimental

### C.E.5 Scene graphs (derived; optional)

What:

- derived relationships between segments/detections (above, overlaps, near)
- stored as edges, not as truth claims

Where:

- optional `graph_edges.parquet` (derived)
- or as a derived export for later graph database ingestion

Captures / ignores:

- captures relational structure useful for browsing and analysis
- extremely sensitive to upstream segmentation/detection errors

---

## C.N Vectorization (explicit second representation regime)

The corpus explicitly calls out a second representation regime: turning raster evidence (edges, masks, regions) into **vector and graph forms** so that “shape” is queryable without rescanning pixels.

### C.N.1 Raster-to-vector from edges (classical)

What:

- edge maps (Canny/Sobel; multi-threshold optional)
- contour extraction and polygon approximation
- simplified polylines for “engraving stroke density” analysis (experimental)

Where:

- run outputs:
  - `runs/<run_id>/outputs/vectors/<plate_id>__<run_id>__vector__edges.svg`
  - `runs/<run_id>/outputs/vectors/<plate_id>__<run_id>__vector__contours.json`
- ledger: `vectors.parquet` (recommended)

Core `vectors.parquet` fields (recommended):

- `run_id`, `plate_id`, `variant_id` (nullable)
- `vector_id`
- `vector_kind` (`edges`, `contour`, `polygon`, `skeleton`, etc.)
- `format` (`svg`, `geojson`, `json`, etc.)
- `vector_ref` + checksum
- summary stats (optional): `path_count`, `total_length_px`, `vertex_count`

Captures / ignores:

- captures geometry in a portable form; enables “shape-first” browsing
- easily dominated by engraving micro-lines; requires a documented simplification policy

### C.N.2 Mask-to-polygon (from segmentation)

What:

- polygonization of segmentation masks (outer boundaries + holes)
- per-polygon area/solidity/convexity metrics

Where:

- derived from `segments.parquet` masks as a separate run (append-only)
- stored in `vectors.parquet` and vector artifact files

Captures / ignores:

- captures region geometry and simplifies downstream computation
- polygonization introduces approximation error; must record tolerance parameters

### C.N.3 Skeleton graphs (shape graphs)

What:

- medial-axis skeletons for selected masks (bird silhouette, branches)
- graph representations (nodes/edges, branch counts)

Where:

- `runs/<run_id>/outputs/vectors/<plate_id>__<run_id>__vector__skeleton.json`
- `vectors.parquet` rows with `vector_kind = skeleton`

Captures / ignores:

- captures a compact “shape grammar” useful for comparison and clustering
- brittle on noisy masks; requires mask quality gating

---

## C.F Text in images

### C.F.1 OCR at multiple levels

What:

- text region boxes + transcripts (Latin binomials, captions, plate numbers)
- confidence scores
- language/script (if available)

Where:

- run outputs:
  - `runs/<run_id>/outputs/ocr/<plate_id>__<run_id>__ocr__boxes.json`
  - `runs/<run_id>/outputs/ocr/<plate_id>__<run_id>__ocr__transcript.json`
- ledger: `ocr.parquet` (recommended)

Core `ocr.parquet` fields (recommended):

- `run_id`, `plate_id`, `variant_id` (nullable)
- `box_id`
- bbox fields
- `text`
- `confidence`
- `engine` (tesseract/trocr/etc.)
- `language` (nullable)

Captures / ignores:

- captures explicit text content that is otherwise treated as “non-nature pixels”
- may misread decorative engraving textures as text; needs region constraints

### C.F.2 Document understanding (only if scans become complex)

What:

- page layout structure (headers, footers, captions)
- reading order

Where:

- optional; only relevant if multi-page scans or compound plates enter the corpus

---

## C.G Captioning, tags, and pseudo-labels (weak labels; prompt registry required)

### C.G.1 Caption generation

What:

- one or more captions per plate (and optionally per segment)
- decoding parameters and prompt IDs (mandatory)
- uncertainty proxies (self-consistency, logprobs if available)

Where:

- run outputs under `outputs/captions/`
- ledger: `captions.parquet`
- prompt registry: `prompts/prompt_registry.yaml` (see addendum)

Core `captions.parquet` fields (recommended):

- `run_id`, `plate_id`, `variant_id` (nullable), `segment_id` (nullable)
- `model_id`, `model_sha`
- `prompt_id`, `prompt_version` or `prompt_hash`
- decoding params (temperature, top_p, max_tokens, etc.)
- `caption_text`
- uncertainty fields (optional)

Captures / ignores:

- captures model priors and culturally saturated readings
- must never be treated as factual description of the historical object

### C.G.2 Tag expansion

What:

- tag sets derived from captions or prompt-based CLIP probes
- tag frequency distributions

Where:

- `captions.parquet` (tags as arrays) or `tags.parquet` (if large)

Captures / ignores:

- captures browseable vocabulary axes
- extremely sensitive to prompt phrasing; registry discipline is non-negotiable

### C.G.3 Attribute models

What:

- explicit attribute logits (e.g., “pastoral/oppressive/desolate” mood probes)
- AVD axes (arousal/valence/dominance) if implemented as prompt probes

Where:

- `quality.parquet` or a dedicated `probes.parquet`

Captures / ignores:

- captures “strange axis” instrumentation as scalars/vectors
- biased by training corpora and prompt language; treat comparatively only

---

## C.H Aesthetics and perceptual quality

### C.H.1 Aesthetic scoring

What:

- aesthetic predictor scalar scores (sorting; pipeline fingerprinting)

Where:

- `quality.parquet` (recommended)
- also eligible as a “probe” output table (`probes.parquet`)

Captures / ignores:

- captures weak salience / composition priors
- does not measure “value” or “canon”; never used as authority

### C.H.2 Technical quality scoring

What:

- blur, exposure, contrast collapse, saturation extremes
- watermark/logo detection (if relevant)

Where:

- `quality.parquet`

Captures / ignores:

- captures digitization artifacts that affect comparability
- can confound intentional engraving texture with “noise”

---

## C.I Image-forensics / provenance / manipulation cues

These are framed as “maximum surface area” extraction signals. In Audubon, they often become pipeline divergence detectors rather than fraud detectors.

### C.I.1 Splice / tamper signals (classical)

What:

- ELA maps and summary statistics
- noise residual consistency
- CFA-like signals (often irrelevant for scans, but can still fingerprint pipelines)

Where:

- `forensics.parquet` (recommended)
- optional artifact images under `outputs/forensics/` (maps)

Captures / ignores:

- captures recompression and processing inconsistencies
- extremely easy to over-interpret; treat as weak signals only

### C.I.2 AI-generated detection signals (weak; error-prone)

What:

- scalar detector scores (if ever used)

Where:

- `forensics.parquet`

Captures / ignores:

- captures “model thinks it looks synthetic” which can correlate with heavy JPEG or restoration
- not reliable; include only if motivated by a mixed corpus

---

## C.J Geo/time inference without metadata (soft, probabilistic)

This category exists in the assay as a conceptual bucket. For Audubon plates, it is usually irrelevant, but it becomes relevant if the project expands to broader photo corpora.

### C.J.1 Geo-style embeddings (optional)

What:

- place-style embeddings (scene priors)

Where:

- `probes.parquet` or `quality.parquet`

### C.J.2 Weather/lighting (optional)

What:

- lighting condition classifiers or derived illumination metrics

Where:

- `quality.parquet`

---

## C.K Dataset-level relational structure (indices, clusters, outliers)

These are derived from the feature tables and exist to make the corpus navigable and to quantify stability across instruments.

### C.K.1 Multi-index ANN retrieval

What:

- FAISS/ScaNN indices for:
  - global embeddings (per model)
  - segment embeddings (per model)
  - optional classical descriptors/hashes
- kNN graphs

Where:

- `indices/` folder:
  - `indices/<index_id>/…`
  - `indices/<index_id>/index.manifest.json`
- optional `indices.parquet` ledger listing index IDs and configs

Captures / ignores:

- captures navigability and retrieval reproducibility
- index parameters are part of provenance; store them as configs with hashes

### C.K.2 Clustering at multiple resolutions

What:

- cluster labels for each embedding space (HDBSCAN/k-means/spectral)
- exemplar selections per cluster
- cross-model agreement measures (neighbor overlap)

Where:

- `clusters.parquet` (recommended derived table) with:
  - `model_id`, `run_id`, `clusterer_id`, `cluster_label`
- figures under `viz/` for projections and exemplars

Captures / ignores:

- captures manifold topology and stability
- clustering is not truth; store as derived views only

### C.K.3 Outlier mining

What:

- distance-to-neighbors summaries
- anomaly scores (per model and fused)

Where:

- `outliers.parquet` (derived)

### C.K.4 Active “curriculum” views

What:

- ordered lists of plates/segments by:
  - instability
  - disagreement across models
  - “stress” composite measures

Where:

- `curricula/` derived artifacts or `curricula.parquet`

---

## C.L Generative-model-oriented features (optional; only if gen workflows are in scope)

These are explicitly optional in preprocessing; include only if you intend to do diffusion-oriented evaluation later.

### C.L.1 Diffusion VAE latents

What:

- VAE latents for each plate (at a standardized resolution)

Where:

- `runs/<run_id>/outputs/embeddings/…` or dedicated `latents/`
- `embeddings.parquet` with `artifact_type = vae_latent` (if unified)

### C.L.2 UNet intermediate features / inversion artifacts / control signals

What:

- inversion reconstructions
- edge maps, depth maps, segmentation-conditioned control images

Where:

- run outputs under `outputs/…`; ledger pointers only

Captures / ignores:

- captures generative “feature space” structure
- high risk of scope creep; keep explicitly downstream of documentation runs

---

## C.M “Any tricks” category (things people forget, but matter for variance)

### C.M.1 Tile-wise everything

What:

- compute the core scalars (color, entropy, edge density) on a tile grid
- optionally embeddings on tiles

Where:

- `tiles.parquet` (grid + per-tile stats)

### C.M.2 Multi-scale pyramids

What:

- compute features at multiple downsample scales
- quantify scale sensitivity (variance changes with resolution)

Where:

- run configs + derived tables; must include `scale_level` field

### C.M.3 Ensemble embeddings

What:

- fused embeddings (late fusion) with stored weights
- cross-model agreement/disagreement vectors

Where:

- `embeddings.parquet` (new `model_id = ensemble/<name>` with config hash)

### C.M.4 Pseudo-chronology / “event” grouping

What:

- derived ordering/grouping by similarity to “stress axes” (purely analytic)

Where:

- derived tables only (`curricula.parquet`)

### C.M.5 Storage strategy (otherwise you drown)

What:

- explicit decision record for what is stored inline vs by reference

Where:

- dataset-level `STORAGE_POLICY.md` (recommended) and/or run config templates

---

## C.3 Minimal “preprocessing complete” feature set (what must exist to stop)

To declare preprocessing complete for the Audubon bootstrap corpus (435 plates), the minimum defensible feature set is:

1. Plate identity + provenance: `manifest.json`, `source.sha256`, schema-valid (per plate)
2. Baseline scalar extraction: `derived/input_image.json` (or equivalent ledger columns)
3. At least one segmentation run OR an explicit decision to defer segmentation (documented)
4. At least one embedding run for global plate embeddings (CLIP + one orthogonal model preferred)
5. Rebuildable ledgers: `plates.parquet`, `runs.parquet`, `segments.parquet` (if segmented), `embeddings.parquet`
6. QC pack: preview grids + outlier lists + basic projections rendered from ledgers

Everything else is optional or downstream, but must remain compatible with the same run/ledger discipline.
