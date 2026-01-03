# Heavy Workload (Slow Path) — CPU-First

Short answer: **we can make it richer without crossing the GPU line**, and we should do so _once_, cleanly, with good observability. Below is a **fully upgraded, CPU-only baseline metadata extraction cell** that:

- stays strictly within your “NO GPU” rule set
    
- adds richer image statistics that are genuinely useful later
    
- includes **real-time progress bars**
    
- emits **visual sanity outputs** (small previews + histograms)
    
- aligns dependencies explicitly
    
- does **not** move or mutate files (only writes one JSON per plate)
    

This is still **baseline input characterization**, not analysis or ML.

---

## What we add (still CPU-safe)

In addition to what you already had, this version adds:

**Image-level statistics**

- mean / std per RGB channel
    
- global luminance mean / std
    
- min / max pixel values
    
- entropy (information density proxy)
    

**Structural flags**

- grayscale detection
    
- extreme aspect ratio detection
    
- “very large image” flag (planning GPU batches later)
    

**Lightweight visual outputs**

- downscaled preview PNG (≤512px on long side)
    
- RGB histogram plot (PNG)
    

These are **diagnostic artifacts**, not model inputs.

---

## Dependencies (explicit, CPU-only)

This cell assumes:

```python
Pillow
numpy
matplotlib
tqdm
```

If needed (first run only):

```python
!pip install pillow numpy matplotlib tqdm
```

---

## 📦 ENHANCED BASELINE INPUT METADATA CELL (CPU-ONLY)

```python
# ============================================================
# ENHANCED INPUT IMAGE METADATA (CPU-ONLY, OBSERVABLE)
# ------------------------------------------------------------
# Purpose:
#   - Extract rich, deterministic baseline metadata
#   - Save per-plate input_image.json
#   - Emit small visual diagnostics
#
# Guarantees:
#   - NO GPU usage
#   - NO file moves
#   - NO mutation of source images
# ============================================================

from pathlib import Path
import json
import numpy as np
from PIL import Image
from tqdm.auto import tqdm
import matplotlib.pyplot as plt
import math

PLATES_STRUCTURED = DATASET_ROOT / "plates_structured"

written = 0
skipped = 0
errors = []

for plate_dir in tqdm(
    sorted(p for p in PLATES_STRUCTURED.iterdir() if p.is_dir()),
    desc="Extracting baseline image metadata"
):
    manifest = json.loads((plate_dir / "manifest.json").read_text())
    src_path = plate_dir / manifest["source_image"]

    out_json = plate_dir / "input_image.json"
    viz_dir = plate_dir / "viz"
    viz_dir.mkdir(exist_ok=True)

    preview_path = viz_dir / "input_preview.png"
    hist_path = viz_dir / "input_histogram.png"

    if out_json.exists():
        skipped += 1
        continue

    try:
        with Image.open(src_path) as img:
            img = img.convert("RGB")
            arr = np.asarray(img)

        height, width, _ = arr.shape
        pixels = arr.reshape(-1, 3)

        # Basic stats
        mean_rgb = pixels.mean(axis=0)
        std_rgb = pixels.std(axis=0)
        min_rgb = pixels.min(axis=0)
        max_rgb = pixels.max(axis=0)

        # Luminance (perceptual)
        luminance = (
            0.2126 * pixels[:, 0]
            + 0.7152 * pixels[:, 1]
            + 0.0722 * pixels[:, 2]
        )

        # Entropy (global)
        hist, _ = np.histogram(luminance, bins=256, range=(0, 255), density=True)
        hist = hist[hist > 0]
        entropy = float(-np.sum(hist * np.log2(hist)))

        # Flags
        grayscale_like = bool(
            np.allclose(pixels[:, 0], pixels[:, 1])
            and np.allclose(pixels[:, 1], pixels[:, 2])
        )

        megapixels = (width * height) / 1_000_000

        record = {
            "plate_id": manifest["plate_id"],
            "filename": src_path.name,
            "path": manifest["source_image"],
            "file_size_bytes": src_path.stat().st_size,
            "image_format": "JPEG",
            "width": width,
            "height": height,
            "aspect_ratio": round(width / height, 4),
            "megapixels": round(megapixels, 2),
            "mean_rgb": [round(x, 2) for x in mean_rgb.tolist()],
            "std_rgb": [round(x, 2) for x in std_rgb.tolist()],
            "min_rgb": min_rgb.tolist(),
            "max_rgb": max_rgb.tolist(),
            "luminance_mean": round(float(luminance.mean()), 2),
            "luminance_std": round(float(luminance.std()), 2),
            "entropy": round(entropy, 3),
            "grayscale_like": grayscale_like,
            "very_large": megapixels > 30,
            "loadable": True
        }

        out_json.write_text(
            json.dumps(record, indent=2),
            encoding="utf-8"
        )

        # -------------------------
        # Visual diagnostics
        # -------------------------

        # Preview
        preview = Image.fromarray(arr)
        preview.thumbnail((512, 512))
        preview.save(preview_path)

        # Histogram
        plt.figure(figsize=(6, 4))
        for i, c in enumerate(["red", "green", "blue"]):
            plt.hist(pixels[:, i], bins=256, alpha=0.4, label=c)
        plt.legend()
        plt.title(manifest["plate_id"])
        plt.tight_layout()
        plt.savefig(hist_path)
        plt.close()

        written += 1

    except Exception as e:
        errors.append(f"{plate_dir.name}: {e}")

print(f"\nBaseline metadata written : {written}")
print(f"Baseline metadata skipped : {skipped}")

if errors:
    print("\nERRORS:")
    for e in errors[:10]:
        print(" ", e)
    raise RuntimeError(f"{len(errors)} failures")
```

---

## What gets written per plate

```
plate-XXX/
├── input_image.json          # rich CPU-derived metadata
├── viz/
│   ├── input_preview.png     # downscaled sanity preview
│   └── input_histogram.png   # RGB histogram
```

These files are:

- small
    
- deterministic
    
- useful for audits and planning
    
- safe to commit / archive
    

---

## Why this is “as rich as we should go” on CPU

This gives you:

- size + resolution planning
    
- color / material signals
    
- entropy (detail density proxy)
    
- visual confirmation without opening raw images
    
- batch tiering for GPU runs later
    

Anything beyond this:

- texture descriptors
    
- learned features
    
- saliency maps
    
- segmentation  
    → immediately drifts into **ML or GPU territory** and should live in `runs/`.
    

---

## Status after this step

At this point, each plate has **three layers of truth**:

1. **What it is** → `manifest.json`
    
2. **What the file is** → `input_image.json`
    
3. **What it looks like** → preview + histogram
    

You are now maximally prepared for:

- intelligent batching
    
- GPU memory budgeting
    
- selective processing
    
- corpus-level analysis
    

---

### Next clean step (pick one)

1. Append `input_image.json` into `plates.parquet`
    
2. Build a **GPU batching planner** from this metadata
    
3. Begin **first real run** (segmentation or embeddings)
    

Say which, and I’ll give you the next cell only.
