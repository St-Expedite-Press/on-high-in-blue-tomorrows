<!-- Auto-generated TOC-aligned file. Source of truth: A_World_Burning/26-whitepaper-skeleton.md -->

# XIII. Machine Learning as Instrument, Not Oracle

[[whitepaper/DRAFT]] | [[whitepaper/MATERIALS_MAP]] | [[A_World_Burning/39-appendix-h-model-cards-and-dependency-registry]] | [[A_World_Burning/27-strange-models-compendium]]

_TOC-aligned entrypoint. Master outline lives in `A_World_Burning/26-whitepaper-skeleton.md`._

---

## Draft (body text)

Machine learning is admitted here as instrumentation: a way of producing measurements that help render difference legible. ML is explicitly refused as an oracle of meaning, intent, or truth.

### XIII.1 The instrument rule

ML may:

- measure similarity in multiple spaces (embeddings),
- decompose structure (segmentation),
- generate salience maps and robustness curves.

ML may not:

- decide what a plate “is about” as documentary fact,
- produce authoritative species identifications as truth labels,
- produce restoration authority (“this is the true original color”).

### XIII.2 Why single embedding spaces are untrustworthy

A single embedding space quickly becomes a hidden canon: whatever the model emphasizes becomes what the system “sees.” This project treats plurality as a requirement:

- use an ensemble of embedding families (e.g., CLIP-family + self-supervised ViTs),
- treat disagreement between instruments as evidence of ambiguity or domain mismatch,
- record model versions, revisions, and known biases explicitly.

### XIII.3 Bias and domain mismatch

Audubon plates are illustrations; most foundation models are trained heavily on photographs and internet text. Bias can appear as:

- systematic mis-grouping driven by background textures or inscriptions,
- caption priors that overwrite visual structure,
- Western art-history categories imported as defaults.

The response is not to pretend bias disappears; it is to document it (Appendix H), test it, and treat it as a first-class limitation (Appendix I).

### XIII.4 Strange instruments (optional, but disciplined)

“Strange” probes (aesthetics predictors, memorability, emotion classifiers) can be useful as axes of variance—precisely because they are culturally saturated and biased. They are admissible only if:

- clearly labeled as probes, not truths,
- versioned and provenance-captured,
- compared against other instruments.

---

## Sources (internal)

- [[A_World_Burning/39-appendix-h-model-cards-and-dependency-registry]]
- [[A_World_Burning/40-appendix-i-known-limitations-and-open-questions]]
- [[A_World_Burning/27-strange-models-compendium]]

---

## Outline (preserved)
**Purpose:** define acceptable ML use, bias management, and what ML cannot be allowed to decide.

- XIII.1 The â€œinstrumentâ€ rule (ML may measure/segment/mediate; may not decide meaning)
- XIII.2 Why single embedding spaces are untrustworthy
  - XIII.2.a ensemble requirement (CLIP + DINO + optional others)
  - XIII.2.b treat disagreement as signal (ambiguity detector)
- XIII.3 Model bias and historical domain mismatch
  - XIII.3.a illustration vs photo bias
  - XIII.3.b Western art-history priors; taxonomy priors; caption bias
- XIII.4 Allowed and forbidden ML tasks
  - Allowed: similarity measurement, salience maps, segmentation confidence, robustness curves
  - Forbidden: â€œspecies identification as truthâ€, narrative authority, automatic restoration claims
- XIII.5 Evaluation and benchmarking (link to Appendix I)
- XIII.6 â€œStrange instrumentsâ€ policy (optional, but documented)
  - see: `A_World_Burning/27-strange-models-compendium.md`

