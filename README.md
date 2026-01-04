# The Burning World

An Obsidian-friendly working vault for a book/whitepaper project: **Canonical Digital Editions Under Conditions of Variance**.

## Start Here

- Read the compiled whitepaper: `burning_world.md` (Obsidian link: `[[burning_world]]`)
- Jump to the working corpus + contracts: `A_World_Burning/README.md` (Obsidian link: `[[A_World_Burning/README]]`)

## Reading Surfaces (What’s “Primary”)

- `burning_world.md` — the current compiled whitepaper (single-file reading surface).
- `whitepaper/DRAFT.md` — sectioned draft version of the same project (better for incremental editing).
- `whitepaper/MATERIALS_MAP.md` — crosswalk from the working corpus into the section structure.

## Directory Map (What Everything Is For)

- `A_World_Burning/` — working corpus + technical contracts + provenance notes (the “raw thinking” layer).
- `whitepaper/` — book/whitepaper structure (front matter, sections, appendices, compiled draft).
- `appendices/` — export-friendly appendix copies (paper-ready technical specs).
- `pipeline/` — execution schedule + ingestion contract + notebook etiquette + SageMaker scaffolds.
- `notebooks/` — runnable notebooks + data dictionary + pinned requirements.
- `abstract_photo_workflows/` — general-purpose workflow notes and “feature surface area” inventory.

## Key Contracts (If You’re Implementing, Not Just Reading)

- Preprocessing/extraction “do we have everything?” list: `A_World_Burning/00_preprocessing_assay.md`
- Source-of-truth outline (maximal completeness): `A_World_Burning/26-whitepaper-skeleton.md`
- Clickable ToC map: `A_World_Burning/30-whitepaper-toc.md`
- Appendices (canonical specs, A–J): `A_World_Burning/32-appendix-a-corpus-and-source-registry.md` through `A_World_Burning/41-appendix-j-glossary.md`

## Notebooks (Dataset Bootstrap)

- Data dictionary for the on-disk contract: `notebooks/DATA_DICTIONARY.md`
- Setup notebook: `notebooks/audubon_bird_plates_setup.ipynb`
- Read-only handoff notebook: `notebooks/audubon_bird_plates_handoff.ipynb`
- Minimal pinned deps for notebook execution: `notebooks/requirements.txt`

## Running Without Notebooks

- Install dependencies for the CPU baseline job: `python -m pip install -r pipeline/sagemaker/requirements.txt`
- CPU baseline job (module): `python -m pipeline.sagemaker.cpu_baseline_job --dataset-root <DATASET_ROOT> --output-root <OUTPUT_ROOT>`
- PowerShell wrapper: `scripts/run_cpu_baseline.ps1 -DatasetRoot <DATASET_ROOT> -OutputRoot <OUTPUT_ROOT> -ShardIndex 0 -ShardCount 1 -SkipIfPresent`
- Normalize old run reports (adds `dataset_root`/`input_root` alias if missing): `python -m pipeline.tools.normalize_run_reports <PATH_TO_REPORT_OR_RUN_OUTPUT_DIR>`

## Obsidian Notes

- This repo is designed to be opened as an Obsidian vault.
- Most navigation is via `[[wikilinks]]` between notes and sections.

## Repo Hygiene

- Local secrets/config live in `.env` and are intentionally not committed.
