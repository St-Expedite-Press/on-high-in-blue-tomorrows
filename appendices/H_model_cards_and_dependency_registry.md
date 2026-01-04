# Appendix H: Model Cards and Dependency Registry (Epistemic + Legal Clarity)

[A_World_Burning/README](../A_World_Burning/README.md) | [A_World_Burning/30-whitepaper-toc](../A_World_Burning/30-whitepaper-toc.md) | [A_World_Burning/26-whitepaper-skeleton](../A_World_Burning/26-whitepaper-skeleton.md)

This appendix records the model and dependency surface area that can affect results, licensing, and long-term reproducibility.

Two rules:

1. **No unpinned models.** Every pretrained model run records `model_id` and a pinned revision (`sha` / commit / tag).  
2. **No assumed licenses.** If a license is not declared, record it as `unknown` until verified.

Related:

- Model library: [A_World_Burning/29-model-library.md](../A_World_Burning/29-model-library.md)
- Reproducibility protocol: [appendices/E_reproducibility_protocols.md](E_reproducibility_protocols.md) (source: [A_World_Burning/36-appendix-e-reproducibility-protocols.md](../A_World_Burning/36-appendix-e-reproducibility-protocols.md))

---

## H.1 Model registry (Hugging Face metadata snapshot)

The table below is a **metadata snapshot** gathered from the Hugging Face model API (`/api/models/<modelId>`). Treat these as:

- a registry of admissible instruments
- a reminder of which models currently have declared licenses vs unknown licenses

At run time, you must pin:

- the model revision/sha
- the exact preprocessing settings

### H.1.1 Registry table (by model_id)

| model_id | pipeline_tag | library | license | sha |
|---|---|---|---|---|
| openai/clip-vit-base-patch32 | zero-shot-image-classification | transformers | unknown | 3d74acf9a28c67741b2f4f2ea7635f0aaf6f0268 |
| openai/clip-vit-large-patch14 | zero-shot-image-classification | transformers | unknown | 32bd64288804d66eefd0ccbe215aa642df71cc41 |
| laion/CLIP-ViT-H-14-laion2B-s32B-b79K | zero-shot-image-classification | open_clip | license:mit | 1c2b8495b28150b8a4922ee1c8edee224c284c0c |
| google/siglip-so400m-patch14-384 | zero-shot-image-classification | transformers | license:apache-2.0 | 9fdffc58afc957d1a03a25b10dba0329ab15c2a3 |
| facebook/dinov2-base | image-feature-extraction | transformers | license:apache-2.0 | f9e44c814b77203eaa57a6bdbbd535f21ede1415 |
| facebook/dinov2-large | image-feature-extraction | transformers | license:apache-2.0 | 47b73eefe95e8d44ec3623f8890bd894b6ea2d6c |
| facebook/dinov2-giant | image-feature-extraction | transformers | license:apache-2.0 | 611a9d42f2335e0f921f1e313ad3c1b7178d206d |
| BAAI/EVA-CLIP-8B | feature-extraction | transformers | license:apache-2.0 | 0e4dca944e8ece27eb9dfe4a488c0ed0c4644fc9 |
| apple/aimv2-large-patch14-336-distilled | image-feature-extraction | transformers | license:apple-amlr | c5239aac7c9bb721cb306ab224385a86611ab04d |
| microsoft/BiomedCLIP-PubMedBERT_256-vit_base_patch16_224 | zero-shot-image-classification | open_clip | license:mit | 9f341de24bfb00180f1b847274256e9b65a3a32e |
| nielsr/imagebind-huge |  | transformers | license:cc-by-nc-sa-4.0 | 51fc1ff707903501e60bdb2f73dd4e8818eef099 |
| facebook/sam-vit-huge | mask-generation | transformers | license:apache-2.0 | 87aecf0df4ce6b30cd7de76e87673c49644bdf67 |
| facebook/sam-vit-large | mask-generation | transformers | license:apache-2.0 | 6851e0441005b0fb96f2cc4dfac472f3d1b14af1 |
| facebook/sam-vit-base | mask-generation | transformers | license:apache-2.0 | 70c1a07f894ebb5b307fd9eaaee97b9dfc16068f |
| syscv-community/sam-hq-vit-huge | mask-generation | transformers | license:apache-2.0 | 9d9d53502fbf666297e7eb3804f64137f930055e |
| facebook/mask2former-swin-large-ade-semantic | image-segmentation | transformers | license:other | aa25c92404a40599614215e76514c79b427c7527 |
| Carve/u2net-universal |  |  | license:apache-2.0 | 10305d785481cf4b2eee1d447c39cd6e5f43d74b |
| facebook/detr-resnet-50 | object-detection | transformers | license:apache-2.0 | 1d5f47bd3bdd2c4bbfa585418ffe6da5028b4c0b |
| IDEA-Research/grounding-dino-base | zero-shot-object-detection | transformers | license:apache-2.0 | 12bdfa3120f3e7ec7b434d90674b3396eccf88eb |
| shunk031/aesthetics-predictor-v1-vit-large-patch14 | feature-extraction | transformers | unknown | 74fd3ab002ca9252b5593f079514e6a1eaa132f9 |
| shunk031/aesthetics-predictor-v1-vit-base-patch16 | feature-extraction | transformers | unknown | ca639583a7648b71c302944d20993ae5568239d2 |
| camenduru/improved-aesthetic-predictor |  |  | unknown | 7b2449be1264fcd9a1cf92e3d30dd29af989c836 |
| PerceptCLIP/PerceptCLIP_Memorability |  |  | unknown | 3cbd14123ef9af65d879cb67a3453b9da85688d9 |
| davanstrien/convnext-tiny-224-wikiart | image-classification | transformers | license:apache-2.0 | ba6b504f73656de53b83ad7c2712a4803f68b075 |
| prithivMLmods/WikiArt-Style | image-classification | transformers | license:apache-2.0 | 1bd5b7d2673c15fafb778a03680d142efbed2fb1 |
| prithivMLmods/WikiArt-Genre | image-classification | transformers | license:apache-2.0 | db65c2fa4d5ee9727f28d33b0911b90ee7d71cf4 |
| birder-project/rope_vit_reg4_b14_capi-places365 | image-classification | birder | license:apache-2.0 | a2a400a2c583f108a5fa266db3e15e28bfc5b980 |
| jayanta/microsoft-resnet-50-cartoon-emotion-detection | image-classification | transformers | license:apache-2.0 | 02e12d45209b0e2494ce56b04bdebc2d2f820e45 |
| jayanta/google-vit-base-patch16-224-cartoon-emotion-detection | image-classification | transformers | license:apache-2.0 | 872b11365b397c8e2382c31a0c6b48a4dd94b9a3 |
| imamassi/Visual_Emotional_Analysis | image-classification | transformers | license:apache-2.0 | c8ef79a9dfea89b9e538586f8982e5214156116f |
| PriyamSheta/EmotionClassModel | image-classification | transformers | unknown | 2fded7bc6b1d0ed0267737c5699a659a5a75d558 |
| microsoft/trocr-base-printed | image-to-text | transformers | unknown | 93450be3f1ed40a930690d951ef3932687cc1892 |
| microsoft/trocr-large-printed | image-to-text | transformers | unknown | 9ff792d8e7c22061f2ee67e1ed2246b1f9ef1e98 |
| Salesforce/blip-image-captioning-base | image-to-text | transformers | license:bsd-3-clause | 82a37760796d32b1411fe092ab5d4e227313294b |
| Salesforce/blip2-opt-2.7b | image-text-to-text | transformers | license:mit | 59a1ef6c1e5117b3f65523d1c6066825bcf315e3 |
| Salesforce/blip2-flan-t5-xl | image-text-to-text | transformers | license:mit | 0eb0d3b46c14c1f8c7680bca2693baafdb90bb28 |
| microsoft/Florence-2-base | image-text-to-text | transformers | license:mit | 5ca5edf5bd017b9919c05d08aebef5e4c7ac3bac |
| microsoft/Florence-2-large | image-text-to-text | transformers | license:mit | 21a599d414c4d928c9032694c424fb94458e3594 |
| Qwen/Qwen2-VL-2B-Instruct | image-text-to-text | transformers | license:apache-2.0 | 895c3a49bc3fa70a340399125c650a463535e71c |
| Qwen/Qwen2-VL-7B-Instruct | image-text-to-text | transformers | license:apache-2.0 | eed13092ef92e448dd6875b2a00151bd3f7db0ac |

Notes:

- Some models do not declare `pipeline_tag` or `license` in HF metadata; treat those licenses as `unknown` until verified from the model card or upstream repository.
- “license:other” should be treated as a gating flag: you need to confirm redistribution and usage constraints explicitly before using it in a released dataset.

---

## H.2 Dependency registry (libraries that change results)

The following dependency families must be recorded per run (or per release):

### H.2.1 Data + IO

- python
- numpy
- pillow
- opencv-python
- pyarrow

### H.2.2 ML stack

- torch
- torchvision
- transformers
- open_clip (if used)
- timm (if used)
- segment-anything / SAM implementation (if not using HF pipeline)

### H.2.3 Analysis / viz

- scikit-image
- scikit-learn
- umap-learn (if used)
- hdbscan (if used)
- matplotlib / seaborn / plotly (if used)

Minimum environment capture policy:

- record version strings for all of the above
- record GPU model + CUDA/cuDNN versions (when relevant)

---

## H.3 Bias and failure mode notes (what to admit in writing)

This is not a moral disclaimer; it is an epistemic requirement.

### H.3.1 Embedding backbones

- CLIP-family: imports web-text priors; sensitive to framing and border; can collapse stylistic variance into “semantic similarity.”
- DINOv2-family: reduces text bias; emphasizes structure/texture; can overweight engraving grain and paper texture.
- SigLIP/EVA/AIMv2: different priors; use them to measure disagreement rather than to pick a winner.

### H.3.2 Segmentation

- SAM-family: can fragment on engraving texture; output count can explode; pruning policy becomes part of the method.
- Semantic segmenters (ADE20K): label spaces are not designed for engraving plates; treat as weak channels only.

### H.3.3 Probes (aesthetics/emotion/style)

These are culturally saturated instruments. Their outputs are never treated as truth; they are treated as axes for browsing and comparative drift.

---

## H.4 Hardware tier expectations (operational)

Hardware is part of the method because it shapes feasible parameterizations.

Reference tiers (from the corpus planning):

- T4 (16GB): baseline CLIP + DINOv2-base + SAM-base (careful)
- L4 (24GB): CLIP-H/SigLIP + DINOv2-large + SAM-large/huge (more stable)
- A100 (40GB): maximal sets (DINOv2-giant, heavier VLMs) without gymnastics

Record which tier each run used; do not pretend runs are comparable if they are not.
