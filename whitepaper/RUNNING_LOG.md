# Colab running log (append-only)

Keep this file as an append-only record of what we've done in Google Colab so far.

## Dataset: Audubon bird plates

### Session: Initial scaffolding

- Mounted Google Drive at `/content/drive` and located the project at `/content/drive/MyDrive/burning-world-series`.
- Discovered the dataset directory `audubon-bird-plates*` under the project root.
- Indexed `plates/plate-*.jpg` files and validated `data.json` (expected `435` entries) matches what's on disk.
- Created `plates_structured/plate-###/` layout for each plate:
  - `source/` (copies original plate image)
  - `runs/` (append-only run outputs)
  - `viz/` (visualizations)
  - `cache/` (derived caches)
- Wrote `manifest.json` per plate (idempotent: re-runs reuse existing manifests).
- Authored JSON Schemas:
  - `schemas/plate.manifest.schema.json`
  - `schemas/run.manifest.schema.json`
- Validated every `manifest.json` against schema and verified each referenced `source_image` exists.
- Wrote/verifed `source.sha256` checksums for each plate's source image.
- Implemented a minimal run system:
  - `generate_run_id(models, note)`
  - `start_run(plate_dir, models, note)` -> creates `runs/run-.../metrics.json`
  - `register_output(run_dir, relative_path)` -> appends outputs to `metrics.json`
- Initialized an empty, rebuildable Parquet 'ledger' scaffold in `ledger/`:
  - `plates.parquet`, `runs.parquet`, `embeddings.parquet`, `segments.parquet`
- Ran a read-only system validation report to confirm invariants:
  - 435 structured plates present
  - manifests schema-valid
  - sources present and checksummed
  - schemas + ledger present
  - run helpers callable (dry)
- Created the notebook capturing these steps: `colab/notebooks/audubon_bird_plates_setup.ipynb`.

### Session: Handoff + contract notebook

- Created a reusable, read-only "handoff" notebook intended to be the first cell(s) of any future run/analysis notebooks:
  - `colab/notebooks/audubon_bird_plates_handoff.ipynb`
- Added a lightweight project loader cell:
  - Mounts Drive
  - Resolves `DATASET_ROOT`
  - Exposes canonical paths (`PLATES_STRUCTURED`, `SCHEMA_DIR`, `LEDGER_DIR`, etc.)
  - Performs light sanity checks only (no schema validation, no checksums)
- Added a read-only structure + naming contract assertion cell that aborts on drift:
  - Plate directory naming law (`plate-###`)
  - Required subdirs (`source/`, `runs/`, `viz/`, `cache/`)
  - Required files (`manifest.json`, `source.sha256`)
  - Run directory naming law (`run-YYYYMMDD-HHMMSS-<hash>`) when runs exist
  - Ledger scaffold presence (not population)
- Added optional cells:
  - Install common analysis deps (`pillow`, `numpy`, `matplotlib`, `tqdm`)
  - Cleanup `input_image.json` files if a baseline step produced them
  - Read-only exploratory report (structure, manifest sampling, image header stats)
