# Appendix J: Glossary of Terms (Enforced Internal Consistency)

[[A_World_Burning/README]] | [[A_World_Burning/30-whitepaper-toc]] | [[A_World_Burning/26-whitepaper-skeleton]]

This glossary defines loaded and technical terms as used in _The Burning World_. It exists to prevent incompatible interpretations from silently entering the document.

---

## Terms

### apparatus

In a critical edition sense: the documented infrastructure that makes variance legible (sources, variants, constraints, provenance, measurement runs). In this project, the apparatus is primary.

### artifact

Any file written by the project (manifests, masks, vectors, embeddings, figures). Artifacts are evidence when they are provenance-linked; otherwise they are just files.

### bootstrap mode

The initial operational mode: one canonical source image per plate (435 plates total). Variance is not yet expanded across institutions.

### canon / canonical

Not “authoritative” or “best.” Here, canonical means **formally constrained**: a bounded, documented space in which known variants are preserved and made comparable.

### canonical digital edition

Not a single image file, but a registered manifold: identity constraints + provenance constraints + process constraints + representation constraints.

### config / configuration

The complete parameterization of a run (model IDs, preprocessing policy, batching policy, seeds). Config is hashed; changing it implies a new run.

### derived

Any output computed from an input (source or other derived artifact). Derived artifacts are not evidence of historical truth; they are evidence of what a run produced.

### drift

Change in bytes or measurements over time. Can be upstream (source bytes replaced) or downstream (model/library/version changes causing measurement differences).

### embedding

A numeric vector representation of an image, segment, tile, or text. Embeddings are instruments; they encode priors. They are never identity.

### evidence tag

One of `[MEASURED]`, `[DERIVED]`, `[INTERPRETIVE]`, `[SPECULATIVE / FUTURE WORK]`. Used to prevent prose from contaminating measurement claims.

### feature

Any computed measurement (scalar, vector, map) extracted from an image or its derived representations (including masks and text).

### immutable (source)

Source image bytes are treated as immutable evidence once ingested. Upstream changes mint new variants; nothing overwrites.

### ingestion

The act of acquiring sources, preserving provenance, computing checksums, writing manifests, and creating canonical structure on disk.

### instrument

A model or algorithm treated as a measurement device. Instruments have versions, priors, and failure modes. Agreement/disagreement across instruments is part of the analysis.

### ledger

A derived, rebuildable Parquet table that indexes plate-local truth and run outputs. Ledgers are disposable views, not primary truth.

### manifold

The bounded space of registered variants and derived measurements that makes “canon under variance” operational.

### mask

A segmentation artifact identifying a region of pixels. Masks can be class-agnostic (preferred first) or semantic (optional, weak channel).

### measurement layer

The preprocessing regime of feature extraction (scalars, embeddings, segmentation) conducted in sealed runs. This layer must remain separated from interpretation and transformation.

### plate

The atomic unit in this project: `plate-001` … `plate-435`. A plate is an identity record, not a single file.

### plate_id

The stable internal identifier for a plate (`plate-###`, zero-padded).

### provenance

The chain of evidence linking any artifact to:

- source/variant identity (checksums)
- run identity (run_id, config hash)
- model identity (model_id, pinned revision)

### prompt registry

A versioned registry of prompts used for captioning/tagging/probes. Without it, text outputs become irreproducible prose drift.

### run

A sealed, append-only computational event that emits artifacts and a run manifest. Runs are never edited; corrections are new runs.

### run_id

A collision-resistant identifier for a run, typically hybrid timestamp + short hash. Run IDs are part of file naming law.

### sealed

A run is sealed when:

- all declared outputs exist
- checksums are recorded
- manifest status is `complete` or `failed`

### segmentation without semantics

The preferred segmentation regime: masks are treated as structural decomposition, not as meaning assignment.

### source

An upstream repository, institutional holding, or URL from which a variant is acquired.

### stress (climate stress)

Downstream, parameterized perturbations applied to images to test stability and drift under controlled change. Stress is not historical truth.

### transformation

Any downstream operation that changes pixels beyond the documentation layer. Transformations are explicitly labeled and cannot contaminate the canonical measurement layer.

### variant

One immutable digitization (one set of bytes) associated with a plate identity. Variants can come from different institutions or pipelines.

### variance mode

The operational mode where multiple variants per plate are ingested and registered, preserved without collapse, and made comparable.
