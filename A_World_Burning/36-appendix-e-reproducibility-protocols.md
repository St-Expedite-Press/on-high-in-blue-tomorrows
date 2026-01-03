# Appendix E: Reproducibility Protocols (Sealed Runs as Lab Practice)

[[A_World_Burning/README]] | [[A_World_Burning/30-whitepaper-toc]] | [[A_World_Burning/26-whitepaper-skeleton]]

This appendix specifies the reproducibility discipline of _The Burning World_. It is written deliberately like a lab protocol: if someone follows it, they should be able to reproduce the dataset’s measurements (or reproduce the documented failure modes) without oral tradition.

Core doctrine:

- plate-local artifacts are primary truth
- runs are sealed, append-only events
- ledgers are derived, rebuildable views

Related:

- Filesystem + run IDs: `33-appendix-b-filesystem-naming-run-ids.md`
- Feature inventory: `34-appendix-c-feature-extraction-inventory.md`
- Prompt registry discipline (if VLM/captioning is used): `00_preprocessing_assay_addendum.md`

---

## E.1 The run lifecycle (non-negotiable)

Every run follows the same lifecycle. A “run” is not “a notebook cell that happened to finish.” It is a sealed event with an identity.

### E.1.1 Pre-run: validate and declare

Before any compute:

- validate plate structure (manifest, exactly-one source file in bootstrap mode, checksum matches)
- validate schemas (manifest schemas load; strict validation)
- declare the intended outputs (what will be written)
- write `config.json` (the full parameterization)

### E.1.2 Mint run ID and create run directory

- compute `config_hash = sha256(config.json)`
- mint `run_id` using the scheme in Appendix B
- create `runs/<run_id>/` directory
- write `run.manifest.json` with status `incomplete`

### E.1.3 Execute compute

- write outputs only under `runs/<run_id>/outputs/…`
- enforce naming law on every artifact
- fail fast on mismatched shapes, missing outputs, or invalid filenames

### E.1.4 Post-run: validate outputs and seal

- verify every output listed in the manifest exists
- compute and record checksums for outputs
- set `run.manifest.json` status to `complete` (or `failed`)
- optionally write `run.sha256` as a convenience checksum bundle

---

## E.2 Configuration discipline (no hidden state)

The goal is to prevent “private knobs” that cannot be audited later.

### E.2.1 `config.json` is mandatory

`config.json` must include:

- task type (embedding / segmentation / OCR / etc.)
- model IDs + pinned revisions (if pretrained)
- input selection (source vs working raster vs tile set)
- preprocessing policy (resize, crop, colorspace, mask handling)
- batching policy (batch size, dtype)
- seed policy (see E.3)

### E.2.2 Config hashing

- `config_hash` is recorded in the run manifest
- any change to `config.json` implies a new run ID (do not edit old runs)

---

## E.3 Randomness control (determinism where possible; bounded nondeterminism where not)

### E.3.1 When determinism is expected

Deterministic results are expected for:

- CPU-only scalar extractions
- checksum computations
- pure geometry computations (bbox/area from a fixed mask)

### E.3.2 When nondeterminism is acceptable (but must be declared)

Some GPU inference paths can vary due to:

- nondeterministic kernels
- mixed precision differences
- differing library versions

Policy:

- record seeds even if they do not fully determine outcomes
- record `torch`, `cuda`, and GPU type
- treat observed drift as a measurement: store it, don’t hide it

---

## E.4 Environment capture (runs are only comparable if their environments are legible)

Every run must record environment metadata sufficient to reproduce or explain drift:

- python version
- OS + kernel/runtime context (Colab vs local)
- library versions (at minimum: torch, torchvision, transformers, numpy, pyarrow)
- GPU name + VRAM
- CUDA/cuDNN versions (if applicable)
- code version:
  - git commit SHA if you are in a repo
  - or a hashed notebook snapshot identifier

This can live in:

- `run.manifest.v2.json`, or
- an `environment.json` output under the run directory

---

## E.5 Failure handling (runs can fail; history cannot disappear)

### E.5.1 Partial runs are still evidence

If a run fails:

- keep the run directory
- write `run.manifest.json` status `failed`
- record the failure mode (error type, message, stage)

### E.5.2 No silent overwrites

- never overwrite an output file
- never “fix” a run by editing inside its directory
- corrections are new runs

### E.5.3 Crash survivability (Colab reality)

Design so that:

- a run can be resumed by minting a new run (not by editing the old run)
- partially computed outputs never masquerade as complete

---

## E.6 Ledger rebuild protocol (derived views are disposable)

Ledgers are convenience views; the dataset survives without them.

### E.6.1 Rebuild steps (minimum)

1. scan plates and validate manifests/checksums
2. enumerate run directories and validate run manifests
3. rebuild:
   - `plates.parquet` from plate manifests + derived facts
   - `runs.parquet` from run manifests
   - `embeddings.parquet` from embedding outputs
   - `segments.parquet` from segmentation outputs

### E.6.2 Ledger schema evolution

When you add columns:

- treat it as additive whenever possible
- record a schema version (Parquet metadata or explicit column)
- never silently reinterpret an existing column

---

## E.7 Publication packaging (derived distribution without undermining truth)

The corpus may be packaged for consumption (Parquet bundles, WebDataset shards, IIIF exports). These packages must be:

- explicitly labeled as derived
- rebuildable from plate-local truth + run artifacts
- accompanied by release manifests and checksums

See `00_preprocessing_assay_addendum.md` for the packaging discipline.

---

## E.8 “No untagged claims” rule (applies to prose about measurements)

In the whitepaper, every subsection ends with an evidence tag:

- `[MEASURED]`
- `[DERIVED]`
- `[INTERPRETIVE]`
- `[SPECULATIVE / FUTURE WORK]`

This rule is how the project prevents interpretive drift from contaminating documentation.
