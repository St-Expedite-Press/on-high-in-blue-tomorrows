# Benchmarks

Yes - once this becomes a paper, **benchmarks stop being optional**. They are how you make the work legible to _both_ technical reviewers _and_ humanities scholars without flattening the project into a demo.

What’s important is that **your benchmarks are not ImageNet-style accuracy benchmarks**. They are _comparative, longitudinal, and stability-oriented_. Below is a clean taxonomy of what actually applies to _The Burning World_ / Audubon (Ottoman plates included), and how to frame it as serious research.

---

## 1. Baseline benchmarks (you must have these)

These establish **ground truth and invariants**.

### A. Structural invariance benchmarks

Purpose: show what _does not_ change.

Metrics:

- Edge map similarity (before vs after)
    
- Keypoint preservation (ORB/SIFT-like, CPU acceptable)
    
- Shape consistency of primary subjects (IoU on coarse segmentation)
    

Benchmark framing:

> “Despite aggressive chromatic and atmospheric manipulation, structural anatomy remains within X% deviation.”

This reassures historians and art scholars.

---

### B. Pixel-statistical baselines

You already did half of this.

Metrics:

- Mean / variance drift (RGB, luminance)
    
- Entropy change
    
- Frequency-domain energy redistribution (low vs high freq)
    

Benchmark framing:

> “We quantify visual degradation not as noise, but as controlled redistribution of spectral energy.”

This anchors your “burning” metaphor in math.

---

## 2. Comparative embedding benchmarks (this is where it becomes a paper)

These answer: _relative to what?_

### A. Original vs manipulated vs failure

You need **three conditions**:

1. Original plates
    
2. Intentionally transformed plates
    
3. Near-collapse / overburned plates
    

Benchmarks:

- Embedding distance trajectories (CLIP, affect, atmosphere)
    
- Variance across runs
    
- Directionality consistency (are changes aligned?)
    

Key question reviewers will ask:

> “Are your transformations coherent, or just stochastic?”

Your answer:

> “They are directionally consistent across embedding spaces.”

---

### B. Cross-collection benchmark

This is huge.

Compare:

- Audubon / Ottoman plates
    
- Other 19th-century natural history plates
    
- Modern wildlife photography
    
- Climate-disaster photography (optional)
    

Metrics:

- Distance from historical illustration manifold
    
- Drift under identical transformations
    

Framing:

> “We show that historical plates respond differently to stress than modern images.”

That’s a real contribution.

---

## 3. Human-aligned benchmarks (dangerous but powerful)

If done carefully, this elevates the work.

### A. Arousal–valence–dominance alignment

Benchmark:

- Correlation between embedding shifts and expected affective direction
    
- Stability of valence collapse vs arousal increase
    

Claim:

> “Quantitative affect trajectories align with historical narratives of ecological loss.”

This bridges ML and humanities _cleanly_.

---

### B. Inter-annotator agreement (lightweight)

You do NOT need crowdsourcing.

Instead:

- 3–5 expert annotations (you, one historian, one artist, one outsider)
    
- Rank small sets: “more intact” → “more collapsed”
    

Benchmark:

- Kendall τ or Spearman correlation with your metrics
    

This is enough to say:

> “Our metrics track expert intuition.”

---

## 4. Model-behavior benchmarks (if you use VLMs)

If you feed plates to vision-language models:

Benchmarks:

- Caption stability under transformation
    
- Semantic drift rate
    
- Hallucination onset point
    

Example:

> “At X level of degradation, models begin hallucinating species.”

This is extremely publishable.

---

## 5. Ablation benchmarks (reviewers will expect this)

You must show:

- What happens without segmentation
    
- Without affect embeddings
    
- Without structural protection
    

Benchmarks:

- Increased semantic collapse
    
- Increased variance
    
- Loss of historical plausibility
    

This proves your pipeline isn’t arbitrary.

---

## 6. Reproducibility benchmarks

This is quietly crucial.

Metrics:

- Run-to-run variance
    
- Seed sensitivity
    
- Determinism under fixed config
    

Framing:

> “Despite stochastic components, results cluster tightly.”

That reassures technical reviewers.

---

## 7. What NOT to benchmark (important)

Do **not** include:

- Accuracy
    
- Precision/recall
    
- Classification scores
    
- Species recognition metrics
    

They dilute the paper and miss the point.

---

## How to frame the paper

Your benchmarks support **three core claims**:

1. Historical images occupy a distinct visual manifold.
    
2. Controlled degradation moves them along coherent, measurable trajectories.
    
3. These trajectories align with affective and narrative interpretations of ecological collapse.
    

This is not a “cool pipeline” paper.

It is:

- digital humanities
    
- computational art history
    
- vision science
    
- climate aesthetics
    

---

## Where this could land

Depending on framing:

- Digital humanities journals
    
- Computer vision + humanities workshops
    
- Computational aesthetics venues
    
- Art history + ML symposia
    

If you want, next we can:

- outline the paper section-by-section
    
- define exact benchmark tables
    
- or design a **single master figure** that visually + quantitatively explains the entire project
