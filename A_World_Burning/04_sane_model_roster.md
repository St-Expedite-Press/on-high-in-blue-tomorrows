# Sane Model Roster (Final)

Here is the **final, sane model roster**, organized by role, matching the pipeline you've now locked in. This is the list that actually makes sense given your data structure, ledgers, and separation between CPU groundwork and GPU runs.

---

### 1. **Embedding / Representation (core, GPU)**

These feed directly into `embeddings.parquet`.

**Vision-only**

- `openai/clip-vit-large-patch14`
    
- `laion/CLIP-ViT-H-14-laion2B-s32B-b79K`
    
- `google/siglip-so400m-patch14-384`
    

**Vision + language alignment**

- `openai/clip-vit-base-patch32` (cheap baseline)
    
- `apple/aimv2-large-patch14` (strong global structure)
    

Use case:

- plate similarity
    
- clustering
    
- retrieval
    
- conditioning generative models later
    

---

### 2. **Self-supervised visual features (non-semantic)**

These are _extremely_ useful for non-textual structure.

- `facebook/dino-v2-base`
    
- `facebook/dino-v2-large`
    
- `facebook/dinov2-giant` (only if batching carefully)
    

Use case:

- material similarity
    
- engraving / pigment structure
    
- pre-semantic clustering
    
- anomaly detection
    

These pair very well with your histogram + entropy metadata.

---

### 3. **Segmentation / Region discovery (GPU)**

These will populate `segments.parquet`.

**Foundation**

- `facebook/sam-vit-h`
    
- `facebook/sam-vit-l`
    
- `facebook/sam-vit-b`
    

**Semantic / hierarchical**

- `facebook/mask2former-swin-large-ade`
    
- `IDEA-Research/detrex-mask2former`
    

Use case:

- foreground isolation
    
- bird vs foliage vs paper
    
- region-level embeddings
    
- palette extraction per segment
    

---

### 4. **Vision-capable LLMs (analysis + synthesis)**

These do _not_ replace embeddings; they sit on top.

- `llava-hf/llava-1.6-34b-hf`
    
- `llava-hf/llava-1.6-13b-hf`
    
- `Qwen/Qwen2-VL-7B-Instruct`
    
- `Qwen/Qwen2-VL-14B-Instruct`
    

Use case:

- structured visual descriptions
    
- region annotation
    
- taxonomy suggestions
    
- cross-checking metadata
    

These will generate **run artifacts**, not overwrite baseline data.

---

### 5. **Diffusion / generative (future, optional)**

Only after segmentation + embeddings are stable.

- `stabilityai/stable-diffusion-xl-base-1.0`
    
- `stabilityai/sdxl-turbo`
    
- `runwayml/stable-diffusion-v1-5`
    

With:

- ControlNet (edges / segmentation)
    
- Palette conditioning from histograms
    
- CLIP/DINO guidance vectors
    

---

### 6. **What you explicitly are _not_ using**

Because your structure makes them unnecessary or harmful:

- YOLO-style detectors (too opinionated)
    
- OCR models (plates are illustrative)
    
- End-to-end captioning as ground truth
    
- Proprietary black-box APIs for embeddings
    
- Any GPU for histogram / metadata work
    

---

### 7. **Why this list is final**

This set cleanly maps to:

- `input_image.json` → CPU
    
- `input_color_histograms.json` → CPU
    
- `runs/run-*/metrics.json` → GPU outputs
    
- `ledger/*.parquet` → aggregation layer
    

No redundancy. No conceptual leakage. No premature semantics.

If you want, next we can:

- lock **run naming conventions per model**
    
- define **embedding dimensionality contracts**
    
- design **ledger schemas per model family**
    

But as a _model list_, this is complete and correct.
