# SageMaker Runner Scaffold

This folder is a minimal scaffold for running repo-aligned jobs on SageMaker while preserving the append-only `runs/` contract.

## What It Does

- Runs a CPU baseline job over a plate range or shard
- Writes outputs under `plates_structured/plate-###/runs/<run_id>/`
- Writes a per-job report JSON suitable for CloudWatch or S3 archiving

## What It Does Not Do

- It does not attempt to overwrite source files
- It does not attempt to merge outputs back into an existing dataset tree automatically
- It does not require GPU

## Inputs

- A local dataset root containing `plates_structured/` and `schemas/`

## Outputs

- A new tree rooted at `--output-root` containing:
  - `plates_structured/plate-###/runs/<run_id>/metrics.json`
  - `plates_structured/plate-###/runs/<run_id>/cpu_baseline.json`
  - `reports/<run_id>/report.json`

## Local Run

```
python cpu_baseline_job.py --dataset-root /path/to/dataset --output-root /tmp/bws-out --shard-index 0 --shard-count 1
```

## SageMaker Processing Mapping

- Processing input channel downloads the dataset prefix to a local path (example: `/opt/ml/processing/input`)
- Processing output channel writes the run-only outputs to `/opt/ml/processing/output`

Invoke:

```
python cpu_baseline_job.py --dataset-root /opt/ml/processing/input --output-root /opt/ml/processing/output --shard-index 0 --shard-count 10 --run-id run-...
```

