# The Burning World

Working repository for a book/whitepaper project: **Canonical Digital Editions Under Conditions of Variance**.

This repo is GitHub-first Markdown (standard links); it also reads cleanly in Obsidian if you use it locally.

## Start Here

- Read the compiled whitepaper (single-file reading surface): [burning_world.md](burning_world.md)
- Read/edit the sectioned draft: [whitepaper/DRAFT.md](whitepaper/DRAFT.md)
- Jump into the working corpus + contracts: [A_World_Burning/README.md](A_World_Burning/README.md)
- Governance / loose ends checklist: [GOVERNANCE_CHECKLIST.md](GOVERNANCE_CHECKLIST.md)

## Reading Surfaces (What's Primary)

- [burning_world.md](burning_world.md) - compiled whitepaper (single-file reading surface).
- [whitepaper/DRAFT.md](whitepaper/DRAFT.md) - sectioned draft version (best for incremental editing).
- [whitepaper/MATERIALS_MAP.md](whitepaper/MATERIALS_MAP.md) - crosswalk from working corpus into section structure.

## Directory Map (What Everything Is For)

- `A_World_Burning/` - working corpus + technical contracts + provenance notes (the "raw thinking" layer).
- `whitepaper/` - book/whitepaper structure (front matter, sections, appendices, compiled draft).
- `appendices/` - export-friendly appendix copies (paper-ready technical specs).
- `pipeline/` - execution schedule + ingestion contract + notebook etiquette + SageMaker scaffolds.
- `pipeline/reports/` - run write-ups (reference artifacts).
- `notebooks/` - runnable notebooks + data dictionary + pinned requirements.
- `abstract_photo_workflows/` - general-purpose workflow notes and "feature surface area" inventory.

## Key Contracts (If You're Implementing, Not Just Reading)

- Ingestion contract (run semantics, invariants): [pipeline/ingestion_contract.md](pipeline/ingestion_contract.md)
- Preprocessing/extraction "do we have everything?" list: [A_World_Burning/00_preprocessing_assay.md](A_World_Burning/00_preprocessing_assay.md)
- Source-of-truth outline (maximal completeness): [A_World_Burning/26-whitepaper-skeleton.md](A_World_Burning/26-whitepaper-skeleton.md)
- Clickable ToC map: [A_World_Burning/30-whitepaper-toc.md](A_World_Burning/30-whitepaper-toc.md)
- OWL ontology sketch (planning inventory): [A_World_Burning/43-owl-ontology-sketch.md](A_World_Burning/43-owl-ontology-sketch.md)
- Model cards + dependency registry (Appendix H): [appendices/H_model_cards_and_dependency_registry.md](appendices/H_model_cards_and_dependency_registry.md)

## Pipeline Docs

- Execution schedule: [pipeline/execution_schedule.md](pipeline/execution_schedule.md)
- Notebook etiquette (run discipline): [pipeline/notebook_etiquette.md](pipeline/notebook_etiquette.md)
- SageMaker-style job scaffolding: [pipeline/sagemaker_setup.md](pipeline/sagemaker_setup.md)

## Appendices

- Whitepaper appendices index: [whitepaper/appendices/README.md](whitepaper/appendices/README.md)
- Export-friendly appendix copies (A–J): `appendices/`

## Notebooks (Dataset Bootstrap)

- Data dictionary for the on-disk contract: [notebooks/DATA_DICTIONARY.md](notebooks/DATA_DICTIONARY.md)
- Setup notebook: `notebooks/audubon_bird_plates_setup.ipynb`
- Read-only handoff notebook: `notebooks/audubon_bird_plates_handoff.ipynb`
- Minimal pinned deps for notebook execution: `notebooks/requirements.txt`

## Running Without Notebooks

- Install dependencies for the jobs: `python -m pip install -r pipeline/sagemaker/requirements.txt`
- CPU baseline job (module): `python -m pipeline.sagemaker.cpu_baseline_job --dataset-root <DATASET_ROOT> --output-root <OUTPUT_ROOT>`
- Segmentation job (Otsu luma; module): `python -m pipeline.sagemaker.segmentation_otsu_job --dataset-root <DATASET_ROOT> --output-root <OUTPUT_ROOT> --max-dim 1024`
- Report normalizer (adds `dataset_root`/`input_root` alias if missing): `python -m pipeline.tools.normalize_run_reports <PATH_TO_REPORT_OR_RUN_OUTPUT_DIR>`
- PowerShell wrappers: `scripts/run_cpu_baseline.ps1`, `scripts/run_segmentation_otsu.ps1`

## Reports

- Reports index: [pipeline/reports/README.md](pipeline/reports/README.md)

## Repo Hygiene

- Local secrets/config live in `.env` and are intentionally not committed.
