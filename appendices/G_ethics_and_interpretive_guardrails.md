# Appendix G: Ethical and Interpretive Guardrails (Formal Refusals)

[[A_World_Burning/README]] | [[A_World_Burning/30-whitepaper-toc]] | [[A_World_Burning/26-whitepaper-skeleton]]

This appendix is a set of explicit refusals and boundary conditions. It exists to keep the project legible to archivists, editors, and technical reviewers, and to prevent the canonical apparatus from being misread as a claim to authority.

Core idea:

> _The Burning World_ does not produce “the correct image.” It produces an infrastructure in which variance can be preserved, measured, and cited without being erased.

Related:

- Whitepaper master outline: `26-whitepaper-skeleton.md`
- Sources/variants discipline: `28-sources-and-variant-acquisition.md`
- Run/ledger discipline: `33-appendix-b-filesystem-naming-run-ids.md`

---

## G.1 Non-claims (what this project refuses to assert)

The project refuses to claim:

- the original, authoritative appearance of a plate
- the artist’s intent as recoverable from model outputs
- that any digitization pipeline is “more correct” in an absolute sense
- that similarity equals identity (especially across institutional variants)
- that model outputs are evidence of historical fact

---

## G.2 No restorative authority

Even if restoration-like operations are performed downstream (cleaning, recoloring, damage removal), the project refuses to treat them as:

- corrections
- reconstructions
- recoveries of “true color”

If restoration-style transforms are produced, they are labeled as:

- downstream
- parameterized
- reversible (in the sense that the original evidence remains intact)

---

## G.3 Machine learning is instrumentation, not oracle

ML models are treated as instruments with priors:

- biased training distributions
- sensitivity to digitization pipelines
- cultural saturation (especially for “aesthetic” or “emotion” probes)

Policy:

- store model disagreements
- do not convert model outputs into truth labels
- do not use a single embedding space as the edition’s “canonical geometry”

---

## G.4 Weak-label policy (captions/tags are never ground truth)

Captions, tags, and VLM outputs are:

- weak signals used for browsing, retrieval, and exploratory analysis
- never used to overwrite identity metadata or provenance fields

Operational constraint:

- prompts and decoding parameters must be versioned and stored (see `00_preprocessing_assay_addendum.md`)

---

## G.5 Institutional respect (licensing, credit, provenance)

The project commits to:

- preserving institutional credit lines
- recording licenses and terms of use where known
- treating sources as mutable unless proven immutable (drift checks)
- not redistributing content in violation of terms

Appendix A records the bootstrap source/terms for the initial Audubon corpus:

- `32-appendix-a-corpus-and-source-registry.md`

---

## G.6 No biometric identity systems (global rule)

Even though the Audubon corpus is not a human-subject dataset, the project adopts a general guardrail:

- do not build, export, or publish biometric identity systems
- do not create face embeddings intended for identification

If any face-like detection is used in other corpora, it is constrained to local technical tasks (blur, dedup) and remains strictly downstream.

---

## G.7 Environmental framing (no ecological forecasting)

The project’s “climate stress” framing is methodological, not predictive:

- no claims about future climate conditions
- no claim that a particular perturbation corresponds to a real ecological event
- no claim that transformations represent “what will happen”

Appendix F exists to keep this precise:

- `37-appendix-f-climate-perturbation-regimes.md`

---

## G.8 Security and operational hygiene

Project survivability is an ethical constraint.

- no secrets checked into repos
- `.env` files treated as compromised if shared
- credentials rotated when risk is detected

See the explicit note in:

- `00_preprocessing_assay_addendum.md`

---

## G.9 Citation discipline (no ambiguous references)

When citing:

- a source variant: cite source registry ID + checksum + access date
- a derived measurement: cite run_id + config hash + model IDs + ledger version
- a transformation: cite transform run_id + parameter set + safeguard metrics

This is not bureaucratic; it is the mechanism by which the project prevents false authority.
