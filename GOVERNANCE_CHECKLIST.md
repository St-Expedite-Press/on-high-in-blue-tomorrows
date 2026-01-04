# Project Governance Checklist (Loose Ends)

This file freezes intent and policy decisions without forcing infrastructure choices prematurely.

## Storage / Destination

- `_RUN_OUTPUT/` is explicitly a working/staging destination.
- For now, validated runs are treated as canonical **in place on local disk**.
- Path law: `_RUN_OUTPUT/` is authoritative until a remote store is defined; when that happens, runs are copied unchanged (no migration decision required yet).

## Schema Authority

- Schemas are authoritative in-repo (`schemas/`, versioned).
- Jobs/notebooks may copy schemas into run outputs for self-description but must not originate or modify schemas there.
- Any schema copied into a run must reference the repo version/hash.

## Verification (Hard Gates)

Define a minimal invariant checklist that must pass for a run to be considered valid:

- plate count invariant
- `manifest.json` schema validation
- source file presence
- required output files exist
- output schema validation
- required report fields present

This checklist lives in `pipeline/ingestion_contract.md`.

## Run Registry / Index

- For now, `reports/<run_id>/report.json` is the canonical registry.
- A derived index (JSONL/Parquet) may be added later; discovery currently happens by enumerating `reports/`.

## Ontology Binding

- Add explicit mappings from concrete fields (e.g., `cpu_baseline.pixel_stats.clip_L_high_ratio`, `segmentation.foreground_ratio`) to ontology terms so the ontology attaches to files, not abstractions.

## Core vs Derived Naming Law

- Core = immutable source image + plate manifest.
- Derived = append-only artifacts under `runs/<run_id>/...`.
- No overwrites.

## Provenance Requirements (Minimum)

Standardize a required provenance block for derived artifacts (no new tooling required; just a required field set):

- inputs used (paths + checksums where applicable)
- params
- method/model ID
- code version/hash
- `run_id` linkage

