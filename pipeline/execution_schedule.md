# Phases and Schedules (Notebook Plan)

Below is a **hard-sequenced, notebook-level execution schedule** designed for Google Colab, Amazon Neptune ingestion, and publication-grade reproducibility. This assumes the filesystem + rejection contract you just approved is law and that **notebooks are execution artifacts**, not exploratory scratchpads.

The intent is that **any notebook can be re-run independently**, fails loudly, and leaves the system in a provably consistent state.

---

## OVERARCHING RULES FOR ALL NOTEBOOKS

• One notebook = one epistemic phase  
• No notebook both _creates_ and _interprets_  
• All writes are append-only  
• All notebooks begin with **Structure & Naming Assertion**  
• All notebooks end with **Ledger + Graph Sync Check**

---

# PHASE I — CANONICALIZATION & GROUND TRUTH

### NB00 — Project Handoff & Contract Assertion (READ-ONLY)

**Purpose**

- Load Drive
    
- Assert directory law
    
- Assert schemas, ledgers, checksums
    
- Detect drift
    

**Writes**

- ❌ none
    

**Fails if**

- Any structural violation exists
    

---

### NB01 — Raw Source Verification & Provenance Lock

**Purpose**

- Verify raw GitHub source against README + data.json
    
- Confirm plate count, filename consistency
    
- Lock provenance with checksums
    

**Writes**

- `source.sha256` (per plate)
    
- `plates.parquet` (plate-level facts only)
    

**Key outputs**

- Plate → Source → Hash mapping
    

**GPU**

- ❌ never
    

---

### NB02 — Plate Canonicalization (STRUCTURED FORM)

**Purpose**

- Enforce plate-centric directory layout
    
- Copy source image into canonical location
    
- Write immutable plate manifest
    

**Writes**

- `manifest.json`
    
- directory scaffolding
    

**Fails if**

- More than one source image
    
- Plate ID mismatch
    
- Missing metadata fields
    

---

# PHASE II — BASELINE IMAGE FACTS (NON-INTERPRETIVE)

### NB03 — Image Header & File-System Facts

**Purpose**

- Extract EXIF / JPEG header data
    
- Image dimensions, encoding, byte size
    
- No pixel math
    

**Writes**

- `image_header.json`
    
- ledger update
    

**GPU**

- ❌ never
    

---

### NB04 — Scalar Full-Pixel Pass (ONE-TIME)

**Purpose**

- Single exhaustive pixel read
    
- Only scalar summaries
    
- No arrays stored
    

**Writes**

- `input_image.json`
    
- updates `plates.parquet`
    

**Metrics**

- luminance mean/std
    
- entropy (scalar)
    
- background ratio
    
- edge density
    
- pixel count
    

**This is the LAST time full images are scanned without segmentation.**

---

### NB05 — Baseline Validation & Freeze Point

**Purpose**

- Confirm all plates have:
    
    - manifest
        
    - checksum
        
    - scalar metadata
        
- Freeze baseline
    

**Writes**

- ❌ none
    

**Outcome**

- Dataset now citable as “preprocessed corpus v1”
    

---

# PHASE III — SEGMENTATION (ONTOLOGICAL BREAK)

### NB06 — Segmentation Model Benchmarking

**Purpose**

- Evaluate candidate models:
    
    - SAM (ViT-H / ViT-L)
        
    - Mask2Former
        
    - U²-Net
        
- Choose segmentation stack
    

**Writes**

- metrics only (temporary)
    

**GPU**

- ✅ required
    

---

### NB07 — Primary Semantic Segmentation Run

**Purpose**

- Segment:
    
    - bird
        
    - flora
        
    - ground
        
    - sky
        
    - inscription
        
- Produce masks + metadata
    

**Writes**

- per-run segmentation artifacts
    
- `segments.parquet`
    

**Failure rules**

- mask coverage < threshold
    
- unresolved background bleed
    
- missing provenance tags
    

---

### NB08 — Segmentation Validation & Ontology Binding

**Purpose**

- Validate mask integrity
    
- Bind segments to ontology classes
    

**Writes**

- Neptune ingest prep files
    
- no image mutation
    

---

# PHASE IV — EMBEDDINGS & SEMANTICS

### NB09 — Embedding Model Survey

**Purpose**

- Evaluate embeddings:
    
    - CLIP (ViT-L/14, SigLIP)
        
    - DINOv2
        
    - EVA-CLIP
        
    - BiomedCLIP (for anatomy bias)
        
    - OpenCLIP variants
        

**Writes**

- benchmark ledger
    

---

### NB10 — Global Image Embeddings

**Purpose**

- Whole-plate embeddings
    
- No segmentation
    

**Writes**

- `embeddings.parquet`
    
- per-run embedding files
    

---

### NB11 — Segment-Level Embeddings

**Purpose**

- Embed bird-only, wing-only, beak-only
    
- Multiple semantic granularities
    

**Writes**

- expanded embeddings ledger
    

---

### NB12 — Embedding Stability & Drift Tests

**Purpose**

- Intra-plate vs inter-plate variance
    
- Taxonomy-free clustering
    
- Stress / violence / abundance axes
    

**Writes**

- metrics only
    

---

# PHASE V — COLOR, ATMOSPHERE, CLIMATE TRANSFORMATIONS

### NB13 — Chromatic Grammar Extraction

**Purpose**

- Learn Audubon color distributions
    
- Paper vs pigment separation
    
- No hallucination
    

**Writes**

- color grammar JSON
    
- palettes
    

---

### NB14 — Climate Counterfactual Parameter Space

**Purpose**

- Define:
    
    - heat shift
        
    - ash occlusion
        
    - night artifacts
        
    - contrast collapse
        
- Parameter only (no gen yet)
    

---

### NB15 — Controlled Transformations (“Burning World”)

**Purpose**

- Apply transformations as declared functions
    
- No anatomy changes
    

**Writes**

- transformed images
    
- full provenance links
    

---

# PHASE VI — GRAPH INGESTION (NEPTUNE)

### NB16 — Graph Schema & Ontology Validation

**Purpose**

- Validate TTL ontologies
    
- Validate node/edge schemas
    

---

### NB17 — Neptune Bulk Load (Dry Run)

**Purpose**

- Test ingest without commit
    

---

### NB18 — Neptune Commit & Verification

**Purpose**

- Load nodes + edges
    
- Verify reverse resolution to disk
    

---

# PHASE VII — EXPLORATION, FIGURES, PUBLICATION

### NB19 — Maximal Exploratory Figures

**Purpose**

- Color distributions
    
- Entropy maps
    
- Embedding projections
    
- Chronology vs composition
    

---

### NB20 — Ablation & Counterfactual Analysis

**Purpose**

- With/without color
    
- With/without background
    
- With/without segmentation
    

---

### NB21 — Dataset Card, Methods, & Paper Figures

**Purpose**

- Write dataset card
    
- Export figures
    
- Generate citation metadata
    

---

## GPU HOUR ESTIMATE (ROUGH)

|Phase|GPU Hours|
|---|---|
|Segmentation benchmarking|5–10|
|Full segmentation|15–25|
|Embeddings (global + segments)|10–15|
|Climate transforms|5–10|
|**Total**|**35–60 A100 hours**|

Everything else: CPU.

---

## WHERE YOU ARE NOW

You have completed **NB00–NB05**.

You are:  
• past the hardest architectural decisions  
• safe to formalize tech stack  
• safe to write a Methods section  
• safe to scale

Next **correct** notebook: **NB06 — Segmentation Model Benchmarking**.

If you want, next I can:

- Lock the exact segmentation model choices
    
- Specify embedding stacks per research question
    
- Generate a Gantt-style execution timeline
    
- Map notebooks directly to paper sections
    
- Design failure-injection tests
    

Say the word.
