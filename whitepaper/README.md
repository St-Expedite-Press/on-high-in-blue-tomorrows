# Whitepaper / Book Structure

This folder is the **book/whitepaper root** for _The Burning World_. The goal here is to make the project readable as a single coherent document while preserving the raw materials and technical contracts elsewhere.

**Start here:** [DRAFT](DRAFT.md)

**Crosswalk from raw materials -> sections:** [MATERIALS_MAP](MATERIALS_MAP.md)

---

## What to read (in order)

- [DRAFT](DRAFT.md) (compiled reading surface)
- `00-front-matter/introduction.md` (working introduction)
- `sections/README.md` (I–XX)
- `appendices/README.md` (A–J)

---

## Editing principle (the “melt”)

- The **body sections** should read like finished argument/spec.
- The appendices can remain exhaustive, but sections should **link out** rather than replicate tables.
- Nothing is deleted; source notes remain as provenance and are linked from each section.

---

## Legacy: Colab workflow notes (preserved verbatim)

The content below was previously stored as `whitepaper/README.md`. It is kept here verbatim so nothing is lost, but it should be treated as implementation-facing notes rather than the paper structure.

---

# Google Colab workflows

This folder keeps **Colab-specific notebooks** and an **append-only work log** for the `burning-world-series` dataset preparation work.

- Notebooks live in `colab/notebooks/`
- The running log lives in `colab/RUNNING_LOG.md`

The goal is MVP-first: make the minimum stable scaffolding to ensure every later step (segmentation, embeddings, model runs, QC) is reproducible and auditable.

## What this folder is (and is not)

- This is a place for notebooks that operate on Google Drive mounted data (Colab runtime).
- This is not a general-purpose Python package or a replacement for source control; derived artifacts should be rebuildable.

## Notebooks

- `colab/notebooks/audubon_bird_plates_setup.ipynb`
  - Drive mount + dataset discovery
  - Plate indexing + JSON/disk validation (expects 435 entries)
  - `plates_structured/` scaffolding and per-plate `manifest.json`
  - JSON schemas (`schemas/`)
  - Source checksums (`source.sha256`)
  - Run helper functions (append-only `runs/`)
  - Empty Parquet ledger scaffold (`ledger/`)
  - Read-only system validation report (asserts invariants)
- `colab/notebooks/audubon_bird_plates_handoff.ipynb`
  - Read-only project/dataset loader (canonical paths + light sanity checks)
  - Structure + naming contract assertion (read-only)
  - Optional cleanup + exploratory inspection cells

## Running log

`colab/RUNNING_LOG.md` is append-only and should record:

- Which notebook(s) were run
- What invariants were asserted
- What directories/files were created
- Anything that might explain a later mismatch (e.g., a dataset re-download)

If something changes that breaks reproducibility, log it first.

## File naming scheme (asserted)

These conventions are treated as **invariants** and are asserted in
`colab/notebooks/audubon_bird_plates_setup.ipynb` and `colab/notebooks/audubon_bird_plates_handoff.ipynb`.

### Project + dataset roots

- **Project root**: `/content/drive/MyDrive/burning-world-series`
- **Dataset directory**: a child directory whose name starts with:
  - `audubon-bird-plates`

### Plate images (raw)

- **Plates directory**: `DATASET_ROOT/plates/`
- **Plate filenames**: `plate-*.jpg`
  - Expected count: `435` plates referenced in `DATASET_ROOT/data.json`

### Plate structure (derived)

For each plate, we create:

- `DATASET_ROOT/plates_structured/plate-###/`
  - `manifest.json` (one per plate; schema-validated)
  - `source/` (contains exactly one copied source image)
  - `source.sha256` (sha256 checksum of the source image)
  - `runs/` (append-only run outputs)
  - `viz/` (visualizations)
  - `cache/` (derived caches)

The directory name format is fixed:

- `plate-###` where `###` is zero-padded (`001`..`435`)
- Regex: `^plate-[0-9]{3}$`

### Schemas (derived, persisted)

- `DATASET_ROOT/schemas/plate.manifest.schema.json`
- `DATASET_ROOT/schemas/run.manifest.schema.json`

### Runs (derived, append-only)

Each run directory is created under a specific plate:

- `DATASET_ROOT/plates_structured/plate-###/runs/run-YYYYMMDD-HHMMSS-<hash>/`
  - `metrics.json` (run manifest; outputs are registered here)

Run ID format (from `generate_run_id`):

- Example: `run-20260101-235959-1a2b3c4d`
- Regex: `^run-[0-9]{8}-[0-9]{6}-[0-9a-f]{8}$`

### Ledger (derived, rebuildable)

The ledger directory contains **empty Parquet files with fixed schemas**:

- `DATASET_ROOT/ledger/plates.parquet`
- `DATASET_ROOT/ledger/runs.parquet`
- `DATASET_ROOT/ledger/embeddings.parquet`
- `DATASET_ROOT/ledger/segments.parquet`

## Adding new notebooks (convention)

Put new notebooks in `colab/notebooks/` and keep the name:

- lower snake_case
- dataset-specific
- purpose-specific

Suggested pattern:

- `<dataset>_<purpose>.ipynb`
  - Example: `audubon_bird_plates_embeddings.ipynb`

If a notebook creates new derived artifacts, update:

- `colab/RUNNING_LOG.md`
- This README's "File naming scheme" section (if you introduce new invariant paths)
