# The Burning World
## Canonical Digital Editions Under Conditions of Variance
### Whitepaper Skeleton (Exhaustive)

[[A_World_Burning/README]] | [[A_World_Burning/30-whitepaper-toc]] | [[whitepaper/White Paper I]]

**Compiled reading draft (Obsidian-friendly):** [[A_World_Burning/42-whitepaper-draft]]

**Document status:** draft skeleton (argument + specification + infrastructure guide)  
**Scope:** conceptual framework + technical architecture through canonicalization, extraction, and reproducible measurement; transformations are explicitly downstream.  
**Companion materials (living, implementation-facing):**  
- `A_World_Burning/00_preprocessing_assay.md` (exhaustive extraction inventory)  
- `A_World_Burning/00_preprocessing_assay_addendum.md` (no-edit addenda surfaced during whitepaper pass)  
- `A_World_Burning/28-sources-and-variant-acquisition.md` (source discovery/acquisition discipline; variant registry)  
- `A_World_Burning/27-strange-models-compendium.md` (unusual embeddings/probes as instruments; candidate models)
- `A_World_Burning/31-sources-and-instruments-bibliography.md` (working links list for sources + model instruments)
- `A_World_Burning/29-model-library.md` (embedding/segmentation library; alias hygiene; pinning protocol)
- `A_World_Burning/32-appendix-a-corpus-and-source-registry.md` (filled Appendix A)
- `A_World_Burning/33-appendix-b-filesystem-naming-run-ids.md` (filled Appendix B)
- `A_World_Burning/34-appendix-c-feature-extraction-inventory.md` (filled Appendix C)

---

## 0. How To Use This Document (meta)

This file is a **maximally documented outline**. It is designed so a third party can:

- Understand the conceptual claim (canon as constraint/manifold, not a single image)
- Implement the pipeline without oral tradition
- Audit provenance and reproduce measurements
- Distinguish “documentation” from “interpretation” at every boundary

Authoring rule: **every subsection must end with one evidence tag** (or equivalent):

- **[MEASURED]** (directly from stored artifacts/ledgers)
- **[DERIVED]** (computed from measured fields; formula stated)
- **[INTERPRETIVE]** (argumentative / humanities framing)
- **[SPECULATIVE / FUTURE WORK]**

This rule is adapted from the internal research prompt discipline in `A_World_Burning/19-the-big-one.md` and should be treated as a non-negotiable editorial constraint for the whitepaper.

---

## 1. Abstract / Executive Summary (write last)

### 1.1 One-paragraph abstract (required)

- Problem statement: single-image “canon” collapses under variance
- Proposed solution: canonical digital editions as **registered manifolds**
- Case study: Audubon plates as a stress case for variance
- Method: provenance-first ingestion, sealed runs, append-only artifacts, measurement-before-interpretation
- Outputs: filesystem contract, ledgers, embeddings/segments, queryable atlas, downstream stress/transform regime definitions

### 1.2 Bullet summary of claims (required)

- Claim A: single-image authority is a false stability mechanism in visual editions
- Claim B: “canonical” can be redefined as **constraint + comparability infrastructure**
- Claim C: variance can be preserved without interpretive collapse via strict run/ledger discipline
- Claim D: ML is admissible only as instrumentation; outputs are versioned, bounded, and never authoritative identity records

### 1.3 Audience matrix (required)

- Archivists / collections: provenance, preservation, citation, governance
- Digital humanists / editors: critical editions, apparatus, variance as evidence
- CV/ML researchers: embeddings, segmentation, benchmarks, reproducibility
- Infrastructure engineers: storage, schemas, indices, determinism, failures

---

## 2. Introduction (draft provided; refine for the whitepaper)

Digital editions of visual works are routinely constructed around a tacit assumption: that there exists a single image capable of standing in for the work as such. This assumption persists even when the historical object survives only as a distributed population of variants—multiple print states, conservation histories, institutional digitizations, color-management pipelines, resolutions, compressions, restorations, and derivative reproductions. In most contemporary workflows, these differences are either ignored, collapsed into an averaged representative, or treated as noise to be minimized. The result is a form of false authority: a canonical image that appears stable precisely because its internal variance has been suppressed.

_The Burning World_ begins from the premise that this suppression is no longer tenable. As digitization accelerates, archives proliferate, and computational systems increasingly rely on visual datasets for analysis, training, and interpretation, the question of what constitutes a “canonical” digital image becomes unavoidable. When similarity itself is operationalized—measured, embedded, clustered, and queried—the notion of a single authoritative image breaks down. What remains is not an image, but a space of variation.

This project proposes a different definition of canon. Here, “canonical” does not mean authoritative, final, or normative. It means formally constrained. A canonical digital edition, in this sense, is not a single file but a registered manifold: a bounded, well-documented space in which all known digital variants of a work are preserved, parameterized, and made comparable. Canonical status is attached not to an instance but to an infrastructure that renders difference legible rather than invisible.

The Audubon bird-plates corpus serves as the primary case study for this approach. The choice is methodological rather than symbolic. Audubon’s plates exist at the intersection of art, natural history, industrial reproduction, and environmental transformation. They have been digitized repeatedly by different institutions under divergent technical regimes, resulting in substantial variation in color, contrast, scale, damage visibility, and framing. This makes the corpus unusually well suited to testing a model of canon that does not rely on stability. Audubon functions here as a stress case: a corpus where suppressing variance produces misleading certainty, and where acknowledging variance forces a rethinking of editorial practice.

Methodologically, _The Burning World_ enforces a strict separation between documentation and interpretation. Ingestion is provenance-first and treats source images as immutable inputs. Feature extraction, embedding, and segmentation are conducted in sealed, reproducible runs that generate append-only artifacts. Interpretive or generative transformations—whether chromatic perturbations, counterfactual environmental stress tests, or hybrid ML workflows—are explicitly downstream and labeled as such. Machine learning is deployed not as an aesthetic engine or oracle of meaning, but as an epistemic instrument for modeling similarity, difference, and instability within a canonical system.

The title _The Burning World_ names the condition under which this work is situated. It refers not only to environmental crisis but to a broader instability affecting archives themselves: material decay, pigment drift, scanning artifacts, compression loss, and institutional divergence. Climate enters the project not as illustration or moral overlay, but as a controlled stress applied to a formally modeled archive. The question is not how images should look under collapse, but how canonical systems behave when stability can no longer be assumed.

This whitepaper lays out the conceptual framework, technical architecture, methodological discipline, and future extensions of _The Burning World_. It is intended to function simultaneously as an argument, a specification, and an infrastructural guide. Its audience includes digital humanists, computer vision researchers, archivists, editors, and technologists interested in building digital editions that do not erase variance in the name of authority.

---

## 3. Table of Contents (expanded; include substructure)

This ToC preserves your section headings, but expands them into an “executable outline”.

### I. Scope, Audience, and Commitments

**Purpose:** define the boundaries of what this whitepaper asserts, how it will be evaluated, and what it refuses.

- I.1 Intended audiences and what each needs
- I.2 Definitions (canon, edition, variant, manifold, run, ledger, provenance)
- I.3 Evidence taxonomy and the “no untagged claims” rule
- I.4 Epistemic separation doctrine: documentation vs interpretation vs transformation
- I.5 Ethics and guardrails (privacy/biometrics, institutional authority, restoration claims, environmental claims)
- I.6 Commitments to reproducibility (determinism where possible, logged nondeterminism where not)
- I.7 Commitments to long-term preservation (formats, checksums, rebuildability)
- I.8 Threat model / operational hygiene (secrets, accidental contamination, drift)

### II. The Problem of Canon in Digital Visual Culture

**Purpose:** show why “single-image canon” became default and why it fails under variance.

- II.1 The tacit single-file assumption as editorial inheritance
- II.2 Varieties of variance (enumerate)
  - II.2.a Print states and production differences
  - II.2.b Conservation histories and material changes
  - II.2.c Institutional digitization divergence (equipment + lighting + profiles)
  - II.2.d Computational postprocessing divergence (color management, sharpening, denoise)
  - II.2.e Resolution, framing, cropping, rotation, page borders
  - II.2.f Compression regimes, container rewrites, downsampling artifacts
  - II.2.g Restoration and derivative reproductions (with/without disclosure)
- II.3 Consequences of suppression
  - II.3.a False authority and the invisibility of editorial choice
  - II.3.b Dataset contamination and model behavior (training leakage, bias)
  - II.3.c Scholarly citation ambiguity (what exact image was referenced?)
  - II.3.d Conservator blind spots (damage visibility depends on pipeline)
- II.4 Prior art / parallels (textual criticism, critical editions, stemmatics, apparatus)

### III. Rethinking “Canonical”

**Purpose:** define canon as constraint + infrastructure rather than authority.

- III.1 Canonical ≠ normative: canon as bounded space, not final image
- III.2 Canonical digital edition as a registered manifold
  - III.2.a What counts as a “variant” (definition + minimum metadata)
  - III.2.b What counts as “registered” (constraints + documentation)
  - III.2.c Parameterization: axes not knobs (link to parameter discipline)
- III.3 Canonical constraints
  - III.3.a Identity constraints (stable IDs; non-negotiable mapping)
  - III.3.b Provenance constraints (checksums + source registry)
  - III.3.c Process constraints (sealed runs; append-only; validators)
  - III.3.d Representation constraints (storage doctrine: artifacts/facts/perception/meaning)
- III.4 Editorial consequences: the apparatus becomes primary
  - III.4.a Citation becomes a path in the manifold (plate_id + variant_id/run_id)
  - III.4.b “Best image” becomes a query result, not an editorial decree

### IV. Case Study Selection: The Audubon Plates

**Purpose:** justify Audubon as methodological stress case.

- IV.1 Corpus summary (what it is, size, plate count, known metadata)
- IV.2 Why Audubon is a “variance amplifier”
  - IV.2.a Industrial reproduction + illustration domain
  - IV.2.b Repeated digitizations across institutions
  - IV.2.c Page borders, inscriptions, paper tone, foxing, staining
- IV.3 Why Audubon is not treated as symbol (guard against over-reading)
- IV.4 Corpus boundary conditions (what counts as “in scope” for Audubon)
  - IV.4.a Plate count is fixed (1–435)
  - IV.4.b Variant sources allowed (multiple holdings) vs current single-source bootstrap

### V. Conceptual Architecture of The Burning World

**Purpose:** name the project’s ontology and state transitions.

- V.1 Plate-centric identity (plate is atomic unit)
- V.2 Variant registration (variants attach to plates)
- V.3 Run as epistemic event (sealed, append-only, auditable)
- V.4 Ledger as derived view (fast, disposable; never authoritative)
- V.5 Stability vs controlled instability
  - V.5.a “Stability” = reproducible measurement pipeline
  - V.5.b “Instability” = downstream stress tests/transformations, explicitly labeled
- V.6 The archive tolerates violence: why provenance-first enables aggressive downstream work

### VI. Data Ingestion and Provenance Control

**Purpose:** define how images enter, how they are frozen, and how they remain trustworthy.

- VI.1 Acquisition pathways (download, institutional pulls, existing repositories)
- VI.2 Source registry requirements (Appendix A)
  - VI.2.a Source URL / institution / holding record
  - VI.2.b Acquisition timestamp and operator
  - VI.2.c License/credit record + restrictions
- VI.3 Integrity verification
  - VI.3.a Cryptographic checksums (sha256; optional xxhash)
  - VI.3.b Dedup detection (exact + near-duplicate signals)
  - VI.3.c File/container fingerprints (quant tables, ICC presence, progressive/baseline)
- VI.4 Immutability rules
  - VI.4.a Source images never overwritten
  - VI.4.b Corrections occur only as new variants or new runs
- VI.5 Drift detection (re-validate manifest/schema/checksum)
- VI.6 Variant acquisition discipline (explicit protocol)
  - see: `A_World_Burning/28-sources-and-variant-acquisition.md`

### VII. Feature Extraction and Measurement (the measurement layer)

**Purpose:** define what is extracted, why, and how it is stored so it remains comparable.

This section must explicitly align with `A_World_Burning/00_preprocessing_assay.md`.

- VII.1 Extraction philosophy: progressive revelation (cheap certainty → expensive meaning)
- VII.2 CPU/GPU boundaries and why they matter (cost is epistemic, not just monetary)
- VII.3 Baseline “facts” vs “representations”
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
- VII.7 Stop conditions (when measurement is “enough”)
  - VII.7.a Stop extracting when new passes stop changing cluster topology
  - VII.7.b Stop when clusters stabilize across multiple embedding families (CLIP vs DINO vs others)
  - VII.7.c Stop when outliers remain outliers regardless of extractor (they become part of the atlas)
  - VII.7.d Stop when additional captioning/weak labels stop introducing new axes (only redundancy)
  - VII.7.e Record the stop decision as a documented policy (with evidence)
- VII.8 Publication packaging of the measured corpus (still “preprocessing”)
  - VII.8.a Dataset card contents (what is included/excluded; licensing; known biases)
  - VII.8.b Distribution formats (choose and document)
    - plate-centric folders as primary truth
    - Parquet/Arrow bundles for facts/vectors
    - optional WebDataset shards for large-scale ML consumption
    - optional IIIF manifests for institutional viewing
  - VII.8.c Checksummed release artifacts (release manifest + hashes)

### VIII. Segmentation Without Semantics

**Purpose:** extract structure without prematurely asserting meaning.

- VIII.1 Why class-agnostic masks (SAM-style) are methodologically aligned
- VIII.2 What segmentation is allowed to claim (and what it is not)
- VIII.3 Segmentation stacks considered
  - VIII.3.a SAM (vit-h primary; vit-l/vit-b fallback)
  - VIII.3.b Mask2Former (when semantic classes are required)
  - VIII.3.c Optional detection support (DETR, GroundingDINO) as scaffolding signals
- VIII.4 Mask representation choices
  - VIII.4.a PNG masks (inspectability)
  - VIII.4.b RLE JSON (compactness; ledger-friendly)
  - VIII.4.c Polygonization (vector regime; COCO polygons)
- VIII.5 Mask QC metrics
  - VIII.5.a segment count distribution
  - VIII.5.b fragmentation/stability measures
  - VIII.5.c largest-segment dominance ratio
  - VIII.5.d boundary uncertainty / “ambiguous zones”
- VIII.6 Segment-level measurement (stats and embeddings per mask)
- VIII.7 Storage: per-run artifacts + `segments.parquet`

### IX. Reproducible Runs and Epistemic Discipline

**Purpose:** make the system auditable; define what “a run” is and how it is sealed.

- IX.1 Run ontology
  - IX.1.a Run = sealed event; never edited; never merged
  - IX.1.b Runs are append-only; corrections are new runs
- IX.2 Run identifiers (choose and freeze)
  - IX.2.a sequential
  - IX.2.b hash-based
  - IX.2.c timestamp + short hash (recommended hybrid)
- IX.3 Run manifest schema (Appendix B)
  - IX.3.a required fields (run_id, plate_id, timestamp, models, outputs)
  - IX.3.b config hash, code version, environment capture
  - IX.3.c input list + checksums; output list + checksums
- IX.4 Validators (failure intolerant)
  - IX.4.a filesystem invariant validation (pre-run)
  - IX.4.b schema validation (pre-run)
  - IX.4.c post-run validation (all outputs registered + exist)
- IX.5 Notebook discipline (Appendix E)
  - IX.5.a CPU notebook rules
  - IX.5.b GPU notebook rules
  - IX.5.c forbidden anti-patterns (silent failures, unregistered writes, implicit state)
- IX.6 Ledgers: derived, rebuildable, disposable
  - IX.6.a ledger rebuild protocol
  - IX.6.b “ledger disagreeing with plate truth” resolution rule
  - IX.6.c Dual-ledger principle (must be explicit)
    - plate-local verbose artifacts = authoritative provenance (“truth”)
    - global ledgers = speed layer (append-only; rebuildable; disposable)
    - if plate-local and ledger disagree, the ledger is wrong

### X. Canon Under Stress: The Climate Frame

**Purpose:** define “stress” as a controlled methodological pressure, not a claim about reality.

- X.1 Climate as frame vs climate as illustration
- X.2 “Archive instability” as broader than climate (pigment drift, scanning, compression, institutional divergence)
- X.3 Stress testing as measurement
  - X.3.a perturbation axes (temperature shift, haze/ash occlusion, nocturne artifacts, contrast collapse)
  - X.3.b parameter discipline: axes, not knobs (link to Appendix F)
  - X.3.c safeguard constraints (do-not-cross thresholds)
- X.4 What is explicitly forbidden in stress transforms (no new anatomy, no restorative claims)

### XI. Interpretation Layers (Explicitly Downstream)

**Purpose:** enforce a quarantine boundary between measured documentation and downstream transforms.

- XI.1 Layer separation doctrine
  - XI.1.a Documentation layer (ingest + measurement)
  - XI.1.b Interpretation layer (analysis, clustering, narrative hypotheses)
  - XI.1.c Transformation layer (counterfactual renderings, LoRA, diffusion)
- XI.2 Labeling and provenance rules for downstream artifacts
  - XI.2.a transform manifests
  - XI.2.b parameter logs + run IDs
  - XI.2.c “no overwrites” enforced
- XI.3 “Contamination” definition and prevention
  - XI.3.a never allow transformed outputs to replace source or baseline ledgers
  - XI.3.b never treat VLM captions as truth labels

### XII. Canonical Query and Analysis

**Purpose:** show what becomes possible once variance is registered.

- XII.1 Similarity search modes
  - XII.1.a image → image retrieval (global embeddings)
  - XII.1.b segment/motif retrieval (segment embeddings)
  - XII.1.c tile-wise retrieval (“thing somewhere in image”)
  - XII.1.d multimodal retrieval (text → image; caption embeddings)
- XII.2 Clustering and multi-resolution maps
  - XII.2.a hierarchical clustering (coarse→fine)
  - XII.2.b outlier mining and “rare mode” discovery
  - XII.2.c near-duplicate and lineage graphs
- XII.3 Dataset atlas deliverables (figures + dashboards)
- XII.4 Query outputs as citations (how to cite a result reproducibly)

### XIII. Machine Learning as Instrument, Not Oracle

**Purpose:** define acceptable ML use, bias management, and what ML cannot be allowed to decide.

- XIII.1 The “instrument” rule (ML may measure/segment/mediate; may not decide meaning)
- XIII.2 Why single embedding spaces are untrustworthy
  - XIII.2.a ensemble requirement (CLIP + DINO + optional others)
  - XIII.2.b treat disagreement as signal (ambiguity detector)
- XIII.3 Model bias and historical domain mismatch
  - XIII.3.a illustration vs photo bias
  - XIII.3.b Western art-history priors; taxonomy priors; caption bias
- XIII.4 Allowed and forbidden ML tasks
  - Allowed: similarity measurement, salience maps, segmentation confidence, robustness curves
  - Forbidden: “species identification as truth”, narrative authority, automatic restoration claims
- XIII.5 Evaluation and benchmarking (link to Appendix I)
- XIII.6 “Strange instruments” policy (optional, but documented)
  - see: `A_World_Burning/27-strange-models-compendium.md`

### XIV. Editorial and Scholarly Implications

**Purpose:** explain what changes for scholarship when the “work” is a manifold.

- XIV.1 Citation: from single images to variant paths
  - XIV.1.a citing plate_id + source_id + checksum
  - XIV.1.b citing run_id + config hash for derived measurements
- XIV.2 Teaching and publication: how to present variance without losing legibility
- XIV.3 Museums and libraries: governance of canonical constraints, not “best images”
- XIV.4 Conservation workflows: “canonical does not mean pristine”

### XV. Infrastructure and Storage Design

**Purpose:** specify the storage doctrine and the concrete artifact graph.

- XV.1 Storage doctrine (must be repeated verbatim in the final whitepaper)
  - Files hold artifacts
  - Parquet holds facts
  - Vectors hold perception
  - Graphs hold meaning
- XV.2 Filesystem contract (Appendix B)
- XV.3 Tabular schemas (Appendix C + Appendix H)
- XV.4 Vector storage + compression (float16, PQ) and index versioning
- XV.5 Optional graph layer (Neptune) as derived meaning space
  - XV.5.a nodes/edges ontology
  - XV.5.b “reverse resolution to disk” requirement
  - XV.5.c graph is derived truth, not primary truth
  - XV.5.d supported graph modes (document which is used)
    - property graph (Gremlin traversal)
    - RDF/OWL (SPARQL queries; ontology reasoning)
  - XV.5.e ontology artifacts (if used)
    - `core.ttl`
    - `audubon.ttl`
    - `burning_world.ttl`
    - `provenance.ttl`
  - XV.5.f bulk ingestion artifacts (if used)
    - nodes/edges tables (CSV/Parquet) with `source_file_path`, `run_id`, `plate_id`, checksum
    - load properties and mapping
  - XV.5.g ingest rejection rules (museum-grade)
    - any node/edge that cannot be reverse-resolved to disk rejects the load
    - any checksum mismatch rejects the load
  - XV.5.h ingest tables vs live DB dependency (prefer tables; DB is optional)
- XV.6 Long-term preservation strategy
  - XV.6.a format choices (Parquet/JSON/PNG/SVG)
  - XV.6.b checksums and periodic revalidation
  - XV.6.c reproducible rebuild from plate truth + run artifacts
- XV.7 Schema and contract versioning (no silent drift)
  - XV.7.a schema version bump rules (when required; how recorded)
  - XV.7.b configuration versioning (config hash; semantic version, if adopted)
  - XV.7.c “no untracked schema changes” enforcement (validation hard-fails)
- XV.8 Distribution and interchange (optional but adoption-critical)
  - XV.8.a Parquet/Arrow as the canonical fact transport
  - XV.8.b WebDataset/HDF5/TFRecord only as derived packaging (never canonical truth)
  - XV.8.c IIIF export for institutional interoperability
  - XV.8.d Export/import invariants (IDs, checksums, and provenance survive round trips)

### XVI. Interfaces and Access Layers

**Purpose:** show how different audiences actually encounter the manifold.

- XVI.1 Minimal access: file browsing + manifests
- XVI.2 Dataset atlas: global figures + per-plate QC sheets
- XVI.3 Query interfaces
  - XVI.3.a notebook-driven querying (Colab)
  - XVI.3.b CLI querying (optional)
  - XVI.3.c web viewer / IIIF export (optional but likely necessary for institutional adoption)
- XVI.3.d GraphRAG / multimodal RAG (optional; only after provenance is stable)
- XVI.3.e API surfaces (optional; must not become authoritative storage)
- XVI.4 Access control and licensing constraints (if variants come from multiple institutions)

### XVII. Failure Modes and Open Problems

**Purpose:** demonstrate that brittleness and uncertainty are recorded, not hidden.

- XVII.1 Technical failure modes
  - XVII.1.a image size extremes; tiling complexity
  - XVII.1.b OCR brittleness on inscriptions
  - XVII.1.c segmentation failure cases (paper vs background confusion)
  - XVII.1.d embedding instability across crops/resolutions
  - XVII.1.e Drive/performance constraints; partial writes; kernel death
- XVII.2 Conceptual failure modes
  - XVII.2.a “variance fetishism” (collecting differences without interpretation discipline)
  - XVII.2.b premature ontology (naming motifs too early)
  - XVII.2.c institutional authority conflicts (who decides constraints?)
  - XVII.2.d conflation of stress tests with historical truth
- XVII.3 Open problems (explicit list; Appendix I expands)

### XVIII. Roadmap and Extensions

**Purpose:** define how this scales beyond Audubon without breaking principles.

- XVIII.1 Scaling to multi-institution, multi-variant corpora
- XVIII.2 Interoperability targets (optional but recommended)
  - IIIF manifests / annotations
  - standardized metadata crosswalks
- XVIII.3 Governance models for canonical constraints (curatorial boards, parameter bounds)
- XVIII.4 Research extensions
  - vectorization as second representation regime
  - affect/atmosphere embedding axes
  - robustness curves as “semantic fragility” measures
- XVIII.5 Publication roadmap (link to “galaxy” in `A_World_Burning/25-reel-it-in.md`)

### XIX. What This Project Refuses (non-claims and prohibitions)

**Purpose:** make refusals enforceable and citable.

- XIX.1 No single-image “best” output as canon
- XIX.2 No claims about original intent or definitive appearance
- XIX.3 No restoration authority (no “improvement” claims)
- XIX.4 No ecological forecasting or factual climate claims from stress images
- XIX.5 No biometric identity systems (general guardrail, even if Audubon is safe)
- XIX.6 No silent failure; no unregistered artifacts; no hidden state

### XX. Conclusion: Canon After Stability

- Summarize: canon as constraint; apparatus as infrastructure; variance as evidence
- Restate the promise: archives that can think later without lying now

---

## 4. Appendices (expand until nothing is implicit)

### Appendix A: Corpus and Source Registry (what the dataset is)

Rendered in: `A_World_Burning/32-appendix-a-corpus-and-source-registry.md`

**Goal:** define the population unambiguously; prevent ambiguity about what is “in”.

- A.1 Corpus boundary statement (Audubon plates 1–435; no exceptions)
- A.2 Plate identity crosswalk
  - A.2.a plate_number ↔ plate_id (zero padded)
  - A.2.b title, slug, canonical filenames
- A.3 Source registry schema
  - A.3.a institution/source name
  - A.3.b acquisition method and timestamp
  - A.3.c original URL / holding identifier
  - A.3.d license/credit statement
  - A.3.e checksums + file fingerprints
- A.4 Variant registry (if multiple digitizations are added)
  - A.4.a what makes a new “variant” distinct
  - A.4.b minimum fields for a variant to be admissible
- A.5 Exclusion log (what was rejected and why)

### Appendix B: File System, Naming Conventions, and Run IDs (disk-level ontology)

Rendered in: `A_World_Burning/33-appendix-b-filesystem-naming-run-ids.md`

**Goal:** reconstructibility; file organization as argument.

- B.1 Canonical directory map (current vs planned evolution; decision recorded)
- B.2 Naming law
  - B.2.a plate directories: `plate-###` only
  - B.2.b run directories: chosen run_id scheme; collision rules
  - B.2.c derived artifacts: `<plate_id>__<run_id>__<artifact_type>__<descriptor>.<ext>`
- B.3 Plate manifest schema (full field list + constraints)
- B.4 Run manifest schema (full field list + constraints)
- B.5 Checksum strategy
  - B.5.a `source.sha256` per plate/variant
  - B.5.b optional per-run `run.sha256`
- B.6 Validators (filesystem + schema + run sealing)
- B.7 Ledger rebuild contract (how to regenerate parquet from plate truth)

### Appendix C: Feature Extraction Inventory (complete; no omissions)

Rendered in: `A_World_Burning/34-appendix-c-feature-extraction-inventory.md`

**Goal:** exhaustive list of computed features, with what they capture and fail to capture.

This appendix should mirror the extraction inventory in `A_World_Burning/00_preprocessing_assay.md` but in a “paper-ready” form:

- C.1 Feature families (File/container; global pixel; CV; embeddings; segmentation; OCR; captions; forensics; quality; indices)
- C.2 For each feature family, specify:
  - C.2.a purpose (what question it answers)
  - C.2.b computational regime (CPU/GPU; full-pass vs sampled vs tiled)
  - C.2.c output shape/schema (fields, dimensionality, normalization)
  - C.2.d storage location (plate-local vs ledger)
  - C.2.e known failure modes and bias
- C.3 Full enumerated inventory (copy the numbered list 1–45, verbatim or as a strict mapping)
- C.4 Versioning policy (what requires a schema bump; what is additive)

### Appendix D: Segmentation Methods and Parameters (no semantic overreach)

**Goal:** segmentation is documented as structure extraction, not meaning assignment.

Rendered in: `A_World_Burning/35-appendix-d-segmentation-methods-and-parameters.md`

- D.1 Model registry (SAM variants; Mask2Former; others)
- D.2 Input policies (resizing, tiling, cropping)
- D.3 Mask generation parameters and any filtering heuristics
- D.4 Mask representations and conversions (PNG ↔ RLE ↔ polygons)
- D.5 Rejection criteria (hard failures)
- D.6 QC metrics and dashboards
- D.7 What segmentation is explicitly not allowed to claim

### Appendix E: Reproducibility Protocols (lab protocol)

**Goal:** make runs reproducible and failures legible.

Rendered in: `A_World_Burning/36-appendix-e-reproducibility-protocols.md`

- E.1 Notebook templates (CPU vs GPU) and mandatory section order
- E.2 Randomness policy
  - E.2.a explicit seeding where possible
  - E.2.b documenting nondeterminism where not
- E.3 Environment capture
  - E.3.a library versions
  - E.3.b model checkpoint identifiers
  - E.3.c hardware info (GPU name/VRAM)
- E.4 Batch execution protocol (resume-safe; append-only)
- E.5 Failure logging protocol (no silent failure; partial writes handled)
- E.6 Drift checks (rerun baseline; checksum revalidation)
- E.7 Notebook phase schedule (Audubon implementation; optional but clarifying)
  - E.7.a contract + handoff (read-only)
  - E.7.b ingestion + canonicalization (manifest/checksum/scaffold)
  - E.7.c header-only extraction (optional split: `image_header.json`)
  - E.7.d scalar pixel-pass extraction (`input_image.json`)
  - E.7.e segmentation run(s) (`segments.parquet`)
  - E.7.f embedding run(s) (`embeddings.parquet`)
  - E.7.g QC atlas generation (figures + known failures ledger)
- E.8 Hardware capability detection + adaptive batching defaults
  - E.8.a detect GPU name/VRAM and classify (CPU/T4/L4/A100-ish)
  - E.8.b per-model capability profiles (image_size, dtype, batch_size)
  - E.8.c clamp batch sizes on weaker GPUs; fail fast if GPU required
- E.9 Prompt registry discipline (if VLM captioning/tagging is used)
  - E.9.a prompt templates live in a versioned registry (e.g., `prompt_registry.yaml`)
  - E.9.b every caption/tag row stores prompt_id + prompt_version + model_id

### Appendix F: Climate Perturbation Regimes (downstream stress definition)

**Goal:** define stress transforms precisely without contaminating documentation.

Rendered in: `A_World_Burning/37-appendix-f-climate-perturbation-regimes.md`

- F.1 Parameter axes and their conceptual interpretation
- F.2 Allowed transforms (examples: thermal shift, haze/ash, nocturne artifacts, contrast collapse)
- F.3 Safeguard constraints (edge preservation thresholds, semantic drift ceilings)
- F.4 Prohibitions (no new anatomy; no “restoration”; no factual climate claims)
- F.5 Logging requirements (transform manifests; parameter capture; run IDs)

### Appendix G: Ethical and Interpretive Guardrails (formal refusals)

**Goal:** prevent automated authority and misuse.

Rendered in: `A_World_Burning/38-appendix-g-ethical-and-interpretive-guardrails.md`

- G.1 Non-claims (no intent inference; no definitive appearance claims)
- G.2 No restorative authority
- G.3 No biometric identity systems (general rule; face embeddings only for local alignment/blur/dedup if ever relevant)
- G.4 Weak-label policy (VLM outputs treated as weak signals; never truth)
- G.5 Institutional respect (credit, licensing, provenance)
- G.6 Security hygiene (secrets management; no `.env` leaks; threat model)

### Appendix H: Model Cards and Dependency Registry (epistemic + legal clarity)

**Goal:** list everything that could bias results or violate licensing.

Rendered in: `A_World_Burning/39-appendix-h-model-cards-and-dependency-registry.md`

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
  - H.5.b L4 (24GB) “sweet spot” assumptions and expanded model set
  - H.5.c A100 (40GB) optional “maximal” set (non-blocking)
  - H.5.d dtype policy (fp16/bf16/tf32) and its implications for comparability

### Appendix I: Known Limitations and Open Questions (ledger of uncertainty)

**Goal:** show what remains unresolved, and why that matters.

Rendered in: `A_World_Burning/40-appendix-i-known-limitations-and-open-questions.md`

- I.1 Dataset gaps (missing variants, institutional blind spots)
- I.2 Measurement brittleness (OCR, segmentation, embeddings)
- I.3 Governance questions (who sets constraints? how to revise them?)
- I.4 Evaluation questions (what benchmarks are legitimate?)
- I.5 Sustainability questions (storage cost, long-term verification)

### Appendix J: Glossary of Terms (enforced internal consistency)

**Goal:** prevent incompatible readings by defining loaded terms.

Rendered in: `A_World_Burning/41-appendix-j-glossary.md`

- plate, variant, run, manifest, ledger
- canonical, edition, manifold, apparatus
- provenance, immutability, auditability
- measurement vs interpretation vs transformation
- semantic drift, robustness curve, stability, failure mode

---

## 5. “Absurdly Exhaustive” Checklists (author-facing, optional in published version)

These are working checklists; they may be moved into a private/internal appendix, but they must exist.

### 5.1 Preprocessing completeness checklist

- All plates registered; manifests valid; sources checksummed
- Baseline scalar facts extracted and stored
- Optional distributions decided (on/off) and documented
- Segmentation executed or explicitly deferred
- Embeddings executed (global; optional segment/tile)
- Ledgers built and rebuildable from plate-local truth
- QC atlas generated; known failures logged

### 5.2 “No silent failure” checklist (per notebook/run)

- Structure assertion ran before any compute
- Config declared and hashed
- All outputs registered in manifest
- Post-run validation succeeded
- Ledger sync updated
- Run sealed (status complete + checksums recorded)

### 5.3 Citation checklist (for scholarship)

- If citing a source variant: include source registry ID + checksum + access date
- If citing a derived measurement: include run_id + config hash + model IDs + ledger version
- If citing a transformation: include transform run_id + parameter set + safeguard metrics
