# First Extraction Plan (GPU/CPU Split)

Short answer: **some are GPU-necessary, some are GPU-optional, some are GPU-wasteful**. You should be explicit per notebook.

Below is the clean breakdown, tied directly to the pipeline you’ve built.

---

## 1. What absolutely does **NOT** need a GPU

These should **never** request a GPU. Using one here is just burning quota.

- Project handoff / loading
    
- Manifest creation and validation
    
- JSON schema validation
    
- Checksum computation
    
- File moves / copies
    
- Ledger initialization (`pyarrow`, Parquet I/O)
    
- Ledger population from manifests
    
- Simple image I/O (PIL load, resize, format checks)
    
- Metadata inspection, statistics, counts
    

**Rule:**  
If the operation is _symbolic, structural, or tabular_, CPU only.

---

## 2. GPU-optional (CPU works, GPU is a speed multiplier)

These can run on CPU, but GPU is useful if you’re doing them **at scale** (hundreds of plates).

- CLIP embeddings (ViT-B/32, ViT-L/14)
    
- DINO / DINOv2 embeddings
    
- BLIP / BLIP-2 captioning (small models)
    
- Color statistics with heavy per-pixel ops
    
- OCR / text detection models (medium size)
    

**Typical pattern**

- CPU: feasible for 1–20 plates
    
- GPU: preferable for 100–435 plates
    

On Colab:

- CPU-only is fine for prototyping
    
- Switch to GPU when batching across the full corpus
    

---

## 3. GPU-necessary (don’t bother without one)

These are **not realistically usable** on CPU for your dataset.

- **SAM / SAM-HQ segmentation**
    
- High-resolution diffusion (Stable Diffusion, SDXL)
    
- Super-resolution models (ESRGAN, SwinIR, Real-ESRGAN)
    
- Vision-language models >1B params (BLIP-2 large, LLaVA)
    
- Any multi-pass vision model with attention over full images
    

For Audubon plates specifically:

- SAM on full-res plates → GPU required
    
- Diffusion-conditioned reinterpretations → GPU required
    

---

## 4. Practical recommendation (how to structure notebooks)

You should explicitly mark notebooks like this:

### 🟢 CPU notebooks

- `00_handoff.ipynb`
    
- `01_validate_dataset.ipynb`
    
- `02_populate_plates_ledger.ipynb`
    
- `03_metadata_analysis.ipynb`
    

Run with:

```
Runtime → Change runtime type → CPU
```

---

### 🟡 Hybrid notebooks

- `10_embeddings_clip.ipynb`
    
- `11_embeddings_dino.ipynb`
    
- `12_captioning.ipynb`
    

Start CPU for debugging, then switch to GPU for full runs.

---

### 🔴 GPU notebooks

- `20_segmentation_sam.ipynb`
    
- `30_diffusion_runs.ipynb`
    
- `40_super_resolution.ipynb`
    

These should:

- Assume GPU availability
    
- Assert CUDA at startup
    
- Fail fast if GPU not present
    

Example guard:

```python
import torch
assert torch.cuda.is_available(), "GPU required for this notebook"
```

---

## 5. Colab-specific reality (important)

Given what you said earlier:

> GPU hours on Colab are _absolutely_ not an issue

Then your strategy is correct:

- Do **all orchestration, validation, ledger work** on CPU
    
- Save GPU strictly for:
    
    - segmentation
        
    - embeddings at scale
        
    - generative work
        

This keeps runs:

- reproducible
    
- restartable
    
- cheap in cognitive overhead
    

---

## 6. One-line rule to remember

> **If the notebook creates new pixels or large vectors → GPU.  
> If it only moves, names, validates, or counts things → CPU.**

If you want, next I can:

- tag your planned notebooks explicitly as CPU/GPU
    
- give you a standard GPU-assert header cell
    
- or design a batching strategy to minimize GPU spin-up cost
    

Just say which.
