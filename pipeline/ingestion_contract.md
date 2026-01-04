# Ingestion Contract (Filesystem + Run Semantics)

This document defines the minimum, failure-intolerant rules for ingesting and measuring plates so that:

- source files remain immutable evidence,
- derived artifacts are append-only and auditable,
- run outputs are discoverable and verifiable,
- downstream interpretation never contaminates the core dataset.

See also: `GOVERNANCE_CHECKLIST.md`

---

## 1. Governing Principles (Non-Negotiable)

1. Files are evidence.
   - Every derived file must be attributable to a plate, a run ID, a method/model ID, parameters, and a timestamp.
2. No silent failure.
   - Any deviation from naming/schema/linkage is a hard error; the run aborts; nothing is written.
3. Append-only semantics.
   - No overwrites. Ever. Corrections are new runs.
4. Core vs derived separation.
   - Core = immutable source image + plate manifest.
   - Derived = append-only artifacts under `runs/<run_id>/...`.

---

## 2. Canonical Destination vs `_RUN_OUTPUT/`

- `_RUN_OUTPUT/` is explicitly a working/staging destination.
- For now, validated runs are treated as canonical in place on local disk.
- Path law: `_RUN_OUTPUT/` is authoritative until a remote store is defined; when that happens, runs are copied unchanged.

---

## 3. Schema Authority

- Schemas are authoritative in-repo (versioned).
- Jobs/notebooks may copy schemas into run outputs for self-description but must not originate or modify schemas there.
- Any schema copied into a run output must reference the repo version/hash.

---

## 4. Directory Layout (Minimum Contract)

Input dataset root (read-only):

```
<DATASET_ROOT>/
  data.json
  schemas/
    plate.manifest.schema.json
    run.manifest.schema.json
    ...
  plates_structured/
    plate-001/
      manifest.json
      source/
        <immutable source image referenced by manifest.json>
    plate-002/
      ...
```

Run output root (write-only; may equal `<DATASET_ROOT>/_RUN_OUTPUT`):

```
<OUTPUT_ROOT>/
  schemas/                      # optional copies for self-description
  reports/
    <run_id>/
      report.json
  plates_structured/
    plate-001/
      runs/
        <run_id>/
          metrics.json
          <run artifacts...>
```

---

## 5. Run Registry / Discovery

- Canonical registry is `reports/<run_id>/report.json`.
- Discovery is by enumerating `reports/` (an aggregated index is optional later, and must be derived).

---

## 6. Verification Checklist (Hard Gates)

A run is considered valid only if all of the following pass:

1. Plate count invariant: expected number of plates is present (Audubon: 435).
2. Plate manifests validate against `schemas/plate.manifest.schema.json`.
3. Source files exist for every selected plate (`manifest.json.source_image` resolves to an existing file).
4. Run manifest (`metrics.json`) exists for every processed plate and validates against `schemas/run.manifest.schema.json`.
5. Required run artifacts exist for every processed plate (job-specific).
6. Run-level report exists at `reports/<run_id>/report.json` and includes required fields:
   - `run_id`, `timestamp`, `dataset_root`, `output_root`, `plates_total`, `plates_selected`, `plates_processed`, `decode_failures`, `schema_failures`
7. Output schemas validate (when applicable): if an artifact schema exists, artifacts must validate against it.

---

## 7. Provenance Requirements (Minimum)

Each derived artifact must carry enough provenance to reproduce and audit it:

- `plate_id`
- `run_id`
- `timestamp` (UTC recommended)
- input reference(s) (`source_image` path; checksums where applicable)
- `method` / `model` identifier
- `params`
- code version/hash (recorded either inside the artifact or in `report.json`)

No new tooling is required to enforce this; it is a required field set.

