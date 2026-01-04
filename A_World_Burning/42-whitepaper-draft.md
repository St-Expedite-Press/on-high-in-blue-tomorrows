# The Burning World
## Canonical Digital Editions Under Conditions of Variance
### Working Whitepaper Draft (compiled)

[A_World_Burning/README](README.md) | [A_World_Burning/30-whitepaper-toc](30-whitepaper-toc.md) | [A_World_Burning/26-whitepaper-skeleton](26-whitepaper-skeleton.md) | [whitepaper/White Paper I](../whitepaper/White%20Paper%20I.md)

> [!important] Status + scope
> This file is a **paper-shaped compilation** so the project reads like a single document.
> - Source-of-truth outline (maximal): [A_World_Burning/26-whitepaper-skeleton](26-whitepaper-skeleton.md)
> - Extraction + preprocessing contracts (implementation-facing): [A_World_Burning/00_preprocessing_assay](00_preprocessing_assay.md), [A_World_Burning/33-appendix-b-filesystem-naming-run-ids](33-appendix-b-filesystem-naming-run-ids.md), [A_World_Burning/34-appendix-c-feature-extraction-inventory](34-appendix-c-feature-extraction-inventory.md)
> - Appendices A–J (paper-ready): [A_World_Burning/32-appendix-a-corpus-and-source-registry](32-appendix-a-corpus-and-source-registry.md) through [A_World_Burning/41-appendix-j-glossary](41-appendix-j-glossary.md)

---

## Abstract (draft)

Digital editions of visual works often treat a single image file as a proxy for the work itself, even when the work survives only as a distributed population of variants across print states, conservation histories, and institutional digitizations. This produces a false authority: a “canonical” image whose stability is an artifact of suppressed variance. _The Burning World_ proposes a different canon: not a single file, but a registered, bounded manifold of variants, rendered comparable by strict provenance control and reproducible measurement. Using the Audubon bird-plates as a stress-case corpus, the project enforces a separation between documentation and interpretation: ingestion is provenance-first and source images are immutable; measurement is conducted in sealed, append-only runs that generate auditable artifacts; downstream transformations (including climate-oriented stress regimes) are explicitly labeled and prevented from contaminating the documentary layer. This whitepaper specifies the conceptual commitments, technical architecture, and reproducibility discipline required to build canonical digital editions under conditions of variance.

---

## 1. Introduction

Digital editions of visual works are routinely constructed around a tacit assumption: that there exists a single image capable of standing in for the work as such. This assumption persists even when the historical object survives only as a distributed population of variants—multiple print states, conservation histories, institutional digitizations, color-management pipelines, resolutions, compressions, restorations, and derivative reproductions. In most contemporary workflows, these differences are either ignored, collapsed into an averaged representative, or treated as noise to be minimized. The result is a form of false authority: a canonical image that appears stable precisely because its internal variance has been suppressed.

_The Burning World_ begins from the premise that this suppression is no longer tenable. As digitization accelerates, archives proliferate, and computational systems increasingly rely on visual datasets for analysis, training, and interpretation, the question of what constitutes a “canonical” digital image becomes unavoidable. When similarity itself is operationalized—measured, embedded, clustered, and queried—the notion of a single authoritative image breaks down. What remains is not an image, but a space of variation.

This project proposes a different definition of canon. Here, “canonical” does not mean authoritative, final, or normative. It means formally constrained. A canonical digital edition, in this sense, is not a single file but a registered manifold: a bounded, well-documented space in which all known digital variants of a work are preserved, parameterized, and made comparable. Canonical status is attached not to an instance but to an infrastructure that renders difference legible rather than invisible.

The Audubon bird-plates corpus serves as the primary case study for this approach. The choice is methodological rather than symbolic. Audubon’s plates exist at the intersection of art, natural history, industrial reproduction, and environmental transformation. They have been digitized repeatedly by different institutions under divergent technical regimes, resulting in substantial variation in color, contrast, scale, damage visibility, and framing. This makes the corpus unusually well suited to testing a model of canon that does not rely on stability. Audubon functions here as a stress case: a corpus where suppressing variance produces misleading certainty, and where acknowledging variance forces a rethinking of editorial practice.

Methodologically, _The Burning World_ enforces a strict separation between documentation and interpretation. Ingestion is provenance-first and treats source images as immutable inputs. Feature extraction, embedding, and segmentation are conducted in sealed, reproducible runs that generate append-only artifacts. Interpretive or generative transformations—whether chromatic perturbations, counterfactual environmental stress tests, or hybrid ML workflows—are explicitly downstream and labeled as such. Machine learning is deployed not as an aesthetic engine or oracle of meaning, but as an epistemic instrument for modeling similarity, difference, and instability within a canonical system.

The title _The Burning World_ names the condition under which this work is situated. It refers not only to environmental crisis but to a broader instability affecting archives themselves: material decay, pigment drift, scanning artifacts, compression loss, and institutional divergence. Climate enters the project not as illustration or moral overlay, but as a controlled stress applied to a formally modeled archive. The question is not how images should look under collapse, but how canonical systems behave when stability can no longer be assumed.

---

## 2. Table of Contents (I–XX)

Use the clickable map: [A_World_Burning/30-whitepaper-toc](30-whitepaper-toc.md).

This draft follows the same macro-structure as the skeleton:

- I. Scope, Audience, and Commitments
- II. The Problem of Canon in Digital Visual Culture
- III. Rethinking “Canonical”
- IV. Case Study Selection: The Audubon Plates
- V. Conceptual Architecture of _The Burning World_
- VI. Data Ingestion and Provenance Control
- VII. Feature Extraction and Measurement
- VIII. Segmentation Without Semantics
- IX. Reproducible Runs and Epistemic Discipline
- X. Canon Under Stress: The Climate Frame
- XI. Interpretation Layers (Explicitly Downstream)
- XII. Canonical Query and Analysis
- XIII. Machine Learning as Instrument, Not Oracle
- XIV. Editorial and Scholarly Implications
- XV. Infrastructure and Storage Design
- XVI. Interfaces and Access Layers
- XVII. Failure Modes and Open Problems
- XVIII. Roadmap and Extensions
- XIX. What This Project Refuses
- XX. Conclusion: Canon After Stability

---

## I. Scope, Audience, and Commitments

> [!note] Primary technical references
> [A_World_Burning/26-whitepaper-skeleton](26-whitepaper-skeleton.md) • [A_World_Burning/38-appendix-g-ethical-and-interpretive-guardrails](38-appendix-g-ethical-and-interpretive-guardrails.md) • [A_World_Burning/36-appendix-e-reproducibility-protocols](36-appendix-e-reproducibility-protocols.md)

This whitepaper functions simultaneously as an argument (canon as constraint), a specification (disk/run/ledger contracts), and a reproducible methods guide (sealed runs as lab practice).

Commitments:

- **Provenance-first**: documentary inputs are immutable; provenance is captured before computation.
- **Sealed runs**: computations are append-only events; artifacts are reproducible or failures are documented.
- **No silent semantics**: upstream segmentation/embedding outputs are instruments, not truth claims.
- **Interpretation is downstream**: any transformation that changes pixels or claims meaning is labeled and prevented from contaminating the documentary layer.

This section’s non-claims and guardrails are formalized in [A_World_Burning/38-appendix-g-ethical-and-interpretive-guardrails](38-appendix-g-ethical-and-interpretive-guardrails.md).

---

## II. The Problem of Canon in Digital Visual Culture

Single-image authority is an editorial convenience that becomes a failure mode under variance. When a work survives as a population of variants—across print states, scanning regimes, conservation histories, and institutional pipelines—choosing one image as “the work” hides the editorial decision that produced it.

When similarity becomes operationalized (embedding, clustering, retrieval), these suppressed differences return as visible instability: the “same” plate behaves differently under different digitization conditions. A canonical system must therefore preserve variance rather than erase it, while still providing stable identifiers and comparable measurements.

---

## III. Rethinking “Canonical” (canon as constraint, not authority)

In this project, canon attaches to a formal apparatus:

- bounded corpus definitions,
- stable internal identifiers,
- explicit provenance and integrity checks,
- reproducible runs that generate auditable measurements,
- clear boundaries between documentation and interpretation.

Canonical does not mean final; it means constrained enough that difference can be cited, compared, and audited.

---

## IV. Case Study Selection: The Audubon Plates

Audubon’s plates provide a practical stress test for canon under variance: repeated digitizations across institutions and pipelines yield substantial differences in color, contrast, framing, damage visibility, and compression artifacts. These differences are not noise; they are evidence of the digitization regime and a testbed for comparability.

The bootstrap corpus (one image per plate) is a convenience for building the machinery, not the endpoint. The real target is variance mode: a registered multi-source manifold.

---

## V. Conceptual Architecture of _The Burning World_

> [!note] Primary technical references
> [A_World_Burning/32-appendix-a-corpus-and-source-registry](32-appendix-a-corpus-and-source-registry.md) • [A_World_Burning/33-appendix-b-filesystem-naming-run-ids](33-appendix-b-filesystem-naming-run-ids.md)

Core commitments:

- **Plate-centric identity**: plates are the atomic unit; models never define identity.
- **Variant registration**: each digital file is a variant with explicit provenance and checksums.
- **Measurement before meaning**: features and segments are produced as instruments for difference.
- **Append-only canon**: new runs add artifacts; they do not overwrite prior evidence.

The architectural split is explicit:

- Documentary layer: acquisition + provenance + sealed measurement runs.
- Downstream layer: interpretive and generative transformations (explicitly labeled).

---

## VI. Data Ingestion and Provenance Control (the documentary layer)

> [!note] Primary technical references
> [A_World_Burning/32-appendix-a-corpus-and-source-registry](32-appendix-a-corpus-and-source-registry.md) • [A_World_Burning/33-appendix-b-filesystem-naming-run-ids](33-appendix-b-filesystem-naming-run-ids.md) • [A_World_Burning/28-sources-and-variant-acquisition](28-sources-and-variant-acquisition.md) • [A_World_Burning/00_preprocessing_assay](00_preprocessing_assay.md)

### VI.1 Ontology: plate identity, sources, variants

In _The Burning World_, the plate is the atomic unit of identity. Plate identity is not inferred from model outputs; it is a registry fact:

- `plate_id`: stable internal identifier (`plate-###`).
- `plate_number`: the corpus index (1–435 in bootstrap mode).
- `title` / `slug`: identity fields that support crosswalks and deterministic acquisition.

The ingestion system distinguishes **sources** (provenance containers) from **variants** (specific digital files). A source can contribute one or many variants per plate; a plate can accumulate many variants across sources. The system never collapses these into a single “best” image upstream of measurement; it stores all admitted variants and records why each was admitted.

Canonical corpus boundaries and plate identity fields are specified in [A_World_Burning/32-appendix-a-corpus-and-source-registry](32-appendix-a-corpus-and-source-registry.md).

### VI.2 Bootstrap ingestion (Mode A) vs variance ingestion (Mode B)

Mode A (bootstrap) establishes the minimum canonical apparatus using one canonical source image per plate. It is a convenience for building the machinery, not a conceptual claim that the bootstrap images are authoritative.

Mode B (variance) is the real target: it grows the corpus by adding institutional digitizations and derivative reproductions as registered variants, while preserving plate identity and provenance.

The acquisition discipline and variant registration schema are specified in [A_World_Burning/28-sources-and-variant-acquisition](28-sources-and-variant-acquisition.md).

### VI.3 Immutability, checksums, and “evidence”

Source images are treated as immutable evidence. Nothing overwrites them. Any operation that changes pixels produces a new derived artifact with its own checksums and manifests.

Minimum integrity requirements:

- Cryptographic checksum (SHA-256) recorded at acquisition.
- Access timestamp + acquisition URL recorded for mutable sources.
- Optional fast hash (xxhash64) for recheck scans, never as a substitute for SHA-256.

### VI.4 Disk ontology (how the canon becomes reconstructible)

The project treats file organization as part of the argument: canonical status attaches to the infrastructure that makes variance legible and comparable. The file system is therefore specified as a contract.

Core requirements:

- Plate-local truth is authoritative; global ledgers are derived views and rebuildable.
- Runs are sealed events that emit append-only artifacts with run manifests.
- Stable naming conventions and run IDs make artifacts traceable and auditable.

The full layout, naming law, and run-sealing protocol are specified in [A_World_Burning/33-appendix-b-filesystem-naming-run-ids](33-appendix-b-filesystem-naming-run-ids.md).

---

## VII. Feature Extraction and Measurement (the measurement layer)

> [!note] Primary technical references
> [A_World_Burning/34-appendix-c-feature-extraction-inventory](34-appendix-c-feature-extraction-inventory.md) • [A_World_Burning/29-model-library](29-model-library.md) • [A_World_Burning/39-appendix-h-model-cards-and-dependency-registry](39-appendix-h-model-cards-and-dependency-registry.md) • [A_World_Burning/00_preprocessing_assay](00_preprocessing_assay.md)

Measurement is the layer where computational systems are allowed to speak—but only under constraint. Every computed quantity is the output of a sealed run, and every run is an auditable event with declared inputs/outputs, versions, and checksums.

### VII.1 Feature families (what gets computed)

Feature extraction is intentionally plural: the manifold is measured along multiple axes to avoid any single embedding model becoming an unacknowledged authority.

Core feature families include:

- Pixel and color statistics (global and tiled).
- Perceptual descriptors (edges, gradients, texture, “damage visibility” proxies).
- Whole-image embeddings (multiple backbones).
- Segment and tile embeddings (derived from segmentation outputs).
- Optional text-layer extraction (OCR/layout) and VLM captioning (explicitly labeled).

The exhaustive feature inventory (with storage targets and failure modes) lives in [A_World_Burning/34-appendix-c-feature-extraction-inventory](34-appendix-c-feature-extraction-inventory.md).

### VII.2 Run manifests, artifact sealing, and ledger derivation

Every extraction run records:

- model identifiers + versions (and preferably immutable revision hashes),
- input artifact checksums,
- run configuration (and a config hash),
- output artifact paths + checksums,
- completion state and failure mode if incomplete.

The authoritative artifacts are run outputs and plate-local manifests; aggregated ledgers are rebuildable derivatives.

---

## VIII. Segmentation Without Semantics (structural decomposition)

> [!note] Primary technical references
> [A_World_Burning/35-appendix-d-segmentation-methods-and-parameters](35-appendix-d-segmentation-methods-and-parameters.md) • [A_World_Burning/29-model-library](29-model-library.md) • [A_World_Burning/27-strange-models-compendium](27-strange-models-compendium.md)

Segmentation is used as an instrument for **making variance measurable**, not as a declaration of meaning. The project uses class-agnostic or weakly constrained segmentation to decompose plates into regions so that measurement can be conducted on parts (birds, text blocks, borders, background fields) without prematurely naming them.

### VIII.1 Why “without semantics”

If segmentation outputs are treated as semantic truth, the system quietly imports a model’s training priors as editorial authority. _The Burning World_ refuses that: segmentation yields regions; meaning is a downstream interpretive layer.

### VIII.2 Segmentation outputs (what gets stored)

Segmentation runs may emit:

- Binary masks (raster) for each region.
- Polygonal contours (vector) for each region (optional).
- Region descriptors (area, bbox, centroid, shape stats).
- Region-to-plate mapping records (variant-aware).

All segmentation details—including parameters, tiling strategies, post-processing rules, and explicit non-claims—are specified in [A_World_Burning/35-appendix-d-segmentation-methods-and-parameters](35-appendix-d-segmentation-methods-and-parameters.md).

---

## IX. Reproducible Runs and Epistemic Discipline

> [!note] Primary technical references
> [A_World_Burning/36-appendix-e-reproducibility-protocols](36-appendix-e-reproducibility-protocols.md) • [A_World_Burning/33-appendix-b-filesystem-naming-run-ids](33-appendix-b-filesystem-naming-run-ids.md)

Reproducibility is treated as a methodological discipline rather than an aspirational claim. Runs are sealed; randomness is controlled where possible and logged where not; outputs are append-only; failures are recorded as first-class artifacts.

The key editorial consequence is auditability: a third party must be able to reconstruct what was computed, when, with what inputs, using which model versions and parameters.

---

## X. Canon Under Stress: The Climate Frame

> [!note] Primary technical references
> [A_World_Burning/37-appendix-f-climate-perturbation-regimes](37-appendix-f-climate-perturbation-regimes.md)

The climate layer is not documentary; it is methodological stress. It is defined as a downstream regime of constrained transformations applied to the measured manifold in order to test stability assumptions, model brittleness, and the behavior of canonical systems under controlled instability.

All climate perturbations are parameterized, logged, and explicitly prohibited from being treated as evidence about the historical object.

---

## XI. Interpretation Layers (Explicitly Downstream)

Interpretation begins where the project permits semantic claims, editorial argument, or pixel-transforming operations. These layers are allowed—but only after documentary ingestion and measurement runs are sealed, and only when transformations are labeled and provenance-preserving.

Guardrails and non-claims are defined in [A_World_Burning/38-appendix-g-ethical-and-interpretive-guardrails](38-appendix-g-ethical-and-interpretive-guardrails.md).

---

## XII. Canonical Query and Analysis

Canonical query is the practical payoff of the manifold: similarity search, clustering, outlier detection, and variance analysis across sources and pipelines. The goal is not to select a single “best” image, but to render differences legible and citeable.

This layer depends on the integrity of ingestion, the plurality of instruments, and the sealed-run discipline.

---

## XIII. Machine Learning as Instrument, Not Oracle

Machine learning outputs are admissible only as measured artifacts with documented bias, versioning, and failure modes. No model output is treated as authoritative identity, intent, or truth; it is treated as a constrained measurement that must be compared across instruments and audited against provenance.

Model surface area and licensing constraints are captured in [A_World_Burning/39-appendix-h-model-cards-and-dependency-registry](39-appendix-h-model-cards-and-dependency-registry.md).

---

## XIV. Editorial and Scholarly Implications

This model of canon changes what can be cited: citations point to plate identities, variant identifiers, and run artifacts—not only to an image. It also changes pedagogy and exhibition: interfaces can expose variance as evidence rather than hiding it as noise.

---

## XV. Infrastructure and Storage Design

The storage design is not incidental: it is the mechanism by which canon becomes reconstructible. The system prioritizes immutable evidence, sealed run artifacts, and derived ledgers that can be rebuilt from plate-local truth.

The disk contract and run ID law are specified in [A_World_Burning/33-appendix-b-filesystem-naming-run-ids](33-appendix-b-filesystem-naming-run-ids.md).

---

## XVI. Interfaces and Access Layers

Different audiences will encounter different “projections” of the manifold: archivists may need provenance-first views; ML researchers may need embeddings and indices; editors may need citation-stable variants with apparatus. Each interface is an access layer over the same canonical constraints.

---

## XVII. Failure Modes and Open Problems

> [!note] Primary technical references
> [A_World_Burning/40-appendix-i-known-limitations-and-open-questions](40-appendix-i-known-limitations-and-open-questions.md)

Failure is expected and must be documented. This includes dataset gaps, institutional blind spots, model brittleness, nondeterministic runs, and conceptual risks (e.g., accidental reintroduction of authority via “best-of” defaults).

---

## XVIII. Roadmap and Extensions

The roadmap includes scaling beyond Audubon, adding more institutional sources, improving acquisition workflows (including IIIF), expanding model libraries with pinned revisions, and building interfaces for canonical query.

---

## XIX. What This Project Refuses (non-claims and prohibitions)

This project refuses:

- claims about historical intent derived from model outputs,
- ecological forecasting presented as documentary evidence,
- restoration authority (e.g., “true” colors) upstream of measurement,
- automated canon formation (“the model says this is the canonical image”),
- silent overwrites of evidence.

These refusals are formalized in [A_World_Burning/38-appendix-g-ethical-and-interpretive-guardrails](38-appendix-g-ethical-and-interpretive-guardrails.md).

---

## XX. Conclusion: Canon After Stability

Canonical digital editions under variance require a shift from single-image authority to constrained infrastructure: provenance-first ingestion, reproducible measurement, and auditably bounded transformation regimes. The canon becomes not a file, but a system that makes difference legible.

---

## Appendices (A–J)

These are not optional; they are the paper’s claim to reconstructibility.

- Appendix A: [A_World_Burning/32-appendix-a-corpus-and-source-registry](32-appendix-a-corpus-and-source-registry.md)
- Appendix B: [A_World_Burning/33-appendix-b-filesystem-naming-run-ids](33-appendix-b-filesystem-naming-run-ids.md)
- Appendix C: [A_World_Burning/34-appendix-c-feature-extraction-inventory](34-appendix-c-feature-extraction-inventory.md)
- Appendix D: [A_World_Burning/35-appendix-d-segmentation-methods-and-parameters](35-appendix-d-segmentation-methods-and-parameters.md)
- Appendix E: [A_World_Burning/36-appendix-e-reproducibility-protocols](36-appendix-e-reproducibility-protocols.md)
- Appendix F: [A_World_Burning/37-appendix-f-climate-perturbation-regimes](37-appendix-f-climate-perturbation-regimes.md)
- Appendix G: [A_World_Burning/38-appendix-g-ethical-and-interpretive-guardrails](38-appendix-g-ethical-and-interpretive-guardrails.md)
- Appendix H: [A_World_Burning/39-appendix-h-model-cards-and-dependency-registry](39-appendix-h-model-cards-and-dependency-registry.md)
- Appendix I: [A_World_Burning/40-appendix-i-known-limitations-and-open-questions](40-appendix-i-known-limitations-and-open-questions.md)
- Appendix J: [A_World_Burning/41-appendix-j-glossary](41-appendix-j-glossary.md)
