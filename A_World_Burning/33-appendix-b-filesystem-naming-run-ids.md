# Appendix B: File System, Naming Conventions, and Run IDs

[[A_World_Burning/README]] | [[A_World_Burning/30-whitepaper-toc]] | [[A_World_Burning/26-whitepaper-skeleton]]

This appendix formalizes the disk-level ontology of _The Burning World_ dataset: **where things live**, **what they are called**, and **how runs are identified** so that a third party can reconstruct the project without oral tradition.

This is not “organization advice.” It is part of the project’s epistemic claim: canon attaches to **constraints + auditability infrastructure**, not to a single file.

---

## B.1 Definitions (used throughout)

- **Dataset root**: the directory that contains `plates_structured/`, `ledger/`, and `schemas/` (current bootstrap layout), or an isomorphic “formal layout” (see B.2.2).
- **Plate**: the atomic unit (`plate-###`).
- **Variant**: one immutable source image for a given plate identity (multi-source future mode).
- **Derived**: a deterministic byproduct computed from an immutable input (e.g., `input_image.json`).
- **Run**: a sealed, append-only event that executes a model/algorithm and emits artifacts + a run manifest.
- **Ledger**: a derived, rebuildable table (Parquet) that indexes plate-local truth and run outputs.

---

## B.2 Canonical directory layouts (bootstrap vs formal)

### B.2.1 Bootstrap layout (current notebooks; ground truth)

The two completed notebooks (`notebooks/*.ipynb`) write and validate this structure:

```
<DATASET_ROOT>/
  plates/                         # raw download staging (optional; may be ranges/1-99 etc)
  plates_structured/              # plate-centric canonical form (authoritative)
    plate-001/
      manifest.json
      source.sha256
      source/
        <one immutable source image file>
      derived/                    # deterministic per-plate derived facts (optional)
      runs/                       # sealed run folders (optional)
    ...
    plate-435/
  schemas/
    plate.manifest.schema.json
    run.manifest.schema.json
  ledger/                         # derived, rebuildable Parquet tables
    plates.parquet
    runs.parquet
    embeddings.parquet
    segments.parquet
```

Notes:

- `plates_structured/` is the authoritative plate-centric namespace in bootstrap mode.
- `plates/` is optional; it is a staging area, not canonical evidence once bytes are copied into `plates_structured/<plate>/source/`.

### B.2.2 Formal layout (paper-facing; isomorphic to bootstrap)

Some planning documents propose a more explicit top-level ontology (raw vs structured vs ledgers). This is recommended for publication and multi-corpus scaling, but it must remain **isomorphic** to the bootstrap contract:

```
burning-world-series/
  datasets/
    audubon/
      raw/
        img/
          ranges/                 # 1-99/, 100-199/, ...
        data.json                 # snapshot used for acquisition (checksummed)
        README.md                 # snapshot used for acquisition (checksummed)
      structured/
        plate-001/ ... plate-435/
      viz/                        # human-facing previews (never authoritative)
  ledgers/
  schemas/
  validators/
  notebooks/
  docs/
```

Migration rule:

- Do not half-migrate. Either stay in bootstrap layout, or migrate once and update validators to enforce the new root.

### B.2.3 Isomorphism mapping (bootstrap → formal)

| Bootstrap path | Formal path |
|---|---|
| `<DATASET_ROOT>/plates_structured/` | `burning-world-series/datasets/audubon/structured/` |
| `<DATASET_ROOT>/plates/` | `burning-world-series/datasets/audubon/raw/img/` |
| `<DATASET_ROOT>/ledger/` | `burning-world-series/ledgers/` |
| `<DATASET_ROOT>/schemas/` | `burning-world-series/schemas/` |

---

## B.3 Plate directory contract (what must exist per plate)

### B.3.1 Plate ID law (immutable)

- Plate IDs are zero-padded: `plate-001` … `plate-435`.
- Plate IDs are **never inferred** from filenames after bootstrap.
- Plate identity is defined by `manifest.json`, not by the source filename.

### B.3.2 Required files

Minimum required per plate:

- `manifest.json` (schema-valid)
- `source/` containing **exactly one** immutable source image file (bootstrap mode)
- `source.sha256` (sha256 of that source image file)

Recommended (not required in bootstrap, but expected for “preprocessing completion”):

- `derived/input_image.json` (baseline scalar extraction)
- `derived/image_header.json` (optional header-only extraction)
- `runs/` (when any model run is executed)

### B.3.3 Plate manifest schema (bootstrap; frozen)

The bootstrap notebook writes `schemas/plate.manifest.schema.json` with these required fields:

- `plate_id` (pattern `^plate-[0-9]{3}$`)
- `plate_number` (integer 1–435)
- `title` (string)
- `slug` (string)
- `source_image` (string path relative to the plate directory)

Additional fields present in the schema (optional):

- `download_url` (string|null)
- `license` (string)
- `created_at` (date-time string)

Constraint: `additionalProperties: false` (unknown fields are rejected).

### B.3.4 Variant namespace (future “variance mode”)

When multiple institutional digitizations are ingested for the same plate identity, the plate directory becomes a *variant container*.

Recommended structure (additive; does not break bootstrap):

```
plate-123/
  variants/
    v-000001/
      source/
        <immutable bytes>
      source.sha256
      variant.manifest.json
    v-000002/ ...
```

Rules:

- Variants are immutable evidence.
- Any cropping/normalization is performed as derived artifacts or runs, never in-place.

Appendix A defines the required variant registry fields; Appendix C defines which features operate at plate vs variant scope.

---

## B.4 Run directory contract (sealed events)

Runs are append-only and never edited. Corrections are new runs.

### B.4.1 Required run folder structure (recommended)

Within a plate directory:

```
runs/
  <run_id>/
    run.manifest.json
    config.json
    outputs/
      embeddings/
      segments/
      metrics/
      visuals/
    run.sha256                # optional, but recommended
```

Bootstrap note:

- The bootstrap notebooks define the **run manifest schema** but do not yet create run folders. This appendix specifies the required contract for when runs begin.

### B.4.2 Run manifest schema (bootstrap; frozen minimal)

The bootstrap notebook writes `schemas/run.manifest.schema.json` with:

Required:

- `run_id` (string)
- `plate_id` (string)
- `timestamp` (date-time string, UTC recommended)
- `models` (string[])
- `outputs` (string[])

Optional:

- `notes` (string|null)

Constraint: `additionalProperties: false`.

### B.4.3 Recommended run manifest extension (paper-grade)

Because bootstrap schema is strict, the safe way to extend it is to:

- mint a new schema ID (e.g., `run.manifest.v2.schema.json`), and
- write `run.manifest.v2.json` for v2 runs, while keeping bootstrap runs v1-valid.

Suggested v2 fields (minimum to make runs citable):

- `schema_version` (e.g., `2`)
- `run_id` (see B.5)
- `plate_id`
- `variant_id` (nullable; required in variance mode)
- `created_at` (UTC timestamp)
- `code_version` (git SHA or “notebook hash”)
- `environment` (python, torch, cuda versions)
- `models`: array of objects:
  - `model_id` (HF id or library name)
  - `model_sha` (pinned revision)
  - `task` (embedding/segmentation/detection/ocr/caption)
- `inputs`: array of objects:
  - `path` (relative)
  - `sha256`
- `outputs`: array of objects:
  - `path` (relative)
  - `sha256`
  - `artifact_type` (embedding/segment/metric/viz/etc.)
  - `record_count` (optional)
- `config_hash` (sha256 of `config.json`)
- `status` (`incomplete` | `complete` | `failed`)
- `failure` (nullable; structured error info if failed)

This extension preserves the system law: plate-local truth is primary; ledgers are derived views.

---

## B.5 Run IDs (collision-resistant, meaningful, reproducible)

### B.5.1 Required properties of a run ID

A run ID must:

- be unique within the dataset root
- be reproducible from run metadata (or at least deterministically generated)
- be sortable by time (for audit convenience)
- be safe in filenames (ASCII, no spaces)

### B.5.2 Recommended run ID format (hybrid)

```
run-YYYYMMDD-HHMMSSZ-<hash8>
```

Where:

- timestamp is UTC (`Z`)
- `<hash8>` is the first 8 hex chars of a sha256 over a canonical string that includes:
  - model IDs + model SHAs
  - `config.json` bytes
  - `code_version`

Example:

```
run-20260102-031455Z-2c1a9f0b
```

### B.5.3 Run ID generation protocol (canonical)

1. Write `config.json` first.
2. Compute `config_hash = sha256(config.json)`.
3. Build `run_hash_material = models + model_shas + config_hash + code_version`.
4. Compute `hash8 = sha256(run_hash_material)[:8]`.
5. Mint `run_id` from UTC timestamp + `hash8`.
6. Create the run directory; abort if it already exists.

Important:

- Never reuse a run ID across different outputs.
- If a run fails, keep the run directory and mark status `failed`; do not delete history.

---

## B.6 Derived artifact naming law (lineage encoded in filenames)

Every derived file written under a run must encode lineage:

```
<plate_id>__<run_id>__<artifact_type>__<descriptor>.<ext>
```

Examples:

```
plate-123__run-20260102-031455Z-2c1a9f0b__embedding__clip-vit-large-patch14.npy
plate-123__run-20260102-031455Z-2c1a9f0b__segment__sam-vit-large__mask-0004.png
plate-123__run-20260102-031455Z-2c1a9f0b__metric__entropy.json
```

Reserved `artifact_type` set (recommendation; extend only with documentation):

- `manifest` (run manifests, config)
- `metric` (JSON scalars + small vectors)
- `embedding` (vectors)
- `segment` (masks, RLE/COCO, polygon approximations)
- `tile` (tile images or tile descriptors)
- `ocr` (text boxes + transcripts)
- `caption` (generated text + prompt ids)
- `viz` (figures; QC sheets; previews)
- `index` (FAISS/ScaNN files)

---

## B.7 Checksums (immutability enforcement)

### B.7.1 Source checksums (required)

`source.sha256` must contain the sha256 digest of the single file in `source/`.

Rules:

- The source bytes never change once ingested.
- If upstream bytes change, mint a new variant (variance mode) or re-ingest explicitly; never overwrite.

### B.7.2 Run checksums (recommended)

`run.sha256` is recommended as a convenience artifact that lists sha256 checksums of:

- `run.manifest.json`
- `config.json`
- every file under `outputs/`

This enables fast post-run verification without re-walking the whole tree.

---

## B.8 Ledgers (derived, rebuildable, and disposable)

The bootstrap notebook creates empty Parquet ledgers under `ledger/`:

- `plates.parquet`
- `runs.parquet`
- `embeddings.parquet`
- `segments.parquet`

System law:

- Ledgers are **views**, not truth. If a ledger is corrupted, it must be rebuildable by scanning plate manifests and run artifacts.

### B.8.1 Ledger rebuild contract (minimum)

A ledger rebuild operation must:

1. Validate plate manifests + source checksums.
2. Enumerate run folders; validate run manifests + output existence.
3. Recompute or re-read the derived row sets:
   - one row per plate (`plates.parquet`)
   - one row per run (`runs.parquet`)
   - one row per embedding record (`embeddings.parquet`)
   - one row per segment (`segments.parquet`)

### B.8.2 Ledger schema evolution

The v0 ledger schemas in the bootstrap notebook are intentionally minimal. For paper-grade work, add new columns but preserve:

- stable primary keys (`plate_id`, `run_id`, `segment_id`)
- explicit `schema_version` for each ledger file (as Parquet metadata or a column)

Appendix C specifies the feature families that drive schema expansion.

---

## B.9 Validators (brutal rejection rules; no silent failure)

Even before full automation, the following validators are conceptually mandatory:

### B.9.1 Plate validator

Reject a plate if:

- `manifest.json` is missing or schema-invalid
- `source/` is missing
- `source/` contains 0 or >1 files (bootstrap mode)
- `source.sha256` is missing or does not match source bytes

### B.9.2 Run validator

Reject a run if:

- `run.manifest.json` is missing or invalid
- any listed output path does not exist
- any output filename violates the naming law (B.6)
- model IDs are missing or unpinned (no sha recorded) for pretrained models

### B.9.3 Ledger validator

Reject a ledger build if:

- any ledger row cannot be reverse-resolved to a plate/run artifact on disk
- key uniqueness constraints fail (duplicate `run_id`, duplicate `(run_id, segment_id)`, etc.)

---

## B.10 “Viz is not evidence” rule

Human-facing preview artifacts (QC sheets, thumbnails, atlas pages) are useful, but they are never authoritative.

Rules:

- `viz/` outputs may be regenerated at any time.
- Do not store the only copy of a measurement in a figure; store the measurement in JSON/Parquet, then render.

---

## B.11 Minimal worked example (one plate, one embedding run)

```
<DATASET_ROOT>/
  plates_structured/
    plate-123/
      manifest.json
      source.sha256
      source/
        plate-123.original.jpg
      runs/
        run-20260102-031455Z-2c1a9f0b/
          run.manifest.json
          config.json
          outputs/
            embeddings/
              plate-123__run-20260102-031455Z-2c1a9f0b__embedding__openai-clip-vit-large-patch14.npy
            metrics/
              plate-123__run-20260102-031455Z-2c1a9f0b__metric__embedding_norms.json
```

With corresponding derived ledger rows:

- `ledger/runs.parquet` contains run provenance
- `ledger/embeddings.parquet` contains the vector pointer and declared dimensionality

---

## B.12 What this appendix guarantees

If Appendix B is obeyed, then:

- any artifact can be traced to a plate, a run, and a configuration
- the dataset can survive notebook crashes and partial failures without losing provenance
- the “canonical edition” is portable: copy the tree, keep checksums, and the edition persists
