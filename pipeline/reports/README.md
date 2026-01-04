# Pipeline Reports

These are reference artifacts documenting exploratory runs (what was executed, what was produced, what it means, and what it does *not* mean).

## Current Reports

- CPU baseline: `pipeline/reports/exploratory_cpu_baseline_run-20260104-043258-877a06a6.md`
- Otsu luma segmentation: `pipeline/reports/exploratory_segmentation_otsu_run-20260104-053757-923adfbe.md`

## Conventions

- Reports describe *run outputs* under a run output root like `.../_RUN_OUTPUT/`.
- The core dataset (`plates_structured/<plate_id>/source/...`) is treated as immutable; derived artifacts are append-only under `plates_structured/<plate_id>/runs/<run_id>/`.
