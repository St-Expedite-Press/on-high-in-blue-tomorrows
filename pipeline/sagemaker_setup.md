# SageMaker Setup (Repo-Aligned)

This note describes how to run this repo’s append-only “runs” model on SageMaker without breaking custody, naming, or reproducibility.

## Target Runtime Model

- Storage: S3 is the authoritative filesystem.
- Compute: a stateless job reads inputs and writes new run outputs.
- Idempotency: re-running a job does not overwrite prior artifacts; it either skips or produces a new `run_id`.

## S3 Layout (recommended)

Choose a single dataset prefix:

- `s3://<bucket>/<prefix>/`

Under it, mirror the canonical contract:

- `plates_structured/plate-###/manifest.json`
- `plates_structured/plate-###/source/plate-###.jpg`
- `plates_structured/plate-###/source.sha256`
- `plates_structured/plate-###/runs/run-YYYYMMDD-HHMMSS-<hash>/metrics.json`
- `plates_structured/plate-###/runs/run-.../<artifact files>`
- `schemas/*.schema.json`
- `ledger/*.parquet`

## IAM (minimum permissions)

Execution role must allow:

- `s3:GetObject` on inputs (`plates_structured/**`, `schemas/**`, `ledger/**`)
- `s3:PutObject` on outputs (`plates_structured/**/runs/**`, `schemas/**` if writing new schemas, `ledger/**` if writing derived ledgers)
- `s3:ListBucket` for the dataset prefix
- `logs:CreateLogGroup`, `logs:CreateLogStream`, `logs:PutLogEvents`

## Container Strategy

Use a single container image for CPU-only runs.

Recommended approach:

- Base: official Python image compatible with SageMaker Processing
- Install: `notebooks/requirements.txt` plus any run-specific extras
- Entrypoint: a single CLI script that accepts S3 paths and a plate shard

Inputs via environment variables:

- `BWS_DATASET_S3_PREFIX=s3://<bucket>/<prefix>`
- `BWS_MODELS=cpu-baseline-v1`
- `BWS_PLATE_SHARD=0/10` (or similar sharding)

## Job Type

Use a SageMaker Processing Job for “map over plates” runs:

- Each job processes a shard of plates.
- Each job writes run outputs under each plate’s `runs/` directory.
- Each job writes a shard report to `s3://.../reports/run-.../shard-...json`.

## Run ID Policy

Make `run_id` globally unique and sortable:

- `run-YYYYMMDD-HHMMSS-<hash>`

If running multiple shards, use a shared `run_id` across shards by passing it in:

- `BWS_RUN_ID=run-...`

If `BWS_RUN_ID` is not provided, each shard generates its own `run_id`.

## CPU Baseline on SageMaker (what changes)

Local notebooks write into a local folder.
On SageMaker:

- Read `manifest.json` and `source/plate-###.jpg` from S3
- Write `runs/<run_id>/cpu_baseline.json` to S3
- Update `runs/<run_id>/metrics.json` in S3

Avoid concurrent writes to the same `metrics.json` from multiple workers.
Options:

- One plate per worker (safe)
- One shard per worker, but write `metrics.json` once per plate (safe if only one worker touches each plate)

## Validation

Validation stays local to the job:

- Load JSON Schemas from `schemas/`
- Validate every written JSON artifact before uploading
- Fail the job on the first schema violation

## Ledger Updates

Treat ledgers as derived batch artifacts:

- `ledger/runs.parquet` and `ledger/plates.parquet` can be rebuilt from `plates_structured/`
- Update ledgers in a dedicated “ledger build” job, not in every run job

## What Not To Do

- Do not store embedding vectors or per-tile arrays as triples in RDF.
- Do not overwrite `source/` or `source.sha256`.
- Do not write “ad-hoc” outputs outside `runs/<run_id>/`.
