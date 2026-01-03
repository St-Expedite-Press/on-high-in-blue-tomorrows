# The Big One (Deep Prompt + Figure Menu)

Below is a **maximally exhaustive deep-research prompt** designed to drive a state-of-the-art investigation **only from the materials assembled in this project** (Audubon plates from GitHub, your preprocessing notebooks, manifests, and derived metadata), augmented with **current best practice (Jan 2026)** framing. This is written to be dropped directly into a research-grade LLM or multi-agent system.

---

## Deep Research Prompt

**Title:** _The Burning World: Quantitative, Semantic, and Aesthetic Re-Readings of Audubon’s Plates under Climate Collapse_

### Role & Scope

You are a multidisciplinary research system operating across **digital humanities, computer vision, art history, ecology, and machine learning**. Your task is to analyze, extend, and critically reframe the Audubon _Birds of America_ plates as a **provable, reproducible dataset** and as an **artistic-theoretical intervention** titled _The Burning World_.

You must ground all claims in:

- The **435 high-resolution Audubon plates** compiled from GitHub (Nathan Buchar collection)
    
- The associated **plate-level metadata** (plate number, title, slug, source URLs)
    
- The **derived dataset structure**: manifests, checksums, scalar image statistics, and preprocessing decisions created in the provided notebooks
    
- No external datasets unless explicitly marked as _comparative context_
    

### Core Research Questions

1. **Material & Provenance**
    
    - What measurable visual regularities (color ranges, luminance, scale, entropy, edge density) define Audubon’s plates as a _system_ rather than individual artworks?
        
    - How does the preprocessing pipeline preserve provenance, auditability, and reproducibility at plate, run, and ledger levels?
        
2. **Semantic Extraction**
    
    - What semantic signals can be derived from vision embeddings (species posture, aggression, scarcity, abundance, environmental staging) without violating historical fidelity?
        
    - How do embeddings cluster when taxonomy is ignored in favor of **pose, violence, ecological pressure, or compositional stress**?
        
3. **Climate Counterfactual (“The Burning World”)**
    
    - How can controlled color transformation, night artifacts, atmospheric distortion, and saturation collapse be parameterized to express climate catastrophe _without_ hallucinating new anatomy?
        
    - Which visual dimensions (temperature shift, ash occlusion, contrast decay) most strongly alter perceived species vitality?
        
4. **Segmentation & Ontology**
    
    - How does separating bird / flora / ground / sky / inscription expose Audubon’s ideological framing of nature?
        
    - What new ontologies emerge when parts (wings, talons, beaks, branches) are recombined across plates?
        
5. **Machine Learning Strategy**
    
    - Which steps require **neural networks** (segmentation, embedding, generative variation) versus classical CV?
        
    - What LoRA-style fine-tuning strategies are viable using _only_ Audubon-derived material (e.g., style-only LoRAs, pose-conditioned LoRAs, chromatic-grammar LoRAs)?
        
6. **Benchmarking & Evaluation**
    
    - What benchmarks are appropriate for historical image corpora (intra-artist consistency, cross-plate entropy, embedding stability)?
        
    - How can ablation studies (with/without background, with/without color) be used as scholarly evidence?
        

### Required Deliverables

Produce the following, explicitly tied back to the dataset artifacts:

1. **Dataset Specification**
    
    - Formal description of directory structure, schemas, ledgers, and checksum strategy
        
    - Justification for Parquet usage for tabular/embedding data vs. file-based image storage
        
2. **Exploratory Figures (Maximal)**
    
    - Global color distributions (full set)
        
    - Luminance vs. entropy scatter plots
        
    - Plate chronology vs. compositional density
        
    - Embedding projections (UMAP / PCA) with and without taxonomy labels
        
3. **Methodological Analysis**
    
    - CPU vs. GPU decision boundaries
        
    - Trade-offs between full-pixel passes and scalar summaries
        
    - Failure modes (decompression limits, bias from paper background)
        
4. **Applications**
    
    - **Academic:** digital art history, extinction studies, climate humanities
        
    - **Artistic:** generative plate series, counterfactual natural histories
        
    - **Commercial:** archival ML tooling, museum-grade restoration pipelines
        
    - **Frontier:** foundation models trained on single-artist corpora, climate-conditioned visual grammars
        
5. **Critical Framing**
    
    - Position _The Burning World_ as both a dataset and a critique of Enlightenment naturalism
        
    - Address ethical issues of historical manipulation vs. interpretive transformation
        

### Citations & Evidence Rules

- Cite the Audubon GitHub corpus and metadata explicitly
    
- Clearly separate **measured results** from **interpretive claims**
    
- Flag speculative or generative outcomes as _counterfactual constructs_
    

### Output Style

- Scholarly, precise, non-promotional
    
- Use tables, figures, and reproducible references where possible
    
- Assume an expert audience; do not explain basic ML or CV concepts
    

---

If you want, next I can:

- Convert this into a **paper outline** (journal-ready),
    
- Generate a **grant proposal version**, or
    
- Translate it into a **multi-agent research workflow** (planner → analyst → critic → artist).
### Where you’re at right now (what’s _done_, what’s _real_, what’s _not yet_)

**Ground truth artifacts you have in hand:**

1. **A complete, structured corpus of 435 plates** (and you already sanity-checked that: 435 plate directories, zero missing manifests, zero missing sources, zero runs).
    
    - The plate universe is explicitly constrained to **1–435** in the schema.
        
2. **A filesystem “contract” for plate identity + provenance**
    
    - Every plate has a `manifest.json` governed by a strict schema with required fields: `plate_id`, `plate_number`, `title`, `slug`, `source_image`.
        
    - `plate_id` is constrained to `plate-###` format and schema disallows extra fields (`additionalProperties: false`).  
        This is huge: it means you’ve already pinned a _reproducible naming law_ and prevented “metadata drift.”
        
3. **A canonical mapping source for plate metadata**
    
    - Your `data.json` contains plate-level identifiers: `plate`, `name`, `slug`, `fileName`, `download` URLs (Audubon site URLs).  
        This is enough to reconstruct provenance and re-download/verify sources if needed.
        
4. **A run system defined (but not yet populated)**
    
    - You have a strict run manifest schema: a run must declare `run_id`, `plate_id`, `timestamp`, `models`, `outputs` (and forbids extra fields).  
        In other words: the “ledgered experiment” layer is already designed—even if you have **0 runs** right now.
        
5. **You attempted baseline image metadata extraction, hit real-world scale issues, and course-corrected**
    
    - The big bottleneck wasn’t “math,” it was **loading + iterating massive pixel arrays** (PIL decompression warnings + `np.histogram`/`bincount` on very large images). That’s normal for 100M+ pixel plates.
        
    - You also learned something critical: **full-distribution histograms for _every_ plate are not a bootstrap step**. They’re a later step, after you’ve got a faster strategy (tiling, downsampled proxies, or deferred heavy runs).
        
6. **Repo exploratory is clean**
    
    - Top level looks exactly like a dataset repo should: `plates_structured`, `schemas`, `ledger`, plus `README.md` and `data.json`.
        
    - No “runs” exist yet (good: you’re still in bootstrap).
        

**So the honest status sentence is:**

> You have a fully structured, schema-governed, provenance-preserving corpus (435 plates) with a defined run/ledger protocol, and you’ve validated naming + structural invariants; what you _do not yet have_ are populated ledgers, segmentations, embeddings, or any “Burning World” transformations.

---

## High-level workflow from here → end of preprocessing (assuming these notebooks are the bootstrap)

You said you want **4 runs total**, and you want an **A100** the whole time (with hardware detection). Here’s the clean “to the end of preprocessing” shape:

### Run 0 — Bootstrap & Baseline (CPU-first, GPU optional but not required)

**Goal:** lock in _lightweight, universal_ features and a deterministic audit trail.

- **0A. Contract re-validation** (what you already have): assert 435, schema present, manifests valid.
    
- **0B. Baseline per-plate metadata** _(scalar, cheap)_
    
    - Dimensions, file sizes, pixel count, aspect ratio
        
    - “Paper/background ratio” proxies (threshold-based masks)
        
    - Sharpness proxies (Laplacian variance), edge density
        
    - Luminance mean/std/entropy **as scalars** (not full distributions)
        
- **0C. Write ledgers**
    
    - `plates.parquet`: one row per plate (plate_id + canonical metadata + scalar features)
        
    - Optional: `preprocess_report.json` and a small “QC gallery” of thumbnails
        
- **0D. Hard-case registry**
    
    - Anything that triggers decompression warnings / extremely large dimensions gets flagged into a `plates_large.csv` (or parquet), so future runs can special-case them.
        

**Stop condition:** every plate has a baseline row in `plates.parquet`, and the run is fully reproducible.

---

### Run 1 — Segmentation (GPU-required)

**Goal:** produce _structured regions_ without hallucinating anatomy.

Outputs per plate:

- bird mask(s)
    
- flora mask(s)
    
- background/paper mask
    
- optional: “inscription”/plate text region
    

Stored as:

- compressed binary masks (PNG/WebP) in `plates_structured/plate-###/cache/` or `runs/run-.../`
    
- `segments.parquet`: region stats + file pointers (not the pixels themselves)
    

Key: you’ll be able to ask questions like:

- “How much of each plate is bird vs flora vs negative space?”
    
- “Does composition density change across plate numbers?”
    

---

### Run 2 — Embeddings & Semantic Indices (GPU-required)

**Goal:** create semantic vectors usable for clustering, retrieval, and “interpretive measurement.”

Multiple embeddings are worth it because they disagree in useful ways:

- **global embedding** (entire plate)
    
- **bird-only embedding** (mask-cropped)
    
- **flora-only embedding**
    
- **composition embedding** (edge map / saliency proxy)
    

Stored as:

- `embeddings.parquet`: vectors (or vector references), model IDs, preprocessing tags, plate_id
    

This unlocks:

- similarity search (“find plates with similar stance/violence/air/emptiness”)
    
- latent clustering without taxonomy labels
    
- change detection after Burning World transforms
    

---

### Run 3 — “The Burning World” Transform Family (GPU + CPU mix)

**Goal:** generate _parameterized_, reproducible, non-anatomy-altering climate-counterfactual variants.

You’ll be able to manipulate:

- illumination regime (nocturne / sodium / wildfire glow)
    
- atmospheric occlusion (haze, ash, particulate)
    
- chroma collapse / selective saturation failure
    
- contrast shaping localized by segmentation (e.g., background decays faster than bird)
    
- print-surface artifacts “as climate damage” (cracking, abrasion, bleed—but controlled)
    

Stored as:

- transformed images in `runs/run-.../outputs/` (or per-plate `runs/`)
    
- `runs.parquet`: parameters + pointers + summary metrics
    
- optional “before/after” paired thumbnails for QC
    

**Stop condition:** you can regenerate any variant given only:

- plate_id
    
- source checksum / source pointer
    
- parameter dictionary
    
- model version string
    

---

## What “scalar” means _in your current pipeline_

In this context, **scalar** = “a single number per plate (or per channel), not an array.”

Examples you already gravitated toward:

- `luminance_mean`, `luminance_std`, `luminance_entropy`
    
- `background_ratio`, `edge_density`, `laplacian_variance`
    
- `mean_rgb` (technically 3 scalars)
    

Why it matters:

- Scalars are cheap to compute and tiny to store.
    
- They let you do _global_ scholarship quickly (scatterplots, correlations, outliers) before you pay the cost of distributions.
    

---

## Parquet: is it “just really compressed”? Can it store pictures?

**Parquet is a columnar table format** designed for analytics: it stores columns efficiently (often compressed and encoded), so you can read _only the columns you need_ without scanning everything. It’s not “just compression,” it’s an analytics-optimized storage layout.

**Can it store images?** Yes, as binary blobs—**but it’s usually a bad idea** for large image corpora.  
Best practice for what you’re doing:

- Keep images as image files (JPG/PNG/TIFF) in a filesystem / object storage
    
- Store **paths + checksums + derived metrics + embeddings** in Parquet
    

That gives you:

- fast querying
    
- cheap recompute
    
- zero dataset bloat
    

---

## Cheaper storage than Google Drive (and what AWS “knowledge graph” is)

**Cheaper storage:** almost always **object storage** (e.g., S3) plus colder tiers for archives. The pattern is:

- hot working set: S3 Standard (or equivalent)
    
- warm archive: S3 Intelligent-Tiering
    
- cold archive: Glacier tiers
    

**Amazon version of a knowledge graph:** **Amazon Neptune** (managed graph database for property graphs / RDF-style graph workloads).

For your project, that translates to:

- Parquet = analytics tables (features/embeddings/segments/runs)
    
- Graph DB (optional) = relationships/ontology (bird ↔ flora ↔ pose ↔ plate ↔ motif ↔ transform)
    

---

# Deliverable (1): Maximal exploratory figures you can justify _by current standards_ (without wasting compute)

Below is the “definitive” figure menu—doable once your ledgers exist:

### A. Corpus health & scale

- file size histogram (per plate)
    
- megapixels distribution
    
- “giant plate” outlier table (top 20 by pixel count)
    

### B. Composition & materiality (baseline scalars)

- edge_density vs laplacian_variance (texture vs sharpness)
    
- background_ratio vs luminance_mean (paper dominance vs exposure)
    
- luminance_entropy vs plate_number (system drift or scan drift)
    

### C. Segmentation-derived

- bird_area_ratio vs plate_number
    
- flora_area_ratio vs bird_area_ratio
    
- “negative space” ratio vs embedding cluster ID
    

### D. Embedding geometry

- PCA / UMAP global plate embeddings
    
- PCA / UMAP bird-only embeddings
    
- distance-to-nearest-neighbor distribution (detect duplicates / near-duplicates)
    
- embedding stability across crops (whole vs bird-only vs flora-only)
    

### E. Burning World transforms (evaluation figures)

- parameter sweep grids (small subset)
    
- perceptual metric deltas: (contrast/entropy/saturation proxies) before vs after
    
- “semantic drift” plots: cosine distance(original_embedding, transformed_embedding)
    

---

# Deliverable (2): Exhaustive applications (academic + artistic + commercial + frontier)

### Academic / scholarly

- **Digital art history**: quantifying compositional grammar across a single-author corpus; segmentation exposes ideological framing (what counts as “nature” in the plate).
    
- **Critical provenance studies**: checksum + schema + run manifests support “computationally citable” transformations.
    
- **Eco-criticism + climate humanities**: controlled counterfactuals as method (not as “AI fantasy”)—you can measure how visual rhetoric changes under “collapse parameters.”
    
- **Media archaeology**: studying scan artifacts, paper whitening, and reproduction drift as part of the object’s contemporary life.
    

### Artistic / studio practice

- _The Burning World_ as a **parameterized editioning machine**: same plate → multiple climate regimes, each reproducible.
    
- Mask-based recomposition: bird extracted as a movable emblem; flora as “host environment”; paper as “world.”
    
- “No new anatomy” constraint produces a strong conceptual frame: you’re altering **climate optics**, not inventing species.
    

### Commercial / institutional

- Museum/archival tooling: QC + segmentation + retrieval for managing plate collections.
    
- Licensing/production: automating print-ready variants with provenance guarantees.
    
- Restoration-adjacent pipelines (without claiming “restoration”): artifact detection, stain mapping, paper tone equalization.
    

### Frontier / cutting edge

- Single-corpus foundation-style studies: what can be learned from “one artist’s world model”?
    
- Evaluation research: embedding drift under controlled transforms as a general method for studying interpretive interventions.
    
- Ontology engineering: building a “motif graph” (poses, branch types, sky types, violence cues) that is _derived_ rather than annotated by hand.
    

---

# A maximally exhaustive deep-research prompt (optimized and tightened)

You already wrote something strong. Below is the “drop-in” version I’d use for a multi-agent or research-grade LLM—**but now it explicitly binds to your schema/run system and forbids untracked claims**.

---

## Deep Research Prompt (v2)

**Title:** _The Burning World: A Reproducible Visual Corpus of Audubon Plates for Quantitative, Semantic, and Counterfactual Climate Reading_

### 0) Hard Constraints (non-negotiable)

- Treat the project’s **435 plates** as the complete universe (`plate_number` 1–435).
    
- Treat `plates_structured/plate-###/manifest.json` as the canonical identity record. Required fields are: `plate_id`, `plate_number`, `title`, `slug`, `source_image`.
    
- Treat `data.json` as a canonical provenance mapping of `plate`, `slug`, `fileName`, and `download` URL.
    
- Treat each processing event as a **run** that must be documented by a `run.manifest` containing at least `run_id`, `plate_id`, `timestamp`, `models`, `outputs`.
    
- No claims are allowed unless they are grounded in:
    
    - measured outputs from ledgers / run outputs, OR
        
    - explicitly marked interpretive/speculative sections.
        

### 1) Roles (multi-agent recommended)

Create agents with distinct goals:

- **Archivist**: provenance, schema compliance, checksum strategy, audit trail.
    
- **Vision Engineer**: segmentation + embeddings + evaluation metrics.
    
- **Art Historian**: compositional grammar, ideological staging, historical framing.
    
- **Climate Humanist**: counterfactual ethics + interpretive method.
    
- **Methods Editor**: reproducibility, ablations, benchmark design.
    

### 2) Core Research Questions (must be answered with evidence tags)

**Material & System Regularities**

- Identify corpus-level regularities using baseline scalar metrics (exposure, entropy, sharpness, background ratio).
    
- Produce outlier analysis: giant plates, low-entropy plates, unusually high edge-density plates.
    

**Semantic Extraction Without Taxonomy**

- Cluster plates by pose, aggression, ecological pressure, compositional stress using embeddings + segmentation-derived region stats.
    
- Explicitly compare whole-plate vs bird-only embeddings.
    

**The Burning World Transform Family (Counterfactual, non-anatomy-altering)**

- Define a parameter space for climate optics (haze/ash, nocturne regimes, chroma collapse, contrast decay).
    
- Require that transformations operate _without_ inventing new anatomical structure (use segmentation masks as constraints).
    

**Segmentation & Ontology**

- Use segmentation masks to quantify “what counts as nature” in each plate: bird vs flora vs paper vs sky.
    
- Build an ontology derived from measured features (not manual labels), and propose a graph representation.
    

**Benchmarking**

- Define benchmarks appropriate for a single-author historical corpus:
    
    - embedding stability across crops and transforms
        
    - outlier reproducibility tests
        
    - ablations: with/without background removal; with/without flora; with/without color
        

### 3) Required Deliverables (strict)

1. **Dataset specification**: directory structure, schemas, run manifests, ledgers; justify tabular vs file-based storage.
    
2. **Exploratory figure pack**: include the maximal set that is computationally justified (see figure menu).
    
3. **Methodology**: CPU/GPU boundaries; failure modes (extreme pixel counts, decompression constraints); mitigation strategies.
    
4. **Applications**: academic, artistic, commercial, frontier—each tied to measurable dataset affordances.
    
5. **Ethics & framing**: distinguish historical artifact from counterfactual construct; argue interpretive legitimacy.
    

### 4) Evidence tagging format (mandatory)

Every paragraph must end with one of:

- **[MEASURED]** (references a ledger field or computed metric)
    
- **[DERIVED]** (computed from measured things; show formula)
    
- **[INTERPRETIVE]**
    
- **[SPECULATIVE / FUTURE WORK]**
    

---

If you want, next I can turn this into:

- a **4-run execution plan** with exact outputs per run (filenames + ledger schemas + parameter dictionaries), or
    
- a **“max figure pack” notebook skeleton** that generates every plot once `plates.parquet / segments.parquet / embeddings.parquet / runs.parquet` exist.
