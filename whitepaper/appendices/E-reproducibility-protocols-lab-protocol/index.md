<!-- Auto-generated TOC-aligned file. Source of truth: A_World_Burning/26-whitepaper-skeleton.md -->

# Appendix E: Reproducibility Protocols (lab protocol)

_TOC-aligned entrypoint. Master outline lives in `A_World_Burning/26-whitepaper-skeleton.md`._


**Goal:** make runs reproducible and failures legible.

- E.1 Notebook templates (CPU vs GPU) and mandatory section order
- E.2 Randomness policy
  - E.2.a explicit seeding where possible
  - E.2.b documenting nondeterminism where not
- E.3 Environment capture
  - E.3.a library versions
  - E.3.b model checkpoint identifiers
  - E.3.c hardware info (GPU name/VRAM)
- E.4 Batch execution protocol (resume-safe; append-only)
- E.5 Failure logging protocol (no silent failure; partial writes handled)
- E.6 Drift checks (rerun baseline; checksum revalidation)
- E.7 Notebook phase schedule (Audubon implementation; optional but clarifying)
  - E.7.a contract + handoff (read-only)
  - E.7.b ingestion + canonicalization (manifest/checksum/scaffold)
  - E.7.c header-only extraction (optional split: `image_header.json`)
  - E.7.d scalar pixel-pass extraction (`input_image.json`)
  - E.7.e segmentation run(s) (`segments.parquet`)
  - E.7.f embedding run(s) (`embeddings.parquet`)
  - E.7.g QC atlas generation (figures + known failures ledger)
- E.8 Hardware capability detection + adaptive batching defaults
  - E.8.a detect GPU name/VRAM and classify (CPU/T4/L4/A100-ish)
  - E.8.b per-model capability profiles (image_size, dtype, batch_size)
  - E.8.c clamp batch sizes on weaker GPUs; fail fast if GPU required
- E.9 Prompt registry discipline (if VLM captioning/tagging is used)
  - E.9.a prompt templates live in a versioned registry (e.g., `prompt_registry.yaml`)
  - E.9.b every caption/tag row stores prompt_id + prompt_version + model_id

