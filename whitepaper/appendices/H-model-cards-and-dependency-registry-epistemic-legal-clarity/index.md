<!-- Auto-generated TOC-aligned file. Source of truth: A_World_Burning/26-whitepaper-skeleton.md -->

# Appendix H: Model Cards and Dependency Registry (epistemic + legal clarity)

_TOC-aligned entrypoint. Master outline lives in `A_World_Burning/26-whitepaper-skeleton.md`._


**Goal:** list everything that could bias results or violate licensing.

- H.1 Model list by role
  - embeddings: CLIP, DINOv2, SigLIP, EVA-CLIP, etc.
  - segmentation: SAM, Mask2Former
  - OCR: Tesseract/TrOCR (if used)
  - captioning/VLM: BLIP-2, LLaVA, Qwen2-VL, Florence-2 (if used)
- H.2 For each model:
  - checkpoint ID
  - license
  - known biases
  - input preprocessing
  - output dimensionality + normalization
- H.3 Library dependency registry (Python + OS-level)
- H.4 Reproducibility warnings (where results vary across versions)
- H.5 Hardware tier expectations (if using Colab)
  - H.5.a T4 (16GB) baseline assumptions and safe model set
  - H.5.b L4 (24GB) ?sweet spot? assumptions and expanded model set
  - H.5.c A100 (40GB) optional ?maximal? set (non-blocking)
  - H.5.d dtype policy (fp16/bf16/tf32) and its implications for comparability

