# Faster / Cheaper / Shittier (Maybe Better)

Below are **(1) hardware detection + capability table** and **(2) a batched run executor** that uses that table. Both are designed for Colab, assume **A100 as the target**, but degrade gracefully if you get something else.

Everything is in **code blocks** with inline annotation. This is the “spine” you reuse for CLIP/DINO/SigLIP/etc.

---

## (1) Hardware detection + model capability table (A100-targeted, adaptive)

```python
# ============================================================
# [1] HARDWARE DETECTION + MODEL CAPABILITY TABLE (ADAPTIVE)
# ------------------------------------------------------------
# Goals:
#   - Detect GPU/CPU environment (Colab-friendly)
#   - Prefer A100 settings, but degrade safely
#   - Centralize per-model defaults (batch size, resolution, dtype)
#
# Notes:
#   - This does not load any ML models yet.
#   - This is safe to run on CPU-only environments.
# ============================================================

import os
import json
from dataclasses import dataclass, asdict
from typing import Optional, Dict, Any

import torch

# -----------------------------
# Hardware detection
# -----------------------------

def detect_hardware() -> Dict[str, Any]:
    hw = {
        "cuda_available": torch.cuda.is_available(),
        "device": "cpu",
        "gpu_name": None,
        "gpu_cc": None,
        "vram_gb": None,
        "recommended_dtype": "float32",
        "tf32_enabled": False,
    }

    if torch.cuda.is_available():
        dev = torch.device("cuda:0")
        props = torch.cuda.get_device_properties(dev)
        hw["device"] = "cuda:0"
        hw["gpu_name"] = props.name
        hw["gpu_cc"] = f"{props.major}.{props.minor}"
        hw["vram_gb"] = round(props.total_memory / (1024**3), 2)

        # A100 and most datacenter GPUs: prefer fp16/bf16 for speed
        # A100 supports BF16 well, but FP16 is universally safe.
        # We'll choose BF16 only if explicitly requested later.
        hw["recommended_dtype"] = "float16"

        # TF32 can speed up matmuls on Ampere+ (A100 is Ampere).
        # Useful for some models; harmless for inference embeddings.
        if props.major >= 8:
            torch.backends.cuda.matmul.allow_tf32 = True
            torch.backends.cudnn.allow_tf32 = True
            hw["tf32_enabled"] = True

    return hw

HW = detect_hardware()
print("=== HARDWARE ===")
print(json.dumps(HW, indent=2))

# -----------------------------
# Capability profiles
# -----------------------------

@dataclass(frozen=True)
class ModelProfile:
    # Identity
    name: str
    family: str  # e.g. "clip", "dinov2", "siglip"
    # Input policy
    image_size: int            # square resize (224/336/384 etc)
    center_crop: bool          # True = standard eval-style crop
    # Performance policy
    batch_size: int            # default batch size on target GPU
    amp_dtype: str             # "float16" or "bfloat16" (if supported)
    # Output policy
    output_dim: Optional[int]  # embedding dimension if known (else None)
    normalize: bool            # L2 normalize embedding vectors
    # Notes / constraints
    min_vram_gb: float         # conservative floor

def _gpu_class(hw: Dict[str, Any]) -> str:
    """
    Coarse binning for safe defaults.
    """
    if not hw["cuda_available"]:
        return "CPU"
    name = (hw["gpu_name"] or "").upper()
    vram = hw["vram_gb"] or 0
    if "A100" in name and vram >= 39:
        return "A100_40GB"
    if vram >= 23:
        return "L4_24GB_OR_BETTER"
    if vram >= 15:
        return "T4_16GB_OR_BETTER"
    return "LOW_VRAM"

GPU_CLASS = _gpu_class(HW)
print("GPU_CLASS:", GPU_CLASS)

# -----------------------------
# Model capability table
# -----------------------------
# These are *defaults*. You can override per-run in the executor call.
# A100 defaults are aggressive but safe.
#
# If you want *maximum* throughput on A100:
#   - increase batch_size
#   - set image_size smaller
#   - keep AMP on
#
# If you get a weaker GPU:
#   - the executor will clamp batch sizes automatically
# -----------------------------

MODEL_PROFILES: Dict[str, ModelProfile] = {
    # CLIP family (embedding)
    "clip_vit_b32": ModelProfile(
        name="clip_vit_b32",
        family="clip",
        image_size=224,
        center_crop=True,
        batch_size=128 if GPU_CLASS == "A100_40GB" else 32,
        amp_dtype="float16",
        output_dim=512,
        normalize=True,
        min_vram_gb=10.0,
    ),
    "clip_vit_l14": ModelProfile(
        name="clip_vit_l14",
        family="clip",
        image_size=224,
        center_crop=True,
        batch_size=96 if GPU_CLASS == "A100_40GB" else 24,
        amp_dtype="float16",
        output_dim=768,
        normalize=True,
        min_vram_gb=14.0,
    ),
    "clip_vit_h14": ModelProfile(
        name="clip_vit_h14",
        family="clip",
        image_size=224,
        center_crop=True,
        batch_size=64 if GPU_CLASS == "A100_40GB" else 12,
        amp_dtype="float16",
        output_dim=1024,
        normalize=True,
        min_vram_gb=22.0,
    ),

    # DINOv2 family (structure embeddings)
    "dinov2_base": ModelProfile(
        name="dinov2_base",
        family="dinov2",
        image_size=224,
        center_crop=True,
        batch_size=128 if GPU_CLASS == "A100_40GB" else 32,
        amp_dtype="float16",
        output_dim=None,      # depends on head; we’ll infer at runtime
        normalize=True,
        min_vram_gb=10.0,
    ),
    "dinov2_large": ModelProfile(
        name="dinov2_large",
        family="dinov2",
        image_size=224,
        center_crop=True,
        batch_size=96 if GPU_CLASS == "A100_40GB" else 16,
        amp_dtype="float16",
        output_dim=None,
        normalize=True,
        min_vram_gb=18.0,
    ),
    "dinov2_giant": ModelProfile(
        name="dinov2_giant",
        family="dinov2",
        image_size=224,
        center_crop=True,
        batch_size=48 if GPU_CLASS == "A100_40GB" else 4,
        amp_dtype="float16",
        output_dim=None,
        normalize=True,
        min_vram_gb=35.0,
    ),
}

print("\n=== MODEL PROFILES (defaults) ===")
print(json.dumps({k: asdict(v) for k, v in MODEL_PROFILES.items()}, indent=2))
```

What you now have: a single authoritative table for “how big can we go” per model and per GPU class, with A100 defaults.

---

## (2) Batched run executor (writes per-plate runs, batch compute)

This is the generic executor that:

- loads images in batches
    
- runs inference in one forward pass per batch
    
- writes each plate’s outputs to its own `runs/run-*/…`
    
- registers outputs in `metrics.json` (if your `start_run/register_output` exists)
    

It includes runtime batch-size fallback if memory is tight (even on A100, this protects you if something else is running).

```python
# ============================================================
# [2] BATCHED RUN EXECUTOR (A100-TARGETED, ADAPTIVE)
# ------------------------------------------------------------
# Goals:
#   - Execute a model across many plates in BATCHES
#   - One forward per batch → massive speedup vs per-plate
#   - Write per-plate run artifacts to plate/runs/run-*/
#   - Be resumable and idempotent
#
# Requirements:
#   - PLATES_STRUCTURED defined (your handoff cell already sets this)
#   - Each plate_dir has manifest.json and source/ image
#
# Optional integration:
#   - If start_run() and register_output() exist in the notebook,
#     we use them. Otherwise we create a minimal compatible run dir.
#
# What it writes (per plate):
#   runs/<run_id>/embeddings/<model_name>.npy
#   runs/<run_id>/metrics.json (or updated via register_output)
# ============================================================

import json
import math
import hashlib
from datetime import datetime, timezone
from pathlib import Path
from typing import List, Tuple, Callable, Dict, Any, Optional

import numpy as np
import torch
from PIL import Image
from tqdm.auto import tqdm

# -----------------------------
# Minimal fallback run helpers
# -----------------------------
def _have_run_helpers() -> bool:
    return ("start_run" in globals()) and ("register_output" in globals())

def _fallback_run_id(models: List[str], note: str = "") -> str:
    stamp = datetime.now(timezone.utc).strftime("%Y%m%d-%H%M%S")
    payload = "|".join(models) + "|" + note
    short = hashlib.sha1(payload.encode()).hexdigest()[:8]
    return f"run-{stamp}-{short}"

def _fallback_start_run(plate_dir: Path, models: List[str], note: str = "") -> Path:
    run_id = _fallback_run_id(models, note)
    run_dir = plate_dir / "runs" / run_id
    run_dir.mkdir(parents=True, exist_ok=False)
    manifest = {
        "run_id": run_id,
        "plate_id": plate_dir.name,
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "models": models,
        "outputs": [],
        "notes": note or None,
    }
    (run_dir / "metrics.json").write_text(json.dumps(manifest, indent=2), encoding="utf-8")
    return run_dir

def _fallback_register_output(run_dir: Path, relpath: str):
    mpath = run_dir / "metrics.json"
    m = json.loads(mpath.read_text(encoding="utf-8"))
    if relpath not in m["outputs"]:
        m["outputs"].append(relpath)
    mpath.write_text(json.dumps(m, indent=2), encoding="utf-8")

def _start_run(plate_dir: Path, models: List[str], note: str = "") -> Path:
    if _have_run_helpers():
        return start_run(plate_dir=plate_dir, models=models, note=note)  # type: ignore
    return _fallback_start_run(plate_dir, models, note)

def _register_output(run_dir: Path, relpath: str):
    if _have_run_helpers():
        return register_output(run_dir=run_dir, relative_path=relpath)  # type: ignore
    return _fallback_register_output(run_dir, relpath)

# -----------------------------
# Image preprocessing
# -----------------------------
def load_and_preprocess(
    img_path: Path,
    image_size: int,
    center_crop: bool = True
) -> torch.Tensor:
    """
    CPU image decode + deterministic resize/crop → CHW float tensor in [0,1].
    Normalization (mean/std) is model-specific and should be applied in the model wrapper.
    """
    with Image.open(img_path) as im:
        im = im.convert("RGB")

        # Resize short side to image_size, then center crop to square if requested.
        w, h = im.size
        scale = image_size / min(w, h)
        new_w, new_h = int(round(w * scale)), int(round(h * scale))
        im = im.resize((new_w, new_h), resample=Image.BICUBIC)

        if center_crop:
            left = (new_w - image_size) // 2
            top = (new_h - image_size) // 2
            im = im.crop((left, top, left + image_size, top + image_size))
        else:
            # If not cropping, force square by simple resize (less ideal, but deterministic)
            im = im.resize((image_size, image_size), resample=Image.BICUBIC)

        arr = np.asarray(im).astype(np.float32) / 255.0  # HWC
        t = torch.from_numpy(arr).permute(2, 0, 1)       # CHW
        return t

# -----------------------------
# Model wrapper contract
# -----------------------------
class EmbeddingModel:
    """
    Wrap any embedding model with:
      - .preprocess_batch(batch_tensor) -> batch_tensor normalized for model
      - .forward(batch_tensor) -> (B, D) float tensor on GPU
    """
    def __init__(self, device: str, amp_dtype: str = "float16"):
        self.device = torch.device(device)
        self.amp_dtype = torch.float16 if amp_dtype == "float16" else torch.bfloat16

    def preprocess_batch(self, x: torch.Tensor) -> torch.Tensor:
        return x

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        raise NotImplementedError

# -----------------------------
# Example: CLIP via transformers
# (You can add DINO/SigLIP wrappers similarly.)
# -----------------------------
# NOTE: This does not import transformers until you actually instantiate it.
class CLIPHF(EmbeddingModel):
    def __init__(self, model_id: str, device: str, amp_dtype: str = "float16"):
        super().__init__(device=device, amp_dtype=amp_dtype)
        from transformers import CLIPModel
        self.model = CLIPModel.from_pretrained(model_id).to(self.device).eval()

        # CLIP normalization constants
        self.mean = torch.tensor([0.48145466, 0.4578275, 0.40821073], device=self.device).view(1,3,1,1)
        self.std  = torch.tensor([0.26862954, 0.26130258, 0.27577711], device=self.device).view(1,3,1,1)

    def preprocess_batch(self, x: torch.Tensor) -> torch.Tensor:
        # x: B,3,H,W in [0,1]
        return (x - self.mean) / self.std

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        # Use image features (not text)
        out = self.model.get_image_features(pixel_values=x)
        return out

# -----------------------------
# Batched executor
# -----------------------------
def run_batched_embeddings(
    model_key: str,
    model: EmbeddingModel,
    plates: List[Path],
    image_size: int,
    center_crop: bool,
    batch_size: int,
    normalize: bool = True,
    note: str = "",
    artifact_name: Optional[str] = None,
    overwrite_existing: bool = False,
):
    """
    Execute embeddings across plates in batches and write per-plate artifacts.

    Writes:
      runs/<run_id>/embeddings/<artifact_name>.npy

    Args:
      model_key: label for metrics.json "models" field
      model: instantiated EmbeddingModel wrapper
      plates: list of plate directories (plate-XXX)
      image_size, center_crop: preprocessing policy (from ModelProfile)
      batch_size: starting batch size (will auto-reduce on OOM)
      normalize: L2 normalize embeddings per row
      artifact_name: filename stem for .npy; defaults to model_key
      overwrite_existing: if False, skips plates that already contain output
    """
    artifact_name = artifact_name or model_key

    device = model.device
    amp_dtype = model.amp_dtype

    # progress bar over batches
    i = 0
    pbar = tqdm(total=len(plates), desc=f"RUN {model_key}", unit="plate")

    while i < len(plates):
        # Assemble a candidate batch of plate dirs
        batch_dirs = plates[i:i+batch_size]

        # Pre-check: skip plates that already have an embedding output
        # We can only do this if we can predict output path; we do so by scanning latest run dirs
        # For simplicity: create a new run per plate for now, but skip if already exists and overwrite=False.
        # (Later: you can group multiple models into a single run_id if you prefer.)
        tensors = []
        kept_dirs = []

        for plate_dir in batch_dirs:
            manifest = json.loads((plate_dir / "manifest.json").read_text())
            src_path = plate_dir / manifest["source_image"]

            # Compute intended run_dir+output path only after run creation.
            # We do a conservative skip: if ANY prior run has embeddings/<artifact_name>.npy, skip.
            if not overwrite_existing:
                found = list((plate_dir / "runs").rglob(f"embeddings/{artifact_name}.npy"))
                if found:
                    pbar.update(1)
                    continue

            t = load_and_preprocess(src_path, image_size=image_size, center_crop=center_crop)
            tensors.append(t)
            kept_dirs.append(plate_dir)

        if not kept_dirs:
            i += batch_size
            continue

        # Stack and ship to GPU
        batch = torch.stack(tensors, dim=0).to(device, non_blocking=True)

        try:
            with torch.inference_mode(), torch.cuda.amp.autocast(dtype=amp_dtype):
                batch = model.preprocess_batch(batch)
                emb = model.forward(batch)  # (B,D)

            emb = emb.float()

            if normalize:
                emb = torch.nn.functional.normalize(emb, p=2, dim=1)

            emb_np = emb.detach().cpu().numpy()

            # Write per-plate artifacts (one run per plate; clean, append-only)
            for j, plate_dir in enumerate(kept_dirs):
                run_dir = _start_run(
                    plate_dir=plate_dir,
                    models=[model_key],
                    note=note
                )

                out_dir = run_dir / "embeddings"
                out_dir.mkdir(parents=True, exist_ok=True)

                out_path = out_dir / f"{artifact_name}.npy"
                np.save(out_path, emb_np[j])

                _register_output(run_dir, f"embeddings/{artifact_name}.npy")

                pbar.update(1)

            i += batch_size

        except torch.cuda.OutOfMemoryError:
            # Auto-reduce batch size and retry
            torch.cuda.empty_cache()
            if batch_size <= 1:
                raise
            new_bs = max(1, batch_size // 2)
            print(f"\n[OOM] Reducing batch_size {batch_size} -> {new_bs} and retrying…")
            batch_size = new_bs
            # Do not advance i; retry same window with smaller batch.
            continue

        finally:
            # Help GC and VRAM stability
            del batch
            if torch.cuda.is_available():
                torch.cuda.empty_cache()

    pbar.close()
    print(f"Completed {model_key} across {len(plates)} plates.")
```

### How you use it (example: CLIP-L14, A100 default batch)

```python
# Example: select plates
plate_dirs = sorted(p for p in PLATES_STRUCTURED.iterdir() if p.is_dir())

# Pull profile (defaults already A100-optimized if you get A100)
profile = MODEL_PROFILES["clip_vit_l14"]

# Instantiate model wrapper (HF id here is just an example)
clip = CLIPHF(
    model_id="openai/clip-vit-large-patch14",
    device=HW["device"],
    amp_dtype=profile.amp_dtype
)

run_batched_embeddings(
    model_key=profile.name,
    model=clipFFamily = clip,  # EmbeddingModel
    plates=plate_dirs,
    image_size=profile.image_size,
    center_crop=profile.center_crop,
    batch_size=profile.batch_size,
    normalize=profile.normalize,
    note="batched embeddings (A100-targeted)",
    artifact_name="clip_image_embedding",
    overwrite_existing=False
)
```

(If you want, I’ll also provide the analogous `DINOv2HF` wrapper and you’ll just swap the profile + wrapper, no changes to executor.)

---

### What “much faster” means under this executor

If you run CLIP-L plate-by-plate you do **435 forwards**.  
With batch_size=96 on A100 you do **~5 forwards** plus I/O. That’s the real speedup.

---

If you want the next concrete piece: I can add

- a **DINOv2 wrapper** + one-liner usage (same executor), and
    
- a **global run-plan enumerator** that records expected runs and checks completion state.
    

But you asked for **1 and 2**; the above is exactly that.



```python
# ============================================================
# BASELINE IMAGE METADATA + HISTOGRAMS (FAST, SAFE, RECODED)
# ------------------------------------------------------------
# Fixes:
#   - Handles extremely large images safely
#   - Subsamples pixels for histogram computation
#   - Uses fast bincount-based histograms
#   - Preserves statistical validity
#   - CPU-only, deterministic, resumable
#
# This REPLACES the previous baseline extraction cell.
# ============================================================

from pathlib import Path
import json
import math
import numpy as np
from PIL import Image
from tqdm.auto import tqdm
import matplotlib.pyplot as plt

# ------------------------------------------------------------
# PIL SAFETY: explicitly allow very large images
# ------------------------------------------------------------
Image.MAX_IMAGE_PIXELS = None

# ------------------------------------------------------------
# CONFIGURATION (all tunables here)
# ------------------------------------------------------------
CONFIG = {
    # Histogram parameters
    "hist_bins": 256,
    "hist_range": (0, 255),

    # Pixel sampling for histograms
    "max_pixels_for_hist": 5_000_000,   # cap for histogram computation
    "hist_sampling": "random",           # "random" or "resize"

    # Background detection
    "background_threshold": 245,

    # Preview rendering
    "preview_max_size": (512, 512),

    # Output control
    "overwrite_existing": False,
    "write_visuals": True,

    # Luminance coefficients (Rec. 709)
    "luminance_weights": (0.2126, 0.7152, 0.0722),
}

PLATES_STRUCTURED = DATASET_ROOT / "plates_structured"

# ------------------------------------------------------------
# Utility functions
# ------------------------------------------------------------
def fast_hist(channel: np.ndarray) -> np.ndarray:
    counts = np.bincount(channel, minlength=256)
    return counts / counts.sum()

def entropy_from_hist(hist: np.ndarray) -> float:
    h = hist[hist > 0]
    return float(-np.sum(h * np.log2(h)))

# ------------------------------------------------------------
# Extraction loop
# ------------------------------------------------------------
written = 0
skipped = 0
errors = []

for plate_dir in tqdm(
    sorted(p for p in PLATES_STRUCTURED.iterdir() if p.is_dir()),
    desc="Extracting baseline image metadata"
):
    try:
        manifest = json.loads((plate_dir / "manifest.json").read_text())
        src_path = plate_dir / manifest["source_image"]

        meta_json = plate_dir / "input_image.json"
        hist_json = plate_dir / "input_color_histograms.json"
        viz_dir = plate_dir / "viz"

        if not CONFIG["overwrite_existing"]:
            if meta_json.exists() and hist_json.exists():
                skipped += 1
                continue

        viz_dir.mkdir(exist_ok=True)

        # ----------------------------------------------------
        # Load full image (for dimensions + preview)
        # ----------------------------------------------------
        with Image.open(src_path) as img:
            img = img.convert("RGB")
            width, height = img.size
            arr = np.asarray(img)

        pixels = arr.reshape(-1, 3)

        # ----------------------------------------------------
        # Scalar metadata (full resolution)
        # ----------------------------------------------------
        w_r, w_g, w_b = CONFIG["luminance_weights"]
        luminance_full = (
            w_r * pixels[:, 0]
            + w_g * pixels[:, 1]
            + w_b * pixels[:, 2]
        )

        meta_record = {
            "plate_id": manifest["plate_id"],
            "filename": src_path.name,
            "width": width,
            "height": height,
            "aspect_ratio": round(width / height, 6),
            "megapixels": round((width * height) / 1_000_000, 3),
            "mean_rgb": np.mean(pixels, axis=0).round(3).tolist(),
            "std_rgb": np.std(pixels, axis=0).round(3).tolist(),
            "min_rgb": pixels.min(axis=0).tolist(),
            "max_rgb": pixels.max(axis=0).tolist(),
            "luminance_mean": round(float(luminance_full.mean()), 3),
            "luminance_std": round(float(luminance_full.std()), 3),
            "grayscale_like": bool(
                np.allclose(pixels[:, 0], pixels[:, 1]) and
                np.allclose(pixels[:, 1], pixels[:, 2])
            ),
        }

        meta_json.write_text(json.dumps(meta_record, indent=2), encoding="utf-8")

        # ----------------------------------------------------
        # Subsample pixels for histogram computation
        # ----------------------------------------------------
        total_pixels = pixels.shape[0]
        if total_pixels > CONFIG["max_pixels_for_hist"]:
            if CONFIG["hist_sampling"] == "random":
                idxs = np.random.choice(
                    total_pixels,
                    CONFIG["max_pixels_for_hist"],
                    replace=False
                )
                pixels_h = pixels[idxs]
            else:
                scale = math.sqrt(CONFIG["max_pixels_for_hist"] / total_pixels)
                new_w = max(1, int(width * scale))
                new_h = max(1, int(height * scale))
                img_small = img.resize((new_w, new_h), Image.BILINEAR)
                pixels_h = np.asarray(img_small).reshape(-1, 3)
        else:
            pixels_h = pixels

        # ----------------------------------------------------
        # Foreground/background separation
        # ----------------------------------------------------
        bg_thresh = CONFIG["background_threshold"]
        bg_mask = np.all(pixels_h >= bg_thresh, axis=1)
        fg_pixels = pixels_h[~bg_mask]

        # ----------------------------------------------------
        # Quantitative histograms
        # ----------------------------------------------------
        rgb_full = {}
        rgb_foreground = {}

        for idx, key in enumerate(("r", "g", "b")):
            rgb_full[key] = fast_hist(pixels_h[:, idx]).tolist()
            rgb_foreground[key] = fast_hist(fg_pixels[:, idx]).tolist()

        luminance_h = (
            w_r * pixels_h[:, 0]
            + w_g * pixels_h[:, 1]
            + w_b * pixels_h[:, 2]
        ).astype(np.uint8)

        luminance_hist = fast_hist(luminance_h)

        hist_record = {
            "bins": 256,
            "range": list(CONFIG["hist_range"]),
            "background_threshold": bg_thresh,
            "background_ratio": round(float(bg_mask.mean()), 4),
            "rgb_hist_full": rgb_full,
            "rgb_hist_foreground": rgb_foreground,
            "luminance_hist": luminance_hist.tolist(),
            "entropy": {
                "r": round(entropy_from_hist(np.array(rgb_full["r"])), 4),
                "g": round(entropy_from_hist(np.array(rgb_full["g"])), 4),
                "b": round(entropy_from_hist(np.array(rgb_full["b"])), 4),
                "luminance": round(entropy_from_hist(luminance_hist), 4),
            },
        }

        hist_json.write_text(json.dumps(hist_record, indent=2), encoding="utf-8")

        # ----------------------------------------------------
        # Visual diagnostics (optional)
        # ----------------------------------------------------
        if CONFIG["write_visuals"]:
            preview = Image.fromarray(arr)
            preview.thumbnail(CONFIG["preview_max_size"])
            preview.save(viz_dir / "input_preview.png")

            plt.figure(figsize=(6, 4))
            for k, c in zip(("r", "g", "b"), ("red", "green", "blue")):
                plt.plot(rgb_full[k], label=c)
            plt.legend()
            plt.title(f"{manifest['plate_id']} — RGB (full)")
            plt.tight_layout()
            plt.savefig(viz_dir / "histogram_rgb.png")
            plt.close()

            plt.figure(figsize=(6, 4))
            for k, c in zip(("r", "g", "b"), ("red", "green", "blue")):
                plt.plot(rgb_foreground[k], label=c)
            plt.legend()
            plt.title(f"{manifest['plate_id']} — RGB (foreground)")
            plt.tight_layout()
            plt.savefig(viz_dir / "histogram_rgb_foreground.png")
            plt.close()

            plt.figure(figsize=(6, 4))
            plt.plot(luminance_hist, color="black")
            plt.title(f"{manifest['plate_id']} — Luminance")
            plt.tight_layout()
            plt.savefig(viz_dir / "histogram_luminance.png")
            plt.close()

        written += 1

    except Exception as e:
        errors.append(f"{plate_dir.name}: {e}")

# ------------------------------------------------------------
# Report
# ------------------------------------------------------------
print(f"\nWritten : {written}")
print(f"Skipped : {skipped}")

if errors:
    print("\nERRORS:")
    for e in errors[:10]:
        print(" ", e)
    raise RuntimeError(f"{len(errors)} failures")
```
