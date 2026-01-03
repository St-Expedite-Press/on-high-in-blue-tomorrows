<!-- Auto-generated TOC-aligned file. Source of truth: A_World_Burning/26-whitepaper-skeleton.md -->

# VII. Feature Extraction and Measurement (the measurement layer)

[[whitepaper/DRAFT]] | [[whitepaper/MATERIALS_MAP]] | [[A_World_Burning/00_preprocessing_assay]] | [[A_World_Burning/34-appendix-c-feature-extraction-inventory]]

_TOC-aligned entrypoint. Master outline lives in `A_World_Burning/26-whitepaper-skeleton.md`._

---

## Draft (body text)

This section defines the measurement layer: what the system computes, why those computations are admissible as documentary instrumentation, and how outputs are stored so they remain comparable across variants and over time.

The key editorial rule is simple: **measurement is allowed to multiply the archive, not overwrite it**. Every extraction is a sealed run that emits append-only artifacts.

### VII.1 Progressive revelation (cheap certainty → expensive meaning)

Extraction should proceed in tiers:

1. **Cheap certainty**: container/header facts, integrity checks, and scalar pixel passes that are fast to recompute and hard to dispute.
2. **Structural decomposition**: segmentation/region proposals that make local measurement possible.
3. **Instrument ensembles**: multiple embedding families/probes so no single model becomes an invisible authority.
4. **Optional weak semantics**: OCR, captioning, and tagging only when explicitly labeled as downstream instrumentation.

This tiering is operationally useful (cost control) and epistemically useful (it prevents premature semantic collapse).

### VII.2 CPU/GPU boundaries are epistemic

The CPU/GPU split is not only a budget decision; it is a boundary between:

- deterministic, easily auditable computation (CPU extraction, schema validation, hashing), and
- heavier inference that is often less deterministic and more version-sensitive (GPU embeddings, segmentation).

Treat GPU runs as higher-risk evidence: capture more provenance (model revision, environment, config hashes) and expect more drift.

### VII.3 Baseline facts vs representations

The project distinguishes:

- **facts**: container/header properties; scalar pixel statistics; checksums; run manifests.
- **representations**: downsampled working images, previews, tiled crops, masks, embeddings, indices.

Representations are valuable and often necessary, but they must remain traceable back to immutable inputs.

### VII.4 Feature families (plural instrumentation)

The measured manifold should include multiple feature families, including:

- file/container fingerprints (ICC presence, compression signatures),
- global and tiled pixel statistics (color, contrast, entropy),
- classical CV descriptors (edges, gradients, texture),
- multiple embedding backbones (e.g., CLIP-family and self-supervised ViTs),
- segmentation-derived region descriptors and region embeddings,
- optional OCR/layout and captioning (if used, versioned and labeled),
- dataset-level structures (ANN indices, cluster assignments, outlier sets) as derived, versioned artifacts.

The exhaustive inventory remains in the appendices; this section explains why those families exist and how they are disciplined.

### VII.5 Stop conditions (when measurement is “enough”)

The system should define stop conditions as policies, not vibes. Examples:

- clusters stabilize across multiple embedding families (instrument agreement);
- new feature passes stop changing outlier sets materially;
- additional captioning/weak labels stop introducing new axes (only redundancy).

Stop conditions are recorded explicitly as part of a run policy so future readers know what was chosen not to compute.

---

## Sources (internal)

- [[A_World_Burning/00_preprocessing_assay]]
- [[A_World_Burning/34-appendix-c-feature-extraction-inventory]]
- [[A_World_Burning/29-model-library]]
- [[abstract_photo_workflows/01_general_photo_set_prompt]]

---

## Outline (preserved)
**Purpose:** define what is extracted, why, and how it is stored so it remains comparable.

This section must explicitly align with `A_World_Burning/00_preprocessing_assay.md`.

- VII.1 Extraction philosophy: progressive revelation (cheap certainty â†’ expensive meaning)
- VII.2 CPU/GPU boundaries and why they matter (cost is epistemic, not just monetary)
- VII.3 Baseline â€œfactsâ€ vs â€œrepresentationsâ€
  - VII.3.a Header/container facts (no pixel math)
  - VII.3.b Scalar pixel-pass facts (one pass; no distributions)
  - VII.3.c Distribution summaries (sampled/tiled; optional)
- VII.4 Full feature inventory (mirrors Appendix C)
  - VII.4.a File/container features
  - VII.4.b Global pixel stats
  - VII.4.c Classical CV descriptors
  - VII.4.d Embedding families (global/multi-crop/patch)
  - VII.4.e Forensics/provenance cues
  - VII.4.f Quality/aesthetic scores
  - VII.4.g OCR/text/layout (if included)
  - VII.4.h Dataset-level relational structures (ANN, clustering, outliers)
- VII.5 Output artifacts and schemas
  - VII.5.a Per-plate derived JSONs (what exists and why)
  - VII.5.b Global Parquet ledgers (what columns exist and why)
  - VII.5.c Index artifacts (FAISS/ScaNN) and their versioning
- VII.6 Known failure modes and mitigations
  - VII.6.a Very large images (decompression-bomb thresholds, tiling strategy)
  - VII.6.b Drive performance constraints (many small writes)
  - VII.6.c Nondeterminism in GPU inference (document and bound)
- VII.7 Stop conditions (when measurement is â€œenoughâ€)
  - VII.7.a Stop extracting when new passes stop changing cluster topology
  - VII.7.b Stop when clusters stabilize across multiple embedding families (CLIP vs DINO vs others)
  - VII.7.c Stop when outliers remain outliers regardless of extractor (they become part of the atlas)
  - VII.7.d Stop when additional captioning/weak labels stop introducing new axes (only redundancy)
  - VII.7.e Record the stop decision as a documented policy (with evidence)
- VII.8 Publication packaging of the measured corpus (still â€œpreprocessingâ€)
  - VII.8.a Dataset card contents (what is included/excluded; licensing; known biases)
  - VII.8.b Distribution formats (choose and document)
    - plate-centric folders as primary truth
    - Parquet/Arrow bundles for facts/vectors
    - optional WebDataset shards for large-scale ML consumption
    - optional IIIF manifests for institutional viewing
  - VII.8.c Checksummed release artifacts (release manifest + hashes)

