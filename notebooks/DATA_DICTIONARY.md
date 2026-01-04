# Data Dictionary (Audubon Bird Plates - bootstrap v0 + run artifacts v0)

This data dictionary documents the on-disk contract created by `notebooks/audubon_bird_plates_setup.ipynb` and asserted by `notebooks/audubon_bird_plates_handoff.ipynb`, plus the first derived run artifacts produced by the baseline jobs.

Scope (v0):

- Raw ingestion index (input): `data.json` (filenames may include slugs; canonicalization happens in `plates_structured/`)
- Per-plate manifest: `plates_structured/<plate_id>/manifest.json`
- Per-plate source checksum: `plates_structured/<plate_id>/source.sha256`
- Per-run manifest: `plates_structured/<plate_id>/runs/<run_id>/metrics.json`
- Per-run artifacts (examples):
  - CPU baseline: `cpu_baseline.json`
  - Segmentation (Otsu luma): `segmentation.json`, `segmentation_mask.png`
- Run registry report: `<OUTPUT_ROOT>/reports/<run_id>/report.json`
- (Planned) derived ledgers: `ledger/{plates,runs,embeddings,segments}.parquet`

---

## Identifiers

| Name | Type | Constraint | Meaning |
|---|---|---|---|
| `plate_id` | string | `^plate-[0-9]{3}$` | Canonical plate identifier (e.g. `plate-001`). |
| `run_id` | string | `^run-[0-9]{8}-[0-9]{6}-[a-f0-9]{8}$` | Canonical run identifier (e.g. `run-20260101-235959-1a2b3c4d`). |
| `segment_id` | string | (implementation-defined) | Stable identifier for a segment within a run (unique at least within `(run_id, plate_id)`). |

---

## Plate Manifest (`manifest.json`)

Location: `plates_structured/<plate_id>/manifest.json`

Schema writer: `notebooks/audubon_bird_plates_setup.ipynb` (`PLATE_MANIFEST_SCHEMA`)

Rules:

- `additionalProperties: false` (unknown fields are rejected)
- `plate_id` must match the parent directory name
- `source_image` is a path relative to the plate directory (bootstrap expects one immutable source file under `source/`)

| Field | Type | Required | Constraints | Description |
|---|---|---:|---|---|
| `plate_id` | string | yes | `^plate-[0-9]{3}$` | Plate identifier. |
| `plate_number` | integer | yes | `1..435` | Plate ordinal number. |
| `title` | string | yes |  | Human title for the plate. |
| `slug` | string | yes |  | URL/filename-safe title surrogate. |
| `source_image` | string | yes |  | Relative path to the canonical source image file (e.g. `source/plate-001.jpg`). |
| `download_url` | string \| null | no |  | Original acquisition URL (if available). |
| `license` | string | no |  | Rights/usage string (if known). |
| `created_at` | string | no | `date-time` | Manifest creation timestamp (ISO 8601). |

---

## Source Checksum (`source.sha256`)

Location: `plates_structured/<plate_id>/source.sha256`

Meaning:

- SHA-256 hex digest of the immutable source bytes for the plate.
- Used to detect drift/corruption. A valid system never rewrites the source file; corrections are new variants/runs.

---

## Run Manifest (`metrics.json`)

Location: `plates_structured/<plate_id>/runs/<run_id>/metrics.json`

Schema writer: `notebooks/audubon_bird_plates_setup.ipynb` (`RUN_MANIFEST_SCHEMA`)

Notes:

- The bootstrap notebooks name the run manifest `metrics.json` (not `run.manifest.json`).
- `outputs` is an append-only registry of artifacts, stored as paths relative to the run directory.

| Field | Type | Required | Constraints | Description |
|---|---|---:|---|---|
| `run_id` | string | yes |  | Run identifier. |
| `plate_id` | string | yes |  | Plate identifier (should equal the parent `plate-###`). |
| `timestamp` | string | yes | `date-time` | Run timestamp (ISO 8601, UTC recommended). |
| `models` | string[] | yes |  | Method/model identifiers used by the run. |
| `outputs` | string[] | yes |  | Relative paths to output artifacts produced by this run. |
| `notes` | string \| null | no |  | Optional run note. |

---

## Run Registry Report (`report.json`)

Location: `<OUTPUT_ROOT>/reports/<run_id>/report.json`

Purpose:

- Canonical run registry entry and summary counters for the run.
- Discovery currently happens by enumerating `reports/`.

Required fields (v0):

- `run_id`, `timestamp`
- `dataset_root` (canonical) and `input_root` (alias)
- `output_root`
- `shard_index`, `shard_count`
- `plates_total`, `plates_selected`, `plates_processed`, `plates_skipped`
- `decode_failures`, `schema_failures`
- `errors_sample` (bounded list)

---

## CPU Baseline Artifact (`cpu_baseline.json`)

Location: `plates_structured/<plate_id>/runs/<run_id>/cpu_baseline.json`

Writers:

- Notebook: `notebooks/cpu_baseline_sagemaker_style.ipynb`
- CLI job: `python -m pipeline.sagemaker.cpu_baseline_job ...`

Purpose:

- Cheap, reproducible, non-ML features for QC, drift detection, and provenance-first comparisons.

Key fields:

- `plate_id`, `run_id`, `timestamp`, `source_image`
- `source_file` (bytes, extension/format, sha256; may include ICC/EXIF/JPEG forensics when available)
- `geometry` (width/height/megapixels/aspect ratio/mode)
- `tiling` (tile_size_px + computed tile counts; informational)
- `pixel_stats` (histograms + derived stats, entropy, Laplacian variance)
- `hashes` (`ahash`, `dhash`, `phash`)

---

## Segmentation Artifacts (Otsu luma v0)

Location:

- `plates_structured/<plate_id>/runs/<run_id>/segmentation.json`
- `plates_structured/<plate_id>/runs/<run_id>/segmentation_mask.png`

Writers:

- Notebook: `notebooks/segmentation_otsu_sagemaker_style.ipynb`
- CLI job: `python -m pipeline.sagemaker.segmentation_otsu_job ...`

Notes:

- This segmentation is a measurement-layer artifact: derived, append-only, and never overwrites sources.
- The mask is intentionally downsampled (see `mask_geometry`) and is primarily a QC/routing signal, not a final semantic segmentation.

---

## Ledgers (Parquet schemas) (planned)

These files are derived views. They must be rebuildable from `plates_structured/` manifests and run artifacts.

### `ledger/plates.parquet`

| Column | Type | Description |
|---|---|---|
| `plate_id` | string | Plate identifier. |
| `plate_number` | int16 | Plate ordinal number. |
| `title` | string | Plate title (from `manifest.json`). |
| `source_checksum` | string | SHA-256 hex digest of the plate's immutable source bytes (from `source.sha256`). |

Keys:

- Primary key (semantic): `plate_id`

### `ledger/runs.parquet`

| Column | Type | Description |
|---|---|---|
| `run_id` | string | Run identifier. |
| `plate_id` | string | Plate identifier (foreign key to `plates.parquet`). |
| `timestamp` | timestamp[ms, tz=UTC] | Run timestamp. |
| `models` | list<string> | Models used in the run. |
| `notes` | string | Run notes (may be empty when absent). |

Keys:

- Primary key (semantic): `run_id`
- Foreign key (semantic): `plate_id` -> `ledger/plates.parquet.plate_id`

### `ledger/embeddings.parquet`

| Column | Type | Description |
|---|---|---|
| `run_id` | string | Run identifier (foreign key). |
| `plate_id` | string | Plate identifier (foreign key). |
| `model` | string | Embedding model identifier (e.g. CLIP variant). |
| `vector` | list<float32> | Embedding vector values. |

Recommended key:

- `(run_id, plate_id, model)`

### `ledger/segments.parquet`

| Column | Type | Description |
|---|---|---|
| `run_id` | string | Run identifier (foreign key). |
| `plate_id` | string | Plate identifier (foreign key). |
| `segment_id` | string | Segment identifier (unique within a run+plate). |
| `area_ratio` | float32 | Segment area / full image area (0..1). |

Recommended key:

- `(run_id, plate_id, segment_id)`
