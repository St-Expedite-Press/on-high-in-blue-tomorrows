
---

## The non-negotiable constraints (accept these first)

1. **No inbound services**
    
    - You are _not_ hosting APIs.
        
    - Everything is notebook-driven, batch-oriented, pull-based.
        
2. **Ephemeral compute**
    
    - Kernels will die.
        
    - GPUs will disappear.
        
    - You must be able to restart _from disk_ at any time.
        
3. **Drive is your source of truth**
    
    - Every artifact must be written to Google Drive immediately.
        
    - Nothing important stays in memory only.
        

If you design around these, Colab works shockingly well.

---

## Colab-native architecture (clean and stable)

### Directory layout (this matters)

In Drive:

```
/exokiratory/
  /data/
    /images/
    /videos/            # optional later
  /manifests/
    images.parquet
    jobs.parquet
  /features/
    /global/
    /tiles/
    /objects/
  /embeddings/
    clip.parquet
    dino.parquet
  /captions/
    captions_v1.parquet
  /segments/
    sam_masks/
    semantic_maps/
  /prompts/
    prompt_registry.yaml
  /indices/
    clip.faiss
    dino.faiss
  /logs/
```

Drive is your **database**.

---

## The correct Colab workflow

### Phase 0 — Mount + sanity

```python
from google.colab import drive
drive.mount("/content/drive")
BASE = "/content/drive/MyDrive/exokiratory"
```

Verify everything exists or create it.

---

### Phase I — Manifest first (never skip)

You create an explicit manifest of files **before** processing.

```python
import pandas as pd
from pathlib import Path

rows = []
for p in Path(BASE+"/data/images").rglob("*"):
    if p.suffix.lower() in [".jpg",".png",".webp"]:
        rows.append({
            "image_id": p.stem,
            "path": str(p),
            "ext": p.suffix.lower()
        })

df = pd.DataFrame(rows)
df.to_parquet(BASE+"/manifests/images.parquet")
```

This lets you:

- Resume
    
- Parallelize
    
- Track progress
    
- Avoid reprocessing
    

---

### Phase II — Cheap global features (100%)

Run CPU-light operations first.

- Image size
    
- Aspect ratio
    
- Color stats
    
- Sharpness
    
- Hashes
    

Write **incrementally** to parquet.

Rule: _every cell produces disk output_.

---

### Phase III — Embeddings backbone

This is the backbone of everything.

- CLIP (global)
    
- DINOv2 (global)
    

Process in **batches of 16–64** images.  
Append results to Parquet files.

If the kernel dies, you restart at the last completed batch.

---

### Phase IV — Stratification

Use embeddings + cheap features to create **subsets**:

- High-quality
    
- Photo vs non-photo
    
- Text-heavy
    
- Human-present
    
- Dense scenes
    

Write subset flags into `images.parquet`.

---

### Phase V — Expensive semantics (selective)

Only now do you run:

- SAM masks
    
- Object detection
    
- OCR
    
- Depth
    

Each gets:

- Its own notebook
    
- Its own output folder
    
- Its own parquet schema
    

Never mix concerns.

---

### Phase VI — Prompted interpretation

Prompt templates live in Drive:

```yaml
id: caption_v1
task: caption
prompt: "Describe the image factually without interpretation."
```

Notebook loads registry, runs prompts, writes outputs with:

- prompt_id
    
- model_id
    
- version
    

This makes outputs comparable.

---

### Phase VII — Indices and navigation

Build FAISS indices and store them in Drive.

- CLIP index
    
- DINO index
    

You can now:

- Search
    
- Cluster
    
- Sample
    

All inside Colab.

---

## How to survive Colab instability

**Rules**

- Never hold more than one batch in memory
    
- Save after every batch
    
- Log progress to parquet
    
- Assume kernel death every 2–6 hours
    

**Pattern**

```python
for batch in batches:
    if batch_done(batch): continue
    process(batch)
    write(batch)
```

---

## GPU usage in Colab (realistic expectations)

- T4 / L4 GPUs
    
- ~12–24 GB VRAM
    
- Enough for:
    
    - CLIP
        
    - DINO
        
    - SAM
        
    - SD 1.5
        
    - Quantized 7B LLMs
        
- Not enough for:
    
    - SDXL + heavy ControlNet
        
    - Large LLMs unquantized
        

Use:

```python
torch.cuda.empty_cache()
```

aggressively.

---

## What you lose vs AWS

- No serving
    
- No always-on endpoints
    
- No concurrency
    

## What you gain

- $0 cost
    
- Zero ops
    
- Fast iteration
    
- Tight coupling to exploration
    

Given your goal is **exploration and synthesis**, this is actually the right choice.

---

## One final warning (important)

Google Drive **is slow** for lots of small writes.

Mitigate by:

- Writing parquet in chunks
    
- Avoid per-image JSON files
    
- Batch writes aggressively
    

---

If you want, next I can:

- Give you **starter notebooks** for each phase
    
- Define **exact parquet schemas**
    
- Write a **resume-safe batch runner**
    
- Design a **Drive-friendly FAISS workflow**
    

Tell me what you want first.