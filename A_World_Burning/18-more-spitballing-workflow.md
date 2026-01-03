# Workflow (More Spitballing)

You're **past "data acquisition" and into "dataset engineering."** Here's where we are, what we've gathered, and what the full preprocessing workflow looks like from here.

---

## Where we are right now (ground truth from the two bootstrap notebooks)

### 1) We have a canonical source dataset and provenance anchors

- **435 full-resolution Audubon plates** (the repo is explicitly “all 435” and organized into plate ranges).
    
- The original repo’s **range-binning** layout is the truth for disk paths (e.g., `plates/1-99`, `plates/100-199`, …, `plates/400-435`).
    
- `data.json` is your authoritative **metadata index**: it includes `plate` (number), `name` (title string), `slug`, `fileName` (the canonical filename), and `download` URL.
    

### 2) We built a _plate-centric_ working dataset layout (your “lab notebook filesystem”)

You now have:

- `plates_structured/plate-001 ... plate-435/`
    
    - `manifest.json` per plate (plate id/number/title/slug/source_image/etc.)
        
    - `source/` containing the canonical source image for that plate (copied in, not moved)
        
    - `runs/` empty for now (good: no derived runs yet)
        
    - `viz/` reserved
        
    - `cache/` reserved
        

This is the key move: **every plate is now an atomic unit** for reproducibility and per-plate derivations.

### 3) We formalized the dataset contract and validation mechanics

- JSON Schemas exist for:
    
    - plate manifests
        
    - run manifests
        
- Validators exist and you’ve been actively asserting:
    
    - directory invariants
        
    - manifest ↔ filesystem consistency
        
    - run naming law (even though runs are empty currently)
        

### 4) We learned a hard constraint about “full pixel pass”

Your attempt to compute “full” histograms across the entire plates set hit two real-world issues:

- **Some plates are huge** (PIL warns about decompression-bomb thresholds), and full-array histogramming becomes **slow / memory heavy**.
    
- The right move is exactly what you concluded:  
    **Full-pixel pass once → store only scalar summaries** (tiny, cheap, provenance-safe).  
    Anything beyond that should be done via tiling / downsample / sampling strategies, or only on selected plates.
    

### 5) Repo exploratory already confirms we’re clean

Your exploratory report indicates:

- 435 plates present
    
- manifests and sources present
    
- runs currently 0
    
- schemas present
    
- image header stats were starting (you stopped before heavy distributional work)
    

---

## What we’ve gathered (current “assets” you can rely on)

### A) Metadata assets

- **Global metadata index** (`data.json`) with stable filename mapping.
    
- **Per-plate manifest** (your normalized, reproducible plate record).
    

### B) Provenance assets

- **Stable plate IDs** (`plate-###`) and deterministic naming.
    
- **Per-plate source immutability** (source image lives in `source/`).
    
- **Checksum infrastructure** exists (you already wrote/validated `source.sha256` earlier in the bootstrap thread).
    

### C) Structural assets

- Schema + validators + contract assertion cell.
    
- Ledger directory exists (even if Parquet scaffolds still need to be created/verified in some runs).
    

---

## High-level workflow from here → end of preprocessing

Below is the **whole preprocessing arc**, assuming the two notebooks are the bootstrap “ground truth,” and everything else is derived and reproducible.

### Phase 0 — Contract + Environment (you already did)

- Drive mount + dataset root resolution
    
- structure assertion
    
- schema presence checks
    
- (optional) environment/hardware detection for logging only
    

### Phase 1 — Baseline “scalar” image diagnostics (CPU-only)

Goal: create _cheap, universal, provenance-useful_ metrics that never need a GPU.  
Per plate, store only:

- file size, dimensions, megapixels, pixel_count
    
- mean/std/min/max RGB
    
- luminance mean/std + entropy (scalar)
    
- background_ratio / white_ratio / black_ratio (scalar heuristics)
    
- sharpness proxy (e.g., Laplacian variance), edge density proxy
    

**Outputs**

- `plates_structured/plate-###/input_image.json` (ONLY)
    

This is the right stopping point before distributions/embeddings/segmentation.

### Phase 2 — Scaled / tiled distributional summaries (CPU-only or GPU-optional, but not required)

Goal: get “color / tone / texture distributions” without ever loading the full plate into a single giant compute step.  
Methods:

- **Downsampled full-frame** histograms (e.g., resize long-edge to 2k or 4k)
    
- **Tiled histograms** (e.g., 512×512 tiles; aggregate stats)
    
- **Random pixel sampling** (e.g., 1–5 million pixels max)
    

**Outputs**

- `input_color_summary.json` (quantitative summaries only, not giant arrays)
    
- optionally `viz/histogram_*.png` (visual-only, cheap)
    

### Phase 3 — Canonical derived images (CPU, sometimes GPU not needed)

Goal: generate deterministic “working representations”:

- preview thumbnails
    
- standardized working PNG/JPEG (optional)
    
- optional “paper/background mask” using heuristics (still CPU)
    
- optional geometric normalization (crop margins, rotate if needed)
    

**Outputs**

- `viz/input_preview.png`
    
- `cache/work_2k.png` (if you choose)
    

### Phase 4 — Segmentation (GPU recommended)

Goal: extract _regions_ that will become the backbone of:

- recoloration pipelines
    
- semantic indexing
    
- object-level manipulation (“catastrophic climate change” overlays by region)
    

Outputs (per plate, per segmentation model/run):

- `runs/run-.../segments/`
    
    - masks (RLE JSON, PNG masks, or COCO-style polygon)
        
    - segment stats (area, bbox, mean color, etc.)
        
- ledger: `segments.parquet` (global)
    

### Phase 5 — Embeddings (GPU recommended)

Goal: compute multimodal embeddings at multiple granularities:

- global plate embedding
    
- embeddings per segment / per tile
    
- optional text embeddings for titles, slugs, captions, prompts
    

Outputs:

- `runs/run-.../embeddings/…`
    
- ledger: `embeddings.parquet`
    

### Phase 6 — Vision-language annotations (GPU recommended)

Goal: generate “semantic field”:

- captions, tags, species guesses, scene descriptions
    
- stylistic descriptors (palette words, mood descriptors)
    
- material / print artifact descriptors (foxing, stains, cracks)
    

Outputs:

- `runs/run-.../vlm/annotations.json`
    
- ledger: `plates.parquet` and/or `runs.parquet` grows
    

### Phase 7 — QC, benchmarking, reproducibility pack (CPU + GPU where relevant)

Goal: make the dataset _publishable and paper-grade_:

- drift tests (same image → same stats)
    
- checksum verification
    
- run-to-run comparability dashboards
    
- model cards + dataset card
    
- “known failure cases” list
    
- exhaustive figure set (below)
    

---

## Deliverable 1: “Maximally useful” exploratory figures + diagnostics library

Think of this as: **the definitive dataset atlas**. You want both:

- _global_ (across all 435 plates)
    
- _per-plate_ (stored inside each plate dir or in runs)
    

### Global overview figures (dataset-level)

**File + geometry**

- Distribution of megapixels, width, height, aspect ratios
    
- Outlier plates (top 10 by pixel count)
    
- File size distribution (detect compression anomalies)
    

**Color / tone (lightweight summaries, not full arrays)**

- Mean RGB scatter (R vs G vs B)
    
- Luminance mean vs luminance std scatter
    
- Background_ratio distribution
    
- “white paper dominance” vs “ink/pigment density” plot (background_ratio vs edge_density)
    

**Texture / detail**

- Laplacian variance distribution (sharpness proxy)
    
- Edge density distribution
    
- Correlations: sharpness vs file size vs megapixels
    

**Similarity / duplicates**

- perceptual hash distance matrix (global)
    
- near-duplicate clusters (if any)
    
- embedding-based neighborhood graph (later)
    

**Segmentation / object structure** (after Phase 4)

- segment count distribution per plate
    
- segment area distribution (global)
    
- “largest segment ratio” (how dominant the bird is vs background)
    
- mask quality metrics (stability, fragmentation)
    

**Embedding space** (after Phase 5)

- 2D projections (UMAP/t-SNE) for:
    
    - full plate embeddings
        
    - segment embeddings
        
- clustering (HDBSCAN / k-means) + representative exemplars
    
- cross-model agreement plots (embedding model A vs B neighbor overlap)
    

**VLM outputs** (after Phase 6)

- tag frequency
    
- caption length distribution
    
- “uncertainty” proxies (self-consistency, logprob if available)
    
- semantic drift across models
    

### Per-plate diagnostic outputs (stored locally)

- `viz/input_preview.png`
    
- `viz/qc_sheet.png` (a single “contact sheet” style panel per plate: thumbnail + key scalars + later segments overlay)
    
- `runs/.../overlay_segments.png`
    
- `runs/.../palette_swatches.png` (dominant colors from sampled pixels)
    
- `runs/.../artifact_map.png` (optional: cracks/foxing detection)
    

### Ledger tables (Parquet) you ultimately want

- `plates.parquet`: one row per plate (joinable master table)
    
- `runs.parquet`: one row per run per plate (run metadata + pointers)
    
- `segments.parquet`: one row per segment (plate_id, run_id, segment_id, area, bbox, stats, mask pointer)
    
- `embeddings.parquet`: one row per embedding vector record (plate/tile/segment, model name, vector pointer or packed vector)
    

---

## Deliverable 2: Exhaustive application space (academic + artistic + commercial + frontier)

You’re building a **reproducible multimodal feature factory** for a historically significant corpus, with a second life as a _generative / critical apparatus_ for “The Burning World.”

### Academic / scholarly applications

**Digital humanities / art history**

- stylistic drift across plates (palette + line density + composition features)
    
- material artifact quantification (foxing, paper aging, staining)
    
- comparative print/provenance studies (if you add source scans from other repositories later)
    
- “visual rhetoric” analysis: how depiction conventions vary by species class (raptors vs songbirds vs waterfowl)
    

**Environmental humanities / climate narrative**

- algorithmic “counterfactual ecology”: re-map habitats/seasons via color/texture transforms
    
- generating evidence-backed “visual climate argument” series: pair each manipulated plate with quantitative deltas (palette shift, saturation drop, haze increase, night artifact injection)
    

**Computer vision / ML research**

- segmentation benchmarking on real, high-res illustration data (not photos)
    
- domain adaptation (photo → illustration; illustration → print)
    
- multimodal retrieval benchmarks (text query → plate; “mood” query → plate)
    
- robust embedding comparisons across foundation models
    

**Museum / archival workflows**

- automated catalog enrichment (captions, tags, crosslinks)
    
- conservation triage (artifact severity scoring)
    
- search + discovery for public access portals
    

### Artistic applications (your “Burning World” core)

Because you’re extracting regions + semantics + palette physics, you’ll be able to do **controlled interventions** instead of “style transfer soup”:

**Region-controlled recoloration**

- sky/background “smoke haze” while preserving bird plumage
    
- selectively desaturate flora, intensify heat-shifted reds/oranges, or push cyan shadows
    
- night-artifact injection: halos, sensor-noise grain, underexposed blacks, sodium-vapor casts—_but only in chosen regions_
    

**Narrative series construction**

- build “chapters” by clustering plates in embedding space and then applying consistent transforms per cluster
    
- “same bird, different world” variations (multiple runs per plate with parameterized transforms)
    

**Print + exhibition deliverables**

- provenance-backed limited editions: every print can ship with a QR linking to:
    
    - the plate’s manifest
        
    - the transformation run manifest
        
    - before/after + quantitative deltas
        

### Commercial / product applications

- subscription or licensed dataset: “Audubon Plates — annotated & segmented”
    
- API: “query by mood / palette / species / composition”
    
- stock/creative tooling: palette extraction packs, texture packs, vectorized elements
    
- conservation-tech partnerships (artifact scoring / restoration planning prototypes)
    

### Frontier / 2026-adjacent applications

**Graph + retrieval systems**

- build a **knowledge graph** where nodes are:
    
    - plate → segments → attributes → embeddings → generated annotations
        
    - link to historical taxonomy, geography, and climate datasets
        
- then do GraphRAG / multimodal RAG:
    
    - “show me plates with swamp / dusk / red-dominant palettes / high edge density”
        
    - “find nearest semantic neighbors to plate 151 (Turkey Buzzard) and describe shared visual motifs”
        

**Training / LoRA / adapters**

- train LoRAs on:
    
    - “Audubon engraving texture”
        
    - “plate border / paper artifact”
        
    - “catastrophic haze overlays” as a controllable concept
        
- train segmentation refiners on illustration domain
    
- train “mood embedding” heads on top of vision embeddings using weak labels from VLM tags
    

**Synthetic data generation**

- generate controlled variants (haze, burn, flood, drought palettes) with run manifests → a clean synthetic benchmark set
    

---

## What you’re actually trying to do (in plain terms)

You’re building a **museum-grade, paper-grade, reproducible, plate-centric multimodal dataset** that supports two simultaneous goals:

1. **A definitive quantitative/qualitative research dataset** (provenance tracked, validated, benchmarkable).
    
2. **An artistic transformation engine** for _The Burning World_ where every aesthetic choice can be parameterized, reproduced, compared, and narrated.
    

That combination (rigorous provenance + controllable aesthetic mutation) is _exactly_ what makes this more than “a folder of images.”

---

## One critical note (security)

Your repo search results include an `.env` file containing credentials/secrets. Treat those as compromised: rotate/revoke them immediately and remove the file from anywhere it could be synced or shared. (I’m not going to repeat any of it here.)

---

If you want, the next thing I’d write is a **single “Preprocessing Master Plan” doc** (one-page) that lists:

- the 4 runs you committed to,
    
- which models each run uses,
    
- exactly what each run emits (files + ledger rows),
    
- and the full figure checklist tied to each phase.

For the current “no-missed-ideas” versions of those artifacts, see:

- `A_World_Burning/00_preprocessing_assay.md`
- `A_World_Burning/28-sources-and-variant-acquisition.md`
- `A_World_Burning/27-strange-models-compendium.md`
