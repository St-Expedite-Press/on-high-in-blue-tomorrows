# Model Library (Embeddings + Segmentation)

[[A_World_Burning/README]] | [[A_World_Burning/30-whitepaper-toc]] | [[A_World_Burning/39-appendix-h-model-cards-and-dependency-registry]]

This document is a **consolidated, implementation-facing registry** of the model families repeatedly referenced across the markdown corpus, plus the minimum operational metadata needed to run them under the project’s provenance discipline.

Scope: **embedding backbones**, **segmentation models**, and closely-adjacent “instrument” models (detectors + probes) that affect dataset creation through preprocessing. Downstream diffusion/LoRA tooling is intentionally not the focus here.

Related:
- `A_World_Burning/00_preprocessing_assay.md` (what features/runs exist)
- `A_World_Burning/27-strange-models-compendium.md` (probe rationale + selection strategy)
- `A_World_Burning/33-appendix-b-filesystem-naming-run-ids.md` (run IDs, artifact naming, manifests)
- `A_World_Burning/34-appendix-c-feature-extraction-inventory.md` (feature families + output schemas)

---

## 0) Non-negotiable rules for admitting a model into the canonical pipeline

Any “model” used during preprocessing must be treated as an **instrument**:

1. **Pinned weights**: record the exact revision/sha used (HF `sha` or explicit commit/tag).  
2. **Declared license status**: record a license tag or explicitly mark as `unknown` (do not assume).  
3. **Declared outputs**: output kind (vector/logits/masks/boxes/text) and expected shape/dtype.  
4. **Declared preprocessing**: image resizing/cropping/normalization and any text prompt templates.  
5. **Declared failure mode**: at least one known way the instrument lies (domain mismatch, bias, sensitivity to borders, etc.).  
6. **Sealed run discipline**: every invocation is a run that writes append-only artifacts + manifest rows.

If any of the above is missing, the model stays in “ideas” and does not enter the dataset.

---

## 1) Model identity hygiene (aliases vs real IDs)

Several earlier notes use informal aliases that do not correspond 1:1 to real Hugging Face IDs.

Use this mapping to avoid “ghost” models:

| Corpus alias / shorthand | Canonical HF model ID (recommended) | Notes |
|---|---|---|
| `facebook/dino-v2-base` | `facebook/dinov2-base` | Alias appears in `A_World_Burning/04_sane_model_roster.md`. |
| `facebook/dino-v2-large` | `facebook/dinov2-large` | Same. |
| `facebook/sam-vit-h` | `facebook/sam-vit-huge` | HF uses `-huge/-large/-base`. |
| `facebook/sam-vit-l` | `facebook/sam-vit-large` | Same. |
| `facebook/sam-vit-b` | `facebook/sam-vit-base` | Same. |
| `facebook/mask2former-swin-large-ade` | `facebook/mask2former-swin-large-ade-semantic` | Include `-semantic`. |
| `apple/aimv2-large-patch14` | `apple/aimv2-large-patch14-336-distilled` (or another explicit size) | “AIMv2” models are size-qualified on HF. |
| `IDEA-Research/detrex-mask2former` | (no HF model ID found) | Treat as a codebase name; use the HF Mask2Former checkpoints instead. |

This file uses canonical HF IDs where possible, and records shorthands only as human-friendly aliases.

---

## 2) Metadata capture protocol (HF-first, no hallucinated fields)

For each HF-hosted model used in preprocessing, capture:

- `modelId`
- `pipeline_tag` (task)
- `library_name`
- `license` (or `license:*` tag if `license` field is absent)
- `sha` (HF head revision at time of pinning)
- relevant config fields (output dim, input size)

Practical API endpoints:

- Model metadata: `https://huggingface.co/api/models/<modelId>`
- Config JSON (when present): `https://huggingface.co/<modelId>/raw/main/config.json`
- open_clip config (when present): `https://huggingface.co/<modelId>/raw/main/open_clip_config.json`

This metadata belongs in:

- `runs/<run_id>/run.manifest.json`
- a dependency/model registry appendix (see Appendix H in `A_World_Burning/26-whitepaper-skeleton.md`)

---

## 3) Embedding backbone library (core)

These are the “universal backbones” that define most of the canonical manifold geometry. The minimum recommended ensemble is **CLIP + DINOv2** so disagreement is measurable.

### 3.1 CLIP-family (contrastive vision-language embeddings)

| Role | Model ID | Pipeline | License tag | Output kind | Expected dim (from config) | Canonical input size | Notes |
|---|---|---|---|---|---:|---:|---|
| baseline CLIP | `openai/clip-vit-base-patch32` | `zero-shot-image-classification` | `unknown` | vector | 512 | 224 | Cheap, stable baseline. |
| core CLIP | `openai/clip-vit-large-patch14` | `zero-shot-image-classification` | `unknown` | vector | 768 | 224 | Primary “semantic alignment” axis. |
| heavy CLIP | `laion/CLIP-ViT-H-14-laion2B-s32B-b79K` | `zero-shot-image-classification` | `license:mit` | vector | 1024 | 224 | Often improves aesthetic similarity; heavier VRAM. |

Operational notes:

- Store both **raw** and **L2-normalized** embeddings if you will mix metrics.
- If computing segment/tile embeddings, record crop policy explicitly (padding, mask, alpha handling).

### 3.2 SigLIP-family (CLIP-like, different training recipe)

| Role | Model ID | Pipeline | License tag | Output kind | Expected dim (from config) | Canonical input size | Notes |
|---|---|---|---|---|---:|---:|---|
| alignment alt | `google/siglip-so400m-patch14-384` | `zero-shot-image-classification` | `license:apache-2.0` | vector | 1152 | 384 | Strong alternative embedding prior; larger input size. |

### 3.3 DINOv2-family (self-supervised structure-first embeddings)

| Role | Model ID | Pipeline | License tag | Output kind | Expected dim (from config) | Canonical input size (from config) | Notes |
|---|---|---|---|---|---:|---:|---|
| DINOv2 base | `facebook/dinov2-base` | `image-feature-extraction` | `license:apache-2.0` | vector | 768 | 518 | Good structure axis; less text bias. |
| DINOv2 large | `facebook/dinov2-large` | `image-feature-extraction` | `license:apache-2.0` | vector | 1024 | 518 | Stronger; heavier. |
| DINOv2 giant | `facebook/dinov2-giant` | `image-feature-extraction` | `license:apache-2.0` | vector | 1536 | 518 | Only if GPU tier supports; batch carefully. |

Operational notes:

- DINOv2 expects a larger canonical input size than CLIP; document your resizing choice (518 vs smaller) and treat it as a manifold-shaping decision.

---

## 4) Embedding backbone library (optional / exotic priors)

These are explicitly proposed in the corpus as “orthogonal priors you may want on purpose” (`A_World_Burning/27-strange-models-compendium.md`) and must be treated as additional axes, not replacements.

### 4.1 EVA-CLIP (higher-fidelity aesthetic similarity)

| Role | Model ID | Pipeline | License tag | Output kind | Expected dim (from config) | Canonical input size | Notes |
|---|---|---|---|---|---:|---:|---|
| EVA-CLIP | `BAAI/EVA-CLIP-8B` | `feature-extraction` | `license:apache-2.0` | vector | 1280 | 224 | Very heavy; use only if it changes atlas topology. |

### 4.2 AIMv2 (structure-sensitive global embeddings; Apple)

Pick a size-qualified checkpoint; do not use unqualified aliases.

| Role | Model ID | Pipeline | License tag | Output kind | Expected dim (from config) | Canonical input size | Notes |
|---|---|---|---|---|---:|---:|---|
| AIMv2 recommended | `apple/aimv2-large-patch14-336-distilled` | `image-feature-extraction` | `license:apple-amlr` | vector | 1024 | 336 | “Global structure” axis; size is explicit. |

### 4.3 BiomedCLIP (anatomy bias as a feature, not a bug)

| Role | Model ID | Pipeline | License tag | Output kind | Expected dim (from open_clip config) | Canonical input size | Notes |
|---|---|---|---|---|---:|---:|---|
| BiomedCLIP | `microsoft/BiomedCLIP-PubMedBERT_256-vit_base_patch16_224` | `zero-shot-image-classification` | `license:mit` | vector | 512 | 224 | Use only as an explicitly “biased instrument” axis. |

### 4.4 ImageBind (multimodal alignment; future-proofing)

| Role | Model ID | Pipeline | License tag | Output kind | Expected dim (from config) | Notes |
|---|---|---|---|---|---:|---|
| ImageBind | `nielsr/imagebind-huge` | (none declared) | `license:cc-by-nc-sa-4.0` | vector | 1024 | License is non-commercial; treat as optional/research-only. |

---

## 5) Segmentation model library (region discovery)

Segmentation is used “without semantics” first: **class-agnostic region proposals** that enable region stats + region embeddings without prematurely asserting meaning.

### 5.1 SAM v1 (Segment Anything; class-agnostic masks)

| Role | Model ID | Pipeline | License tag | Output kind | Canonical image size (from config) | Notes |
|---|---|---|---|---|---:|---|
| SAM huge | `facebook/sam-vit-huge` | `mask-generation` | `license:apache-2.0` | masks | 1024 | Primary for best masks if VRAM allows. |
| SAM large | `facebook/sam-vit-large` | `mask-generation` | `license:apache-2.0` | masks | 1024 | Fallback. |
| SAM base | `facebook/sam-vit-base` | `mask-generation` | `license:apache-2.0` | masks | 1024 | Cheap baseline. |

### 5.2 SAM-HQ (higher-quality masks; optional)

| Role | Model ID | Pipeline | License tag | Output kind | Canonical image size (from config) | Notes |
|---|---|---|---|---|---:|---|
| SAM-HQ huge | `syscv-community/sam-hq-vit-huge` | `mask-generation` | `license:apache-2.0` | masks | 1024 | Useful when SAM boundaries are too coarse on engraving textures. |

### 5.3 Semantic segmentation (only when classes are required)

Use only when you need specific class channels (e.g., “sky/water/ground”), and keep it explicitly separate from the class-agnostic mask pipeline.

| Role | Model ID | Pipeline | License tag | Output kind | Canonical input size (from config) | Notes |
|---|---|---|---|---|---:|---|
| ADE20K semantic | `facebook/mask2former-swin-large-ade-semantic` | `image-segmentation` | `license:other` | class map | 384 | License tag is `other`; treat as a gated dependency. |

### 5.4 Lightweight foreground/background baselines (optional)

The corpus mentions a “U2-Net”-style foreground/background baseline (`A_World_Burning/24-etiquette.md`) as a sanity check against heavier models.

One HF candidate with a declared license tag:

| Role | Model ID | Pipeline | License tag | Output kind | Notes |
|---|---|---|---|---|---|
| U2Net baseline | `Carve/u2net-universal` | (none declared) | `license:apache-2.0` | mask | Use as a fast foreground prior; do not treat as semantics. |

---

## 6) Optional detection scaffolds (boxes, counts, spatial relations)

These are not required for preprocessing completion, but they are repeatedly mentioned as useful scaffolds for:

- “count” signals (how many birds? how many objects?)
- spatial relations (bird above water, etc.)
- text-conditioned proposals (for “bird”, “branch”, “egg”, “nest” prompts)

| Role | Model ID | Pipeline | License tag | Output kind | Notes |
|---|---|---|---|---|---|
| DETR baseline | `facebook/detr-resnet-50` | `object-detection` | `license:apache-2.0` | boxes + logits | Opinionated prior; treat as weak signal. |
| GroundingDINO | `IDEA-Research/grounding-dino-base` | `zero-shot-object-detection` | `license:apache-2.0` | boxes + logits | Text-conditioned boxes; prompt registry discipline required. |

---

## 7) “Strange probes” library (weak axes; never authority)

These models do not become canon; they become **measured axes** inside the manifold to make variance legible.

### 7.1 Aesthetics predictors (sorting heuristics; pipeline fingerprinting)

| Role | Model ID | Pipeline | License tag | Output kind | Notes |
|---|---|---|---|---|---|
| aesthetic probe | `shunk031/aesthetics-predictor-v1-vit-large-patch14` | `feature-extraction` | `unknown` | scalar score | Common diffusion-adjacent probe; license not declared in tags. |
| aesthetic probe | `shunk031/aesthetics-predictor-v1-vit-base-patch16` | `feature-extraction` | `unknown` | scalar score | Smaller variant. |
| aesthetic probe | `camenduru/improved-aesthetic-predictor` | (none declared) | `unknown` | scalar score | Treat as unpinned/unverified until audited. |

### 7.2 Memorability (attention economy as signal)

| Role | Model ID | Pipeline | License tag | Output kind | Notes |
|---|---|---|---|---|---|
| memorability probe | `PerceptCLIP/PerceptCLIP_Memorability` | (none declared) | `unknown` | scalar score | Custom repo (no config.json); require manual audit + pin. |

### 7.3 Art-historical envelope probes (WikiArt classifiers)

| Role | Model ID | Pipeline | License tag | Output kind | Notes |
|---|---|---|---|---|---|
| wikiart styles (small) | `davanstrien/convnext-tiny-224-wikiart` | `image-classification` | `license:apache-2.0` | logits | 11-label model; light “envelope” axis. |
| wikiart styles (large) | `prithivMLmods/WikiArt-Style` | `image-classification` | `license:apache-2.0` | logits | 137 labels; SigLIP-based. |
| wikiart genres | `prithivMLmods/WikiArt-Genre` | `image-classification` | `license:apache-2.0` | logits | 43 labels; SigLIP-based. |

### 7.4 Emotion probes (use comparatively; treat as biased)

These are examples listed in `A_World_Burning/27-strange-models-compendium.md`:

| Role | Model ID | Pipeline | License tag | Output kind | Notes |
|---|---|---|---|---|---|
| emotion probe | `jayanta/microsoft-resnet-50-cartoon-emotion-detection` | `image-classification` | `license:apache-2.0` | logits | “Cartoon” prior may be closer to illustration than photo. |
| emotion probe | `jayanta/google-vit-base-patch16-224-cartoon-emotion-detection` | `image-classification` | `license:apache-2.0` | logits | Same. |
| emotion probe | `imamassi/Visual_Emotional_Analysis` | `image-classification` | `license:apache-2.0` | logits | Treat as weak axis only. |
| emotion probe | `PriyamSheta/EmotionClassModel` | `image-classification` | `unknown` | logits | License not declared in tags. |

---

### 7.5 Scene / place priors (weak composition axes)

Mentioned as “mostly relevant for general corpora” but still useful as weak signals about openness/sky dominance (`A_World_Burning/27-strange-models-compendium.md`).

| Role | Model ID | Pipeline | License tag | Output kind | Notes |
|---|---|---|---|---|---|
| Places365 prior | `birder-project/rope_vit_reg4_b14_capi-places365` | `image-classification` | `license:apache-2.0` | logits | Treat as weak axis only; Audubon is not a photo scene dataset. |

---

## 8) Output contracts (what to record per model family)

This is the minimal cross-model contract needed for downstream comparability. Exact column names belong in Appendix C; this section states what must exist.

### 8.1 Embeddings

For each embedding record (plate-level, segment-level, tile-level):

- `model_id` + `model_sha` (pinned)
- `preprocess_tag` (resize/crop policy, normalization, mask handling)
- `vector_dim` (asserted, stored)
- `scope` (plate/segment/tile)
- `vector` or `vector_ref` (inline float list for small scale; or `.npy/.npz` pointer for scale)

### 8.2 Segmentation

For each segmentation record:

- `model_id` + `model_sha` (pinned)
- `mask_ref` (PNG/RLE/COCO) + checksum
- geometry fields (bbox, area, centroid) and normalized ratios
- mask-quality metrics (stability/fragmentation) when available

### 8.3 Probe outputs

For each probe:

- per-plate score or logits vector
- calibration metadata (if any)
- explicit statement of failure modes and intended use

---

## 9) Practical “minimum viable ensemble” recommendation (from the corpus)

If the goal is to get through preprocessing without “model-shopping”:

1. Embeddings: `openai/clip-vit-large-patch14` + `facebook/dinov2-large`
2. Segmentation: `facebook/sam-vit-large` (upgrade to `facebook/sam-vit-huge` if GPU allows)
3. Optional semantic segmentation: `facebook/mask2former-swin-large-ade-semantic` only if you truly need class channels
4. Optional probe: `shunk031/aesthetics-predictor-v1-vit-large-patch14` (sorting) + one WikiArt classifier (envelope axis)

Stop adding models when they stop changing the atlas topology; document that stop condition (see `A_World_Burning/27-strange-models-compendium.md`).

---

## 10) Optional: text-bearing extraction models (OCR + captioning/VLM)

These do not replace embeddings/segmentation; they add weak, explicitly downstream annotation signals that can be embedded and queried.

Important discipline (repeated): prompts and decoding params are part of provenance; treat text as weak signal; never overwrite plate identity fields.

### 10.1 OCR (inscriptions, marginalia, plate labels)

| Role | Model ID | Pipeline | License tag | Output kind | Notes |
|---|---|---|---|---|---|
| OCR baseline | (Tesseract) | (n/a) | (varies) | text + boxes | CPU-friendly; document version and language packs. |
| TrOCR printed | `microsoft/trocr-base-printed` | `image-to-text` | `unknown` | text | HF license tag not declared in metadata; treat as “unknown until verified”. |
| TrOCR printed | `microsoft/trocr-large-printed` | `image-to-text` | `unknown` | text | Heavier; better on small type. |

Notes:

- TrOCR checkpoints are recognition models; you may still need a text-region detector or simple heuristics for plate label zones.

### 10.2 Captioning / VLM (weak labels; prompt-registry required)

| Role | Model ID | Pipeline | License tag | Output kind | Notes |
|---|---|---|---|---|---|
| BLIP caption baseline | `Salesforce/blip-image-captioning-base` | `image-to-text` | `license:bsd-3-clause` | text | Fast factual captions; use for indexing + weak tags. |
| BLIP-2 OPT | `Salesforce/blip2-opt-2.7b` | `image-text-to-text` | `license:mit` | text | Heavier; better descriptions; still “weak label”. |
| BLIP-2 FLAN-T5 | `Salesforce/blip2-flan-t5-xl` | `image-text-to-text` | `license:mit` | text | Often strong for grounded captions. |
| Florence-2 base | `microsoft/Florence-2-base` | `image-text-to-text` | `license:mit` | text + (multi-task) | Multi-task VLM; treat tasks as separate instruments. |
| Florence-2 large | `microsoft/Florence-2-large` | `image-text-to-text` | `license:mit` | text + (multi-task) | Heavier variant. |
| Qwen2-VL small | `Qwen/Qwen2-VL-2B-Instruct` | `image-text-to-text` | (varies) | text | Use when GPU is constrained. |
| Qwen2-VL core | `Qwen/Qwen2-VL-7B-Instruct` | `image-text-to-text` | `license:apache-2.0` | text | Mentioned in `A_World_Burning/04_sane_model_roster.md`. |
| Qwen2-VL large | `Qwen/Qwen2-VL-72B-Instruct` | `image-text-to-text` | (varies) | text | Likely gated/heavy; include only if needed. |

Notes:

- `llava-hf/llava-1.6-13b-hf` and `llava-hf/llava-1.6-34b-hf` appear in older notes, but no public HF model IDs were found at those exact paths; treat them as historical placeholders and resolve to a currently available LLaVA checkpoint before use.
- Some VLM checkpoints may be gated; capture access conditions as part of provenance (token used, acceptance date, etc.).

---

## 11) Optional: ConvNet texture baselines (non-text priors)

The corpus repeatedly calls out “ConvNeXt/EfficientNet pooled features” and even VGG/ResNet-style baselines as useful texture/material axes (`A_World_Burning/00_preprocessing_assay.md`, `A_World_Burning/20-a-real-paper.md`).

These are typically pulled from:

- `torchvision.models` (weights bundled with a specific torchvision version), or
- `timm` (many backbones; weight provenance depends on the specific checkpoint)

Because these are not always stable HF model IDs, the pinning rule changes:

- record `library` + exact version (and ideally git commit)
- record the exact weight identifier (`IMAGENET1K_V1`, etc.) and a checksum of the downloaded weight file when feasible

Recommended “texture axis” candidates (examples):

- ResNet-50 pooled features
- VGG16 pooled features
- EfficientNet-B0/B4 pooled features
- ConvNeXt-Tiny/Small pooled features

Do not treat any of these as canon; they are additional axes whose disagreement can reveal variance modes that CLIP-like models suppress.
