# Preprocessing & Extraction Assay (Exhaustive)

[[A_World_Burning/README]] | [[A_World_Burning/30-whitepaper-toc]] | [[A_World_Burning/33-appendix-b-filesystem-naming-run-ids]]

This document is an **exhaustive inventory** of every datum/artifact described across the markdown corpus that we may need to **acquire (“go get”)**, **extract**, or **derive** in order to build the dataset through **preprocessing**.

It is intentionally **redundant**: if an idea appears anywhere in the markdown, it is represented here.

---

## Scope (what “through preprocessing” means here)

Included (dataset creation + preprocessing):

- Acquisition + integrity (download/verify/freeze)
- Canonicalization into plate-centric structure
- Baseline per-plate facts (header + scalar pixel pass)
- Optional distribution summaries (sampled/tiled histograms, etc.)
- Derived working images (previews, standardized working resolution)
- Segmentation / region proposal + region stats
- Embeddings (whole-plate, segment, tile; multi-model ensembles)
- Text extraction (OCR + layout, if desired)
- Captioning/tags/weak labels (versioned prompts, if desired)
- Vectorization (edges/regions → SVG/polygons, if desired)
- Forensics + quality + “hygiene” signals (as extraction outputs)
- Dataset-level indices (ANN) and the tables needed to make the corpus queryable
- QC/benchmark artifacts required to freeze the preprocessing output as citable

Excluded (not preprocessing; mentioned elsewhere, but not the focus):

- Climate counterfactual transformations / rendering the “Burning World” images
- Interpretive synthesis (narrative claims, paper writing, cluster “meaning”)
- Institutional graph/Neptune deployment (we can emit ingest tables, but not required to complete preprocessing)

---

## Current baseline (what the two moved notebooks cover)

From `A_World_Burning/notebooks/audubon_bird_plates_setup.ipynb` and `A_World_Burning/notebooks/audubon_bird_plates_handoff.ipynb`:

- [x] Define `DATASET_ROOT` and canonical paths in Colab/Drive
- [x] Build `plates_structured/plate-###/` scaffold
- [x] Write per-plate `manifest.json`
- [x] Write and/or verify per-plate `source.sha256`
- [x] Persist JSON schemas under `schemas/` (plate + run)
- [x] Create empty ledger scaffolding under `ledger/` (`plates.parquet`, `runs.parquet`, `embeddings.parquet`, `segments.parquet`)
- [x] Read-only “handoff” entrypoint + structure assertion + exploratory report

Not yet covered by those two notebooks (but required for preprocessing completion):

- [ ] Baseline per-plate extraction beyond identity: `input_image.json` (scalar pixel pass)
- [ ] Any distributional summaries (histograms, sampling, tiling)
- [ ] Any segmentation runs / segment ledgers
- [ ] Any embedding runs / embedding ledgers
- [ ] Any OCR/captioning/VLM runs
- [ ] Any indices (FAISS/ScaNN) for retrieval

---

## Non‑negotiable system laws (dataset creation constraints)

### Plate-centric + dual-ledger discipline

- The **plate is the atomic unit**.
- **Runs are sealed events** (append-only; never edited/merged).
- Plate-local data is authoritative; ledgers are **derived** and disposable.
- Nothing overwrites source images; everything is restartable.

### Validators (must exist conceptually even if implemented later)

- Plate validator:
  - schema-valid `manifest.json`
  - `source_image` exists
- Run validator:
  - run references a valid plate
  - declared outputs exist
  - run folder is sealed / immutable
- Validators run:
  - at notebook start
  - before ledger aggregation
  - before any destructive cleanup

### Run provenance requirements (minimum)

Every run must record:

- `run_id`, `plate_id`, timestamp
- model(s) used and versions
- configuration (and ideally a config hash)
- inputs (paths + checksums)
- outputs (paths + checksums)
- status: incomplete/complete + failure mode if aborted

Minimum run folder contents (one proposed strict form):

- [ ] `runs/<run_id>/run.manifest.json`
- [ ] `runs/<run_id>/config.json` (the hashed config)
- [ ] `runs/<run_id>/outputs/…` (embeddings/segments/metrics/visuals)
- [ ] `runs/<run_id>/run.sha256` (optional but explicitly proposed)

Derived artifact naming law (explicitly proposed as a strict option):

- [ ] `<plate_id>__<run_id>__<artifact_type>__<descriptor>.<ext>`

### Run ID semantics (must be decided once)

The markdown explicitly calls out this decision point:

- [ ] Sequential run IDs (e.g., `run-0001`, `run-0002`)
- [ ] Hash-based run IDs (content/config hash)
- [ ] Hybrid (timestamp + short hash)

Whichever you choose, enforce it everywhere and treat runs as sealed.

---

## Execution scaffolding required to make extraction survivable (Colab/Drive reality)

These are not “features”, but they **are** repeatedly described as required infrastructure for doing the extraction without losing provenance or wasting compute.

Colab constraints (accept and design around them):

- [ ] No inbound services (batch/notebook driven only)
- [ ] Ephemeral compute (kernels die; GPUs disappear)
- [ ] Drive (or equivalent) is the source of truth; write outputs early and often

Manifest-first workflow (never skip):

- [ ] Build a manifest of all source files before processing (IDs + paths + hashes + geometry)
- [ ] Use that manifest as the sole driver for batching, resuming, and completeness checks

Resume-safe batching pattern:

- [ ] Process in batches; after each batch:
  - [ ] write outputs to disk
  - [ ] append/update Parquet ledgers
  - [ ] record progress / “batch done” state

Hardware detection + adaptive defaults (explicitly provided in markdown):

- [ ] Detect GPU availability + name + VRAM and classify (CPU/T4/L4/A100-ish)
- [ ] Use a capability table to set per-model defaults (image_size, dtype, batch_size)
- [ ] Clamp batch sizes automatically on weaker GPUs

Batched run executor (explicitly provided in markdown):

- [ ] A single executor that:
  - [ ] runs a model across many plates in batches
  - [ ] writes per-plate outputs under `plate/runs/run-*/...`
  - [ ] is resumable/idempotent (skip plates already done)

Notebook “law” (repeated across multiple files):

- [ ] Every notebook begins with:
  - [ ] environment + hardware detection
  - [ ] structure/naming assertion
  - [ ] immutable config block (hashable)
- [ ] Every notebook ends with:
  - [ ] validation + registration of all written files
  - [ ] ledger sync checks
  - [ ] explicit STOP
- [ ] CPU notebooks must never request GPU; GPU notebooks must fail fast if GPU missing
- [ ] No hidden state across notebooks; all paths derive from `DATASET_ROOT`

Drive performance caveat (called out explicitly):

- [ ] Avoid extremely many small writes on Drive for large corpora
- [ ] For this corpus (435 plates), per-plate JSON is likely acceptable; still prefer Parquet for anything that grows (segments/tiles/embeddings)

Stop condition for “keep extracting more” (explicitly stated):

- [ ] Stop adding new extractors when cluster topology stabilizes:
  - [ ] clusters stabilize across different embedding models (CLIP/DINO/etc.)
  - [ ] outliers remain outliers regardless of extractor
  - [ ] additional captions add redundancy, not new axes

Storage doctrine (explicitly stated):

- [ ] **Files hold artifacts**
- [ ] **Parquet holds facts**
- [ ] **Vectors hold perception**
- [ ] **Graphs hold meaning**

---

## Things to go get (inputs to acquire/freeze)

### Required for the Audubon corpus as described

- [ ] **All 435 plates** (full resolution) from the source repository (range-binned layout: `plates/1-99`, `plates/100-199`, …, `plates/400-435`)
- [ ] `data.json` (authoritative metadata index):
  - `plate` number
  - `name` (title)
  - `slug`
  - `fileName` (canonical filename)
  - `download` URL
- [ ] Repository `README.md` / licensing/credit statements (for dataset card + provenance record)

### Optional / future inputs explicitly mentioned

- [ ] Additional plate corpora (e.g., “Ottoman plates” are mentioned as comparative material) handled as a second dataset root with the same contract
- [ ] Comparative datasets (only if explicitly allowed later): other 19th‑century natural history plates, modern wildlife photos, climate-disaster photo sets (these are *not* required for preprocessing of Audubon-only, but are mentioned as benchmark context)

### One critical non-feature note that still affects dataset engineering

- [ ] If a `.env` file with secrets exists anywhere in the working tree, treat it as compromised: rotate/revoke and remove from any synced/shared location (called out explicitly in the markdown corpus).

---

## Canonical dataset structure (what must exist on disk)

### Plate directory scaffold (minimum viable, current notebooks implement this)

For every `plate-###`:

- [ ] `manifest.json` (identity only; never stores ML outputs)
- [ ] `source/` (exactly one canonical source image)
- [ ] `source.sha256`
- [ ] `runs/` (append-only run folders)
- [ ] `viz/` (human-only previews/diagnostics)
- [ ] `cache/` (deterministic working derivatives; never overwrites source)

### Schemas + ledgers

- [ ] `schemas/plate.manifest.schema.json`
- [ ] `schemas/run.manifest.schema.json`
- [ ] `ledger/plates.parquet` (derived)
- [ ] `ledger/runs.parquet` (derived)
- [ ] `ledger/embeddings.parquet` (derived)
- [ ] `ledger/segments.parquet` (derived)

### Optional “planned evolution” structure (mentioned as a stricter future layout)

- [ ] Split into:
  - `datasets/audubon/raw/…` (immutable source)
  - `datasets/audubon/structured/plate-###/…` (plate-centric truth + derived)
  - `ledgers/…` (global parquet)
  - `graph/…` (optional)

This is a **design choice to reconcile** with the current notebooks’ `DATASET_ROOT/plates_structured` approach; both appear in the markdown.

---

## Extraction inventory (the complete feature surface area)

This section is the full checklist of “things to extract/derive” from `abstract_photo_workflows/01_general_photo_set_prompt.md` **plus** Audubon-specific additions from the `A_World_Burning/` files.

Treat this as a **menu with tiering**, not a requirement to do everything on day one.

### A. File- and container-level features (even when “no metadata”)

#### 1. Byte-level / format signatures

- [ ] MIME/type, magic bytes, codec, container (JPEG/PNG/WebP/HEIC/TIFF), progressive vs baseline JPEG
- [ ] Dimensions, aspect ratio, bit depth, color type (RGB/RGBA/gray), chroma subsampling (4:4:4, 4:2:0), ICC profile presence
- [ ] Compression ratio proxy: `file_size / (W*H)`, JPEG quant tables, Huffman tables, PNG filter usage statistics
- [ ] Thumbnail presence (some formats), XMP remnants, IPTC remnants (often stripped but sometimes partial)

#### 2. Integrity / duplication / lineage

- [ ] Perceptual hashes: pHash/dHash/aHash/wHash (multiple) + multi-resolution hashes
- [ ] Exact hashes: SHA256, xxhash
- [ ] Near-duplicate graph: approximate nearest neighbors over hashes + embeddings
- [ ] Crop/resize lineage detection: match via keypoints (SIFT/ORB) + RANSAC homographies

#### 3. Pipeline fingerprints (forensics-lite)

- [ ] JPEG quantization table clustering (camera/app families)
- [ ] Recompression count estimation
- [ ] Resampling detection (periodicity)
- [ ] Color management anomalies (missing/odd ICC)

### B. Global pixel statistics (cheap, surprisingly powerful)

#### 4. Color / tone / contrast

- [ ] RGB/HSV/Lab histograms (coarse + fine), joint histograms (RG, GB)
- [ ] Mean/var/skew/kurtosis per channel, per colorspace
- [ ] Dynamic range, clipping rates (percent near 0/255), gamma estimate
- [ ] White balance estimate, illuminant estimation
- [ ] Contrast measures (RMS contrast, Michelson on tiles), entropy

#### 5. Texture / sharpness / noise

- [ ] Laplacian variance (sharpness), Tenengrad, edge density
- [ ] Noise level estimation (per-channel, spatially varying), ISO-like noise signature proxy
- [ ] Blur type classification (motion vs defocus) via frequency-domain features
- [ ] JPEG blocking score, ringing score

#### 6. Frequency-domain

- [ ] FFT radial power spectrum, 1/f slope, high-frequency energy ratio
- [ ] Wavelet energy across scales/orientations
- [ ] Periodicity detection (moire, screen/print patterns)

#### 7. Composition geometry (still global)

- [ ] Saliency map statistics (center bias, saliency entropy)
- [ ] Horizon likelihood (dominant line orientation)
- [ ] Vanishing point estimate, perspective strength
- [ ] Symmetry scores (vertical/horizontal), rule-of-thirds energy distribution

### C. Classical CV local features (pre-deep, still useful)

#### 8. Keypoints and descriptors

- [ ] SIFT/ORB/AKAZE keypoints count, descriptor aggregates
- [ ] Bag-of-visual-words (BoVW) histograms (train vocab on subset)
- [ ] Geometric consistency features (repeat patterns, architectural cues)

#### 9. Contours and shape summaries

- [ ] Canny edge maps -> edge density, contour length distributions
- [ ] HOG descriptors (global + tile)
- [ ] LBP texture histograms (multi-scale)
- [ ] Gabor filter bank responses

### D. Foundation-model embeddings (the “universal backbone”)

#### 10. CLIP-family embeddings (image)

- [ ] Global embedding (e.g., ViT-L/14 class)
- [ ] Multi-crop embeddings (center + corners + random)
- [ ] Patchwise CLIP embeddings (feature map from intermediate layers)
- [ ] Text-conditioned similarity against large tag lexicon (open-vocab tagging)

#### 11. Self-supervised vision transformers

- [ ] DINO/DINOv2: global + patch tokens
- [ ] iBOT/MAE-style embeddings (reconstruction-aware)

#### 12. ConvNet embeddings (still good at textures)

- [ ] EfficientNet/ConvNeXt pooled features
- [ ] Places365-style scene embeddings (if you want scene taxonomy)

#### 13. Multimodal caption embeddings

- [ ] Generate captions (see below), then embed captions (text embeddings) for language indexing + cross-modal retrieval

### E. Dense semantics (objects, masks, parts, relationships)

#### 14. Object detection (open-vocab if possible)

- [ ] Boxes + class labels + confidence
- [ ] Count features: number of persons, vehicles, animals, etc.
- [ ] Co-occurrence graphs and spatial stats (object adjacency, relative positions)

#### 15. Instance/semantic segmentation

- [ ] Per-pixel class maps (semantic segmentation)
- [ ] Instance masks; shape features per mask: area, perimeter, convexity, eccentricity

#### 16. “Segment Anything” style masks (class-agnostic)

- [ ] Many masks per image at multiple scales
- [ ] For each mask: compute embedding of the crop (CLIP/DINO), color stats, texture stats
- [ ] Store as an “object-ish database” from unlabeled images

#### 17. Keypoints / pose / layout

- [ ] Human pose keypoints (for non-identifying pose analytics)
- [ ] Hand keypoints, face landmarks (not for identity; for alignment/blur/pose clusters)
- [ ] Depth estimation (monocular depth map)
- [ ] Surface normals estimate
- [ ] Optical flow (video); for photos, you can still estimate motion blur direction

#### 18. Scene graphs (derived)

- [ ] Scene graph: nodes = detected objects/masks; edges = relations (left-of, above, inside, near, overlaps)
- [ ] Graph embeddings for retrieval (e.g., “person near car under tree”)

### F. Text in images

#### 19. OCR at multiple levels

- [ ] Text presence probability
- [ ] OCR text + bounding boxes + confidence
- [ ] Script/language detection
- [ ] Font-ish features (stroke width, typeface class), sign vs document classification

#### 20. Document understanding (if many scans)

- [ ] Layout detection (title/body/table)
- [ ] Table extraction into structured rows/cols
- [ ] Form fields detection

### G. Captioning, tags, and pseudo-labels

#### 21. Caption generation

- [ ] Short caption, long caption, dense caption (multiple regions)
- [ ] Store: caption text, per-sentence confidence/entropy proxies, and LM logprob if available

#### 22. Tag expansion

- [ ] Captions -> extract nouns/entities -> canonicalize -> map to taxonomy
- [ ] Add synonyms/hypernyms via lexical resources (optional)

#### 23. Attribute models

- [ ] Aesthetic attributes: “moody”, “high key”, “film grain”, “bokeh”, “street”, etc. (classifier or prompt-based scoring)
- [ ] Style attributes: “illustration”, “render”, “photo”, “anime”, “diagram”, “scan”, etc.
- [ ] NSFW filtering (for pipeline hygiene)

### H. Aesthetics and perceptual quality

#### 24. Aesthetic scoring

- [ ] NIMA-like aesthetic score
- [ ] “Interestingness”, memorability
- [ ] Composition scores (rule-of-thirds adherence, subject centeredness)

#### 25. Technical quality scoring

- [ ] Blur score, noise score, exposure score, color cast score
- [ ] “Usable for print?” heuristics
- [ ] Watermark/logo detection

### I. Image-forensics / provenance / manipulation cues

#### 26. Splice / tamper signals

- [ ] Error Level Analysis (ELA) (weak but sometimes helpful)
- [ ] CFA artifact analysis (if raw-like)
- [ ] Inconsistency maps (noise residual anomalies)

#### 27. AI-generated detection signals

- [ ] Model-based detectors (weak signal only)
- [ ] Frequency artifacts / upscaling signatures
- [ ] Diffusion “fingerprints” (weak; useful for stratification)

### J. Geo/time inference without metadata (soft, probabilistic)

#### 28. Geo-style embeddings

- [ ] Scene/place recognition embeddings (urban vs rural, architecture style, vegetation climate)
- [ ] Language from signs (OCR) -> country hints
- [ ] Sun position + shadow orientation -> approximate time-of-day; combined with vegetation maybe season (very approximate)

#### 29. Weather/lighting

- [ ] Cloud cover estimation, haze, rain/snow likelihood
- [ ] Indoor/outdoor classifier
- [ ] Night/day/dusk classifier

### K. Dataset-level relational structure

#### 30. Multi-index ANN retrieval

- [ ] Separate ANN indices: CLIP global, DINO global, FFT spectrum, color hist
- [ ] Composite retrieval: weighted fusion for search-by-image or “find similar but different”

#### 31. Clustering at multiple resolutions

- [ ] HDBSCAN / k-means / spectral on embeddings
- [ ] Hierarchical clustering for coarse→fine topics
- [ ] Cluster summaries via captioning: pick exemplars, caption, auto-name cluster

#### 32. Outlier mining

- [ ] Isolation forest / LOF on embeddings
- [ ] Rare-object mining from detector counts
- [ ] Near-duplicate clusters for spam/reposts

#### 33. Active “curriculum” views

- [ ] Sort by quality, novelty, uncertainty (caption entropy), cluster density
- [ ] Sampling policy for labeling or human review

### L. Generative-model-oriented features (optional, only if gen workflows are in scope)

#### 34. Diffusion VAE latents

- [ ] Encode each image into diffusion VAE latent space
- [ ] Store latents (possibly quantized) or statistics/low-rank projections

#### 35. Diffusion UNet intermediate features (expensive)

- [ ] Store intermediate activation summaries from inversion/encoding pipeline
- [ ] Or do fixed denoise-trajectory features (few steps, fixed schedule)

#### 36. Inversion artifacts

- [ ] DDIM inversion latent, reconstruction error
- [ ] “Promptability score”: how well captions reconstruct via text-to-image similarity

#### 37. Control signals

- [ ] Edge maps (Canny, HED), depth, normals, segmentation maps, pose maps
- [ ] Store as training-ready ControlNet targets

#### 38. Prompt mining

- [ ] Caption -> prompt rewrite variants (short/style/object-focused)
- [ ] Negative prompt suggestions from detected artifacts (blur/noise/watermark)

#### 39. Patch libraries

- [ ] Build patch datasets via SAM masks or sliding windows (textures/materials)
- [ ] Tag patches via CLIP; cluster (“rust”, “stucco”, “foliage”, “neon sign”, etc.)

### M. “Any tricks” category (things people forget)

#### 40. Tile-wise everything

- [ ] Compute features per image AND per tile pyramid (e.g., 256px tiles)
- [ ] Store tile embeddings + tile quality scores
- [ ] Enables “find images with this thing somewhere in it”

#### 41. Multi-scale pyramids

- [ ] Process at multiple resolutions: 256, 512, 1024 (or native)
- [ ] Some artifacts only appear at certain scales (watermarks, texture, faces)

#### 42. Ensemble embeddings

- [ ] Store 3–5 embedding families; don’t bet on one
- [ ] Optional: learn small fusion later

#### 43. Pseudo-chronology / “event” grouping

- [ ] Near-duplicate + background similarity clusters to find bursts (same event)
- [ ] Build sets suitable for multi-view or temporal narratives

#### 44. Weak identity-like grouping without biometrics

- [ ] Prefer: clothing color/texture embeddings; pose + scene context; near-duplicate series grouping
- [ ] If using face features: use only for local alignment/blur/dedup; avoid cross-context identity systems

#### 45. Storage strategy (otherwise you drown)

- [ ] Per-image table: ids, paths, file stats, global embeddings (arrays), quality scores, hashes
- [ ] Per-object table: image_id, mask_id, bbox/mask RLE, object embedding, object tags
- [ ] Per-tile table: image_id, tile_id, coords, tile embedding, tile quality
- [ ] Indices: FAISS/ScaNN per embedding type
- [ ] Columnar storage: Parquet/Arrow; compress embeddings (float16 / PQ)

---

## Audubon-specific preprocessing artifacts & decisions (from `A_World_Burning/`)

### Baseline extraction (Phase 1 “scalar”, CPU-only)

Target per-plate derived record (canonical place: `plates_structured/plate-###/input_image.json`):

- [ ] Filesystem/provenance:
  - [ ] file size bytes
  - [ ] checksum exists (do not recompute unless verifying)
  - [ ] loadability flag
  - [ ] format + JPEG subsampling (and “EXIF present?” but not full EXIF parse)
- [ ] Geometry:
  - [ ] width, height
  - [ ] aspect ratio
  - [ ] megapixels
  - [ ] orientation (portrait/landscape/square)
  - [ ] pixel_count
- [ ] Scalar pixel facts (one pass):
  - [ ] mean/std/min/max RGB
  - [ ] luminance mean/std
  - [ ] grayscale-likeness
  - [ ] background_ratio (paper detection heuristic)
  - [ ] white_ratio (saturation near-white)
  - [ ] black_ratio (saturation near-black)
- [ ] Signal/complexity scalars:
  - [ ] luminance entropy (scalar; histogram not stored)
  - [ ] global contrast (Michelson + RMS)
  - [ ] sharpness proxy (Laplacian variance)
  - [ ] edge density proxy (Sobel magnitude mean)
- [ ] Planning flags:
  - [ ] very_large image flag (MP > threshold)
  - [ ] extreme aspect ratio flag (optional)

**Explicit “pause point” option** (also described): stop here (no histograms, no arrays, no GPU, no ledgers beyond updating `plates.parquet`).

Optional split of “header-only” vs “pixel-pass” facts (explicitly scheduled elsewhere):

- [ ] `image_header.json` (header/container facts only; no pixel math)
- [ ] `input_image.json` (pixel-pass scalar facts)

### Optional distributional summaries (Phase 2, CPU-only or GPU-optional)

If you decide you want distributions (without “full pixel pass everywhere”):

- [ ] Downsampled full-frame histograms (e.g., long edge 2k/4k)
- [ ] Tiled histograms (e.g., 512×512) aggregated to summary statistics
- [ ] Random pixel sampling (cap pixels to 1–5M)
- [ ] Foreground/background split histograms using a paper threshold

Possible per-plate outputs (choose one):

- [ ] `input_color_summary.json` (summary only; avoids giant arrays)
- [ ] `input_color_histograms.json` (256-bin arrays for RGB + luminance; optionally foreground split)

Optional per-plate visual-only diagnostics:

- [ ] `viz/input_preview.png`
- [ ] `viz/histogram_rgb.png`
- [ ] `viz/histogram_rgb_foreground.png`
- [ ] `viz/histogram_luminance.png`

### Canonical derived working images (Phase 3)

- [ ] `viz/input_preview.png` (thumbnail)
- [ ] `cache/work_2k.png` (standard working resolution, if chosen)
- [ ] Optional deterministic geometry normalization:
  - [ ] margin crop / plate border removal policy (must be declared)
  - [ ] rotation correction policy (must be declared)
  - [ ] tiling policy for outliers (must be declared)

### Segmentation (Phase 4, GPU recommended)

Outputs (per plate, per run):

- [ ] Masks in one or more forms:
  - [ ] PNG masks (for inspection)
  - [ ] RLE JSON (compact + ledger-friendly)
  - [ ] COCO-style polygons (vector-friendly)
- [ ] Segment-level stats (per mask):
  - [ ] bbox, area %, perimeter, convexity/solidity, eccentricity
  - [ ] mean color / palette summary within the mask
  - [ ] texture/edge density within the mask
  - [ ] embedding pointers for the mask crop (if computed)
- [ ] Run overlays/diagnostics:
  - [ ] `runs/.../overlay_segments.png`
- [ ] Global ledger:
  - [ ] `segments.parquet` rows per (plate_id, run_id, segment_id)

Model options explicitly named across the markdown:

- [ ] SAM (vit-h primary; vit-l/vit-b fallback)
- [ ] Mask2Former (for semantic classes like sky/ground/water, if needed)
- [ ] Optional benchmarking of multiple segmentation stacks before choosing

Additional explicit model/tool names that appear in the markdown corpus (optional pool):

- [ ] GroundingDINO (text-conditioned boxes)
- [ ] DETR (count signals, spatial relations)
- [ ] SAM-HQ (mentioned; optional)

### Embeddings (Phase 5, GPU recommended)

Granularities explicitly expected:

- [ ] Whole-plate embeddings
- [ ] Segment embeddings (mask crops)
- [ ] Tile embeddings (multi-resolution tiles)
- [ ] Text embeddings for:
  - [ ] titles/slugs
  - [ ] captions/tags/prompts (if generated)

Model families explicitly named across the markdown:

- [ ] CLIP variants (ViT-B/32 baseline; ViT-L/14 core; ViT-H optional)
- [ ] SigLIP (e.g., SO400M)
- [ ] DINOv2 (base/large; giant optional)
- [ ] iBOT/MAE-style embeddings (optional)
- [ ] ConvNeXt/EfficientNet embeddings (texture axis; optional)
- [ ] “Strange embeddings” (optional, called out explicitly):
  - [ ] affect / mood embeddings
  - [ ] Arousal–Valence–Dominance (AVD) projections
  - [ ] art-historical similarity embeddings (engraving/manifold distance)
  - [ ] narrative tension embeddings via VLM prompting + text embedding
- [ ] “absence” / negative-space sensitivity embeddings

Additional explicit embedding model names that appear in the markdown corpus (optional pool):

- [ ] EVA-CLIP (higher-fidelity aesthetic embeddings)
- [ ] AIMv2 (Apple; “global structure” axis)
- [ ] BiomedCLIP (anatomy bias; explicitly proposed as surprising/optional)
- [ ] ImageBind (multimodal alignment; explicitly proposed as “future-proof”)

Global ledger:

- [ ] `embeddings.parquet` rows per embedding record (plate/segment/tile × model × run)

### Vision-language annotations (Phase 6, optional but explicitly planned)

- [ ] Caption passes (short/long/dense; whole plate and/or segments)
- [ ] Tag sets (canonicalized)
- [ ] Style descriptors (illustration/scan/engraving/pastoral/ominous/etc.)
- [ ] Material/print artifact descriptors (foxing, stains, cracks)
- [ ] Optional “species guesses” (mentioned, but must not overwrite known metadata)

Outputs:

- [ ] `runs/run-.../vlm/annotations.json` (or similar run-scoped path)
- [ ] Ledger growth via `runs.parquet` and/or a dedicated captions/tags table (recommended)

VLM/caption model names explicitly listed in the markdown corpus (optional pool):

- [ ] BLIP / BLIP-2 (factual captioning)
- [ ] LLaVA (dense description / reasoning)
- [ ] Qwen2-VL (instruct VLM)
- [ ] Florence-2 (multi-task vision-language)

### Vectorization (explicitly called out as a second representation regime)

Edge-based vectorization:

- [ ] Canny/Sobel/Laplacian edges → tracing (Potrace-style)
- [ ] SVG paths + path-level statistics (length, curvature, topology)

Region/shape vectorization:

- [ ] Segmentation masks → polygonization (COCO polygons)
- [ ] Superpixels → vector regions (optional)

Skeletonization / medial axis (experimental):

- [ ] Skeleton graphs (spines/joints/axes)

Learned vectorization (explicitly discouraged as primary truth; optional as baseline):

- [ ] Neural SVG extraction models (compare only; don’t treat as authoritative)

### QC + benchmarking pack (Phase 7)

Determinism/drift:

- [ ] Re-run baseline extraction → identical outputs (or controlled floating tolerance)
- [ ] Checksum verification for sources and critical derived artifacts

Structural invariance metrics (especially useful as “safeguards” later):

- [ ] Edge map similarity (before/after or across pipeline stages)
- [ ] Keypoint preservation (ORB/SIFT-like)
- [ ] Shape consistency (IoU on coarse segmentation)

Pixel-statistical baselines:

- [ ] Mean/variance drift (RGB/luminance)
- [ ] Entropy change
- [ ] Frequency-domain energy redistribution (low vs high freq)

Segmentation quality:

- [ ] segment counts per plate
- [ ] fragmentation metrics, stability scores
- [ ] “largest segment ratio” (foreground dominance)

Embedding stability:

- [ ] cross-model neighbor overlap (CLIP vs DINO vs SigLIP)
- [ ] projection plots (PCA/UMAP/t-SNE) for plates and segments

Per-plate “contact sheet” diagnostics:

- [ ] `viz/qc_sheet.png` (thumbnail + scalars + overlays)
- [ ] palette swatches
- [ ] optional artifact maps

Known failure cases list:

- [ ] decompression-bomb-size plates
- [ ] plates with unusual borders / text density
- [ ] plates that break segmentation assumptions

Dataset atlas figures/diagnostics (explicit deliverable; derived artifacts):

- [ ] File + geometry:
  - [ ] distributions: megapixels, width, height, aspect ratios
  - [ ] outlier plates (top-N by pixel count)
  - [ ] file size distribution (compression anomaly detection)
- [ ] Color / tone (from baseline summaries):
  - [ ] mean RGB scatter (R vs G vs B)
  - [ ] luminance mean vs luminance std scatter
  - [ ] background_ratio distribution
  - [ ] “paper dominance vs pigment density” plot (background_ratio vs edge_density)
- [ ] Texture/detail:
  - [ ] Laplacian variance distribution
  - [ ] edge density distribution
  - [ ] correlations (sharpness vs file size vs megapixels)
- [ ] Similarity / duplicates:
  - [ ] perceptual-hash distance matrix
  - [ ] near-duplicate clusters (if any)
  - [ ] embedding neighborhood graph (once embeddings exist)
- [ ] Segmentation structure:
  - [ ] segment count distribution per plate
  - [ ] segment area distribution (global)
  - [ ] largest-segment ratio distribution
  - [ ] mask quality metrics (stability, fragmentation)
- [ ] Embedding space:
  - [ ] 2D projections (UMAP/t-SNE/PCA) for full-plate embeddings
  - [ ] 2D projections (UMAP/t-SNE/PCA) for segment embeddings
  - [ ] clustering (HDBSCAN/k-means) + exemplar plates/segments
  - [ ] cross-model agreement plots (neighbor overlap)
- [ ] VLM outputs:
  - [ ] tag frequency distributions
  - [ ] caption length distribution
  - [ ] uncertainty proxies (self-consistency, logprob if available)
  - [ ] semantic drift across models (if multiple are used)

---

## Storage + tables (what we ultimately need to “have” after preprocessing)

Minimum “joinable” Parquet set (explicitly expected):

- [ ] `plates.parquet` (1 row per plate; includes identity + baseline metrics)
- [ ] `runs.parquet` (1 row per run per plate; provenance + pointers)
- [ ] `segments.parquet` (1 row per segment/mask; geometry + pointers + stats)
- [ ] `embeddings.parquet` (1 row per embedding record; model + vector or pointer)

Commonly-needed additional tables (implied by the feature list; optional but coherent):

- [ ] `tiles.parquet` (tile coordinates + per-tile stats + embedding pointers)
- [ ] `ocr.parquet` (text boxes + transcripts + confidence + language/script)
- [ ] `captions.parquet` (caption text + prompt_id + model_id + confidence/logprob)
- [ ] `quality.parquet` (blur/noise/exposure/watermark + aesthetic scores)
- [ ] `forensics.parquet` (ELA/CFA/noise-residual anomaly scores, AI-gen weak scores)
- [ ] `vectors.parquet` (vector paths/polygons/skeleton graphs + stats + pointers)

Indices (to make it navigable without rescanning):

- [ ] FAISS/ScaNN index per embedding family (global, segment, tile)
- [ ] Optional composite retrieval layer (fusion weights stored as config)

---

## CPU/GPU boundaries (operational constraints)

CPU-only (never request GPU):

- [ ] Manifests + schema validation
- [ ] Checksums and file integrity
- [ ] Directory moves/copies/scaffolding
- [ ] Ledger initialization and Parquet I/O
- [ ] Exploratory audits / header-only inspection
- [ ] Baseline scalar extraction (if kept strictly scalar + single pass)

GPU-optional (CPU works; GPU helps at scale):

- [ ] CLIP embeddings
- [ ] DINO embeddings
- [ ] small captioning models
- [ ] OCR models (depending on choice)

GPU-necessary (don’t bother CPU-only at full resolution):

- [ ] SAM/SAM-HQ segmentation (full-res)
- [ ] High-res diffusion work (not preprocessing unless explicitly desired)
- [ ] Large VLMs (>1B params) for dense annotation

Colab GPU tier reality (explicitly mapped in markdown; used for planning):

- [ ] T4 (16GB): CLIP ViT-B/L, DINOv2-base, SAM ViT-B; SAM ViT-L with resizing/tiling
- [ ] L4 (24GB): CLIP ViT-H, SigLIP SO400M, DINOv2-large, SAM ViT-H, some Mask2Former; 7B–13B VLMs
- [ ] A100 (40GB): DINOv2-giant, 34B VLMs, SDXL high-res without gymnastics

---

## Open “reconciliation” points (places ideas conflict across files)

These are the cracks to decide explicitly so preprocessing doesn’t drift.

- [ ] **Do histograms exist at all?**
  - Option A: scalar-only `input_image.json` and no histograms (strict pause point)
  - Option B: keep `input_color_histograms.json` but sample/resize/tile to avoid full-pass pain
- [ ] **Per-plate JSON vs Parquet-only storage**
  - Colab/Drive guidance says “avoid many small writes”
  - Plate-centric Audubon guidance prefers per-plate truth files + derived ledgers
  - Decide: for 435 plates, per-plate JSON is fine; for larger corpora, prefer Parquet-first.
- [ ] **OCR: in or out?**
  - One doc calls OCR unnecessary (“plates are illustrative”)
  - Another lists OCR as Tier‑1 for extracting binomials and text masks
  - Decide based on whether inscription/text is a research axis or just noise to mask.
- [ ] **Directory law (“current” vs “planned evolution”)**
  - Current notebooks: `DATASET_ROOT/plates_structured`
  - Formal contract draft: `datasets/audubon/raw` + `datasets/audubon/structured` + `ledgers/`
  - Decide whether/when to migrate; avoid half-and-half.

---

## Stop conditions (when preprocessing is “done”)

Preprocessing can be considered complete when:

- [ ] All 435 plates have: `manifest.json`, source image, `source.sha256`
- [ ] All plates have baseline `input_image.json` (or its ledger equivalent)
- [ ] Segmentation outputs exist for the chosen stack (or you explicitly decide to defer segmentation)
- [ ] Embeddings exist for the chosen stack (global; plus segment/tile if desired)
- [ ] Ledgers exist and are rebuildable from plate-local truth and run artifacts
- [ ] QC pack exists (drift tests, outlier lists, known failure cases, basic projections)

At that point the corpus is **frozen but rich**: everything downstream is interpretation or transformation, not preprocessing.
