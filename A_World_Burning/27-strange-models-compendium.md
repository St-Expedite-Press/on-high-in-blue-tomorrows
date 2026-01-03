# Strange Models Compendium (Embeddings as Instruments)

[[A_World_Burning/README]] | [[A_World_Burning/30-whitepaper-toc]] | [[A_World_Burning/29-model-library]]

This document deepens the “strangest embeddings” thread into an **operational catalog** of unusual model families and probe strategies that can act as **epistemic instruments** inside a canonical manifold.

Core rule (repeated): **these models do not produce truth**. They produce **measurements** (often weak, biased, or culturally saturated) that become useful only when:

- versioned and provenance-captured,
- compared across multiple instruments,
- treated as axes of variance rather than labels of meaning.

This is written to be compatible with the run/ledger discipline: every model/probe here can be expressed as a sealed run that emits:

- per-plate scores (scalars),
- per-plate vectors (embeddings),
- optional maps (saliency, depth, masks),
- and a ledger row linking everything back to disk.

---

## 0. Why “strange” models matter here

Standard CV instrumentation (CLIP/DINO/SAM) gives:

- semantic alignment (CLIP),
- structure-first similarity (DINOv2),
- region proposals (SAM).

“Strange” models give additional **orthogonal axes** that are not reducible to “what object is it?”:

- affective temperature (not sentiment, but tone)
- perceived dominance/fragility (AVD-style)
- atmosphere (oppressive vs luminous vs pastoral)
- historical plausibility distance (staying inside/outside an art-historical envelope)
- memorability/interestingness (attention economy as a signal)
- negative space / absence (composition as loss)

These axes are especially aligned with “canon under conditions of variance” because they model **how images are read** under different perceptual regimes, including regimes that are unstable.

---

## 1. Admission rules: what qualifies as an “instrument” in this project

Before any new model/probe enters the pipeline, it must have:

- A declared purpose (what question it answers)
- A declared output type (scalar / vector / map / text)
- A declared failure mode (at least one known way it lies)
- A license check (model + weights + training data constraints)
- A reproducibility note (deterministic? nondeterministic? what affects it?)
- A storage plan (what files are written; what ledger columns are populated)

If any of these are missing, the instrument is not admissible.

### 1.1 Model card provenance (required when using pretrained models)

If the instrument is a pretrained model (Hugging Face or otherwise), capture enough metadata to make it reproducible and legally legible:

- model identifier (e.g., HF `modelId`)
- pipeline tag / task type
- license (if declared; if absent, record as **unknown** until verified)
- base model lineage (if declared)
- training dataset tags (if declared)
- revision/commit SHA (HF “revision”) used to pin weights

Example model API endpoints (for automated capture):

- `https://huggingface.co/api/models/<modelId>`

This metadata belongs in the run manifest and should be mirrored into a dependency registry appendix.

---

## 2. A note on Audubon domain mismatch

Audubon plates are:

- illustrations with engraving logic,
- paper tone and border artifacts,
- inscription text,
- non-photographic color distributions.

Many “strange” models are trained on **photographic web images** and will import biases.

That is not disqualifying — it is precisely why we treat them as **instruments with priors**, and why we:

- use ensembles,
- store disagreement,
- and prefer comparative/relative readings over absolute scores.

---

## 2.1 Exotic backbone families (orthogonal priors you may want on purpose)

Even before you get to “strange probes”, you can gain a lot by adding embedding backbones that fail differently:

- **SigLIP** (strong alignment, different training recipe than CLIP)
- **EVA-CLIP** (often higher fidelity for aesthetic similarity)
- **AIMv2** (structure-sensitive global embeddings; different inductive bias)
- **BiomedCLIP** (surprisingly useful when “anatomy bias” is a feature, not a bug)
- **ImageBind** (multimodal alignment; future-proofing)

Operationally, treat these as additional embedding columns in `embeddings.parquet`, not as replacements for CLIP/DINO.

---

## 3. Strange axis family: Affect / Emotion (image emotion recognition)

### 3.1 What it captures

- coarse emotional framing (“tense”, “serene”, “joyful”, “fearful”, etc.)
- often reflects training set stereotypes more than “truth”

### 3.2 How it should be used here

- only comparatively (plate vs plate; or same plate across variants)
- as a weak axis for ordering, not labeling
- never as a claim about Audubon’s intent

### 3.3 Concrete candidate models (Hugging Face examples)

These exist as `image-classification` models and can be evaluated as probes:

- `https://huggingface.co/jayanta/microsoft-resnet-50-cartoon-emotion-detection`
- `https://huggingface.co/jayanta/google-vit-base-patch16-224-cartoon-emotion-detection`
- `https://huggingface.co/PriyamSheta/EmotionClassModel`
- `https://huggingface.co/imamassi/Visual_Emotional_Analysis`

Warning: several are explicitly “cartoon” or non-photographic oriented; that may be an advantage for Audubon, but it also implies unknown label semantics and dataset biases.

### 3.4 Better strategy (recommended): probe on top of robust embeddings

Instead of trusting emotion classifiers, build an affect axis by:

- extracting CLIP and DINO embeddings,
- training a small linear probe (or ridge regression) on an external affect dataset,
- then using the probe only as a comparative axis inside the manifold.

This keeps “instrument behavior” explicit and auditable.

### 3.5 What to store

- per-plate emotion logits/probabilities (vector of label scores)
- per-plate top-k labels (for browsing only)
- calibration metadata (if you do temperature scaling)

---

## 4. Strange axis family: Arousal–Valence–Dominance (AVD)

### 4.1 Why AVD is unusually aligned with this project

AVD models not “what is it?”, but:

- arousal: calm ↔ activated
- valence: pleasant ↔ unpleasant (use carefully; culturally biased)
- dominance: controlled ↔ overwhelmed

Dominance in particular maps cleanly onto “world losing stability”.

### 4.2 How to obtain AVD measurements (three viable approaches)

1) **Direct AVD regressors** (if you find reliable ones)  
2) **Derived AVD from emotion distributions** (map categorical emotions into AVD space)  
3) **Prompt-based AVD via CLIP similarity**:

- build a fixed adjective set for each axis (e.g., calm/tense, pleasant/bleak, dominant/overwhelmed)
- measure CLIP similarity to each adjective template
- treat the difference as an axis coordinate

Approach (3) is primitive but auditable, and it makes priors explicit.

### 4.3 What to store

- AVD triplet per plate (scalars)
- the adjective set and prompt templates used (versioned prompt registry)
- confidence proxies (axis margin; ensemble agreement)

---

## 5. Strange axis family: Atmosphere / Mood (art-facing “world tone”)

### 5.1 What it captures

- “luminous”, “oppressive”, “pastoral”, “desolate”, “fragile”, etc.

### 5.2 Two practical implementations

- **Prompt-based mood probes** (CLIP text-image similarity against mood lexicon)
- **Caption → embed → mood**:
  - generate factual captions (BLIP-2)
  - generate interpretive captions (LLaVA/Qwen2-VL) *as weak labels only*
  - embed captions and cluster by mood language

### 5.3 Storage

- mood axis scores (scalars)
- lexicon + prompts (versioned)
- optional mood cluster IDs (derived)

---

## 6. Strange axis family: Aesthetics / “Interestingness” / Print fitness

### 6.1 Why it belongs (with skepticism)

Even if you reject aesthetic authority, “aesthetic model outputs” can act as:

- a sorting heuristic for human review,
- a proxy for “signal density” or composition salience,
- a bias detector across digitization pipelines (institution A consistently “scores higher”).

### 6.2 Concrete candidate models (Hugging Face examples)

CLIP-based aesthetic predictors (common in diffusion tooling ecosystems):

- `https://huggingface.co/shunk031/aesthetics-predictor-v1-vit-large-patch14`
- `https://huggingface.co/shunk031/aesthetics-predictor-v1-vit-base-patch16`
- `https://huggingface.co/camenduru/improved-aesthetic-predictor`

Operational note: not all popular “aesthetic predictors” declare a license field in their model card metadata. Treat license as **unknown** until verified and record that explicitly.

### 6.3 What to store

- scalar aesthetic score per plate
- score distribution per source/variant group (pipeline fingerprinting)
- model and checkpoint IDs + preprocessing settings

### 6.4 Red line

Do not use aesthetic scores to claim “better” or “more canonical.”  
They are operational signals only.

---

## 7. Strange axis family: Memorability (attention economy as a signal)

### 7.1 What it captures

- a proxy for how likely an image is to be remembered
- often correlates with composition, contrast, novelty, and training priors

### 7.2 Concrete candidate model (Hugging Face example)

- `https://huggingface.co/PerceptCLIP/PerceptCLIP_Memorability`

Model card note (example of the kind of provenance fields to record):

- declares base model lineage (`openai/clip-vit-large-patch14`) and paper reference (`arxiv:2503.13260`) in tags

### 7.3 Why it’s useful here

Memorability can be used as:

- a scan of “canonical salience” across plates without asserting meaning,
- a way to detect whether certain digitization pipelines consistently suppress or amplify salient structure.

### 7.4 What to store

- memorability score per plate
- optionally a paired “salience map” if the method supports it (many do not)

---

## 8. Strange axis family: Art-historical similarity (staying inside an engraving envelope)

### 8.1 What it captures

- proximity to learned distributions of “art styles” or “genres”
- can act as a proxy for when a transformation becomes anachronistic

### 8.2 Concrete candidate models (WikiArt-trained examples)

- `https://huggingface.co/davanstrien/convnext-tiny-224-wikiart`
- `https://huggingface.co/prithivMLmods/WikiArt-Style`
- `https://huggingface.co/prithivMLmods/WikiArt-Genre`

Model card note: `davanstrien/convnext-tiny-224-wikiart` advertises a training dataset tag (`dataset:wiki_art`) and an Apache-2.0 license tag; record these fields in the dependency registry.

### 8.3 Two robust uses

- **Comparative drift:** plate variants from different institutions drift differently in “style space”
- **Transformation guardrail:** enforce that counterfactual stress remains within some plausibility band (if you choose)

### 8.4 What to store

- style logits (vector)
- top-k predicted styles (for browsing only)
- aggregated “distance from engraving envelope” (derived; must be defined)

---

## 9. Strange axis family: Place/scene priors (mostly relevant for general corpora)

Audubon plates are not scenes in the Places365 sense, but scene embeddings can still produce signals about:

- “outdoor-ness”, openness, sky dominance
- which can correlate with background composition

Example model (Places365-trained):

- `https://huggingface.co/birder-project/rope_vit_reg4_b14_capi-places365`

Use with caution; treat as weak signals only.

---

## 10. Strange axis family: Forensics / manipulation cues (why include even if you’ll manipulate later?)

These are generally more relevant for mixed corpora than Audubon, but they are part of the “maximum surface area” extraction doctrine:

- tamper/splice cues (ELA, noise residual inconsistency)
- AI-generation detectors (weak; error-prone)

For Audubon specifically, these may become:

- pipeline fingerprint detectors (recompression/resampling artifacts)
- “institutional divergence” measures (how aggressively images were processed)

Output storage should be “weak signal” tables, not hard labels.

---

## 11. Strange axis family: Derived “stress embeddings” (model-agnostic)

These are not pretrained models; they are **derived feature vectors** built from:

- entropy, edge density, Laplacian variance
- frequency-domain slopes
- background/paper dominance ratios
- segmentation boundary ambiguity metrics

Why they matter:

- explainable, auditable, and domain-relevant
- can function as a second embedding space (structural exhaustion space)

Store as:

- a small per-plate vector (`stress_vec`)
- plus the scalar components used to build it

---

## 12. Narrative tension embeddings (VLM as a sampler of cultural priors)

This is explicitly speculative but methodologically coherent when treated as weak signal:

- Prompt a VLM with neutral templates:
  - “Describe the scene in one sentence, factually.”
  - “What is about to happen?” (narrative expectation)
- Embed the resulting text; compare across variants and transformations.

Model candidates (examples; evaluate feasibility on your GPU tier):

- BLIP-2 family (factual captions)
- LLaVA family (dense descriptions)
- Qwen2-VL family (instruct VLM)
- Florence-2 (multi-task VLM)

Critical discipline:

- prompts are versioned
- outputs are treated as weak labels
- never overwrite known metadata

---

## 13. Instrument selection strategy (“information gain per GPU hour”)

A sane “strange stack” for Audubon, ordered by likely value:

1) Aesthetic predictor (scalar) — quick browsing + pipeline bias detection  
2) WikiArt style logits (vector) — historical envelope axis  
3) Memorability (scalar) — salience proxy  
4) Prompt-based mood lexicon via CLIP (scalars) — atmosphere axis  
5) AVD prompt axes (3 scalars) — dominance collapse axis  
6) VLM narrative prompts (text + embedded) — only after structure exists  

Stop adding instruments when they stop changing the atlas topology (documented stop condition).

---

## 14. What each instrument must emit (run + ledger requirements)

Minimum for any instrument run:

- `run.manifest.json` with:
  - model IDs, checkpoint IDs, preprocessing settings
  - config hash
  - input variant pointer(s)
  - output pointer(s)
- plate-local artifacts (as appropriate):
  - score JSON / NP arrays / maps
- ledger rows:
  - `runs.parquet`: run metadata
  - a specific table or a column group in `plates.parquet` / `embeddings.parquet`

Never store “interpretive prose” as if it were a measured field.

---

## 15. Prompt-based probes (when you don’t want another model)

Some “strange axes” are best implemented as **explicit prompt sets** over a stable embedding model (usually CLIP), because:

- the axis definition is transparent and editable,
- prompts can be versioned like code,
- you avoid importing a new opaque training dataset.

### 15.1 Probe families worth formalizing (examples)

- **Medium/format probes** (illustration vs scan vs engraving vs photograph)
- **Atmosphere probes** (pastoral vs oppressive vs desolate vs luminous)
- **Absence probes** (empty/voided/blank vs dense/filled/overgrown)
- **Stability probes** (stable/ordered vs chaotic/failing/dissolving)

### 15.2 Non-negotiable discipline

- prompts live in a versioned prompt registry
- each score stores the prompt_id + prompt_version/hash
- do not edit prompts “in place” without bumping the version

---

## 16. Ensemble protocol (truth emerges where multiple bad instruments agree)

If you keep only one rule from this document, keep this one:

> Never trust a single embedding space or single probe.

Operationally:

- store **at least two** orthogonal embedding families (CLIP + DINOv2)
- when you add a strange axis, store:
  - the axis score itself
  - an **agreement signal** (how consistent is it across instruments?)
  - a **disagreement signal** (ambiguity detector)

Why:

- agreement surfaces robust structure
- disagreement surfaces interpretive tension and instability (often the interesting part)
