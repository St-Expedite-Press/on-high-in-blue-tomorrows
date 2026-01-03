# Preprocessing & Extraction Assay - Addendum (No Edits to the Main Assay)

[[A_World_Burning/README]] | [[A_World_Burning/30-whitepaper-toc]] | [[A_World_Burning/00_preprocessing_assay]]

This file exists to capture **additional preprocessing-adjacent requirements** that surfaced during the whitepaper skeleton pass, **without modifying** `A_World_Burning/00_preprocessing_assay.md`.

If any item here is adopted, it should be treated as part of the preprocessing contract and reflected in notebook templates / validators (not as “nice-to-have” prose).

---

## A. Prompt Registry Discipline (only if VLM/captioning is used)

The extraction assay correctly treats captions/tags as weak labels, but the markdown corpus also implies a stricter operational requirement:

- Maintain a versioned prompt registry (example structure):
  - `prompts/prompt_registry.yaml`
  - entries include: `prompt_id`, `task`, `prompt_text`, `notes`, `version`, `created_at`
- Every caption/tag output must store:
  - `prompt_id`
  - `prompt_version` (or prompt hash)
  - `model_id` / checkpoint ID
  - decoding params (temperature/top_p/max_tokens, etc.)

Reason: without a registry, captions become non-reproducible “prose drift” and cannot be compared across runs.

---

## B. Canonical vs Derived Packaging (dataset distribution without undermining truth)

The storage doctrine appears across the markdown corpus and is worth making explicit in preprocessing deliverables:

- Canonical truth remains:
  - plate-centric folders + manifests + sealed runs (filesystem evidence)
- Derived packaging may be produced for consumption:
  - Parquet/Arrow bundles for facts/vectors
  - optional WebDataset shards / HDF5 for large-scale ML workflows
  - optional IIIF exports for institutional viewers
- Any derived packaging must be:
  - rebuildable from plate-local truth + run artifacts
  - accompanied by a release manifest + checksums
  - explicitly labeled as “derived packaging” (never authoritative)

---

## C. Schema and Contract Versioning (prevent silent drift)

Several markdown files imply “hard law” behavior around contracts:

- Any schema change requires an explicit version bump.
- Validation must fail hard on schema drift (no warning-only mode).
- Configurations used for runs should be hashable and versioned (config hash is mandatory; semantic versioning optional).

This should be treated as preprocessing infrastructure, not a later “paper concern”.

---

## D. Graph/Ontology Artifacts (optional in preprocessing, but constrain later meaning)

The corpus contains a formal Neptune/graph contract draft. Even if the graph database is not deployed during preprocessing, you may still want to emit **graph ingest tables** as a derived artifact so “meaning” remains downstream and reversible:

- Optional ontology files (TTL):
  - `core.ttl`, `audubon.ttl`, `burning_world.ttl`, `provenance.ttl`
- Optional ingest tables:
  - nodes/edges tables that include `source_file_path`, `run_id`, `plate_id`, checksum
- Hard requirement if graphs are used:
  - every graph node/edge must be reverse-resolvable to disk artifacts (or it does not exist)

---

## E. Notebook Schedule as Reproducibility Artifact (implementation clarity)

The markdown corpus includes a notebook-level phase schedule. If you want preprocessing to be “third-party runnable”, record the schedule as a stable artifact (even if you don’t use the exact NB numbers):

- Contract + handoff (read-only)
- Ingestion + canonicalization (manifests + checksums + scaffolding)
- Header-only extraction (optional split: `image_header.json`)
- Scalar pixel-pass extraction (`input_image.json`)
- Segmentation run(s) (`segments.parquet`)
- Embedding run(s) (`embeddings.parquet`)
- QC atlas + known failures ledger

Reason: “what counts as preprocessing” becomes citable only if the phase boundaries are explicit.

---

## F. Operational Security Note (action item)

One markdown file flags the presence of a `.env` with secrets as a risk. Independently, the current workspace also contains an `.env` at `C:\\Users\\rberr\\Desktop\\raw_photo_no_metadata\\.env`.

- Treat any shared/synced `.env` as compromised:
  - rotate/revoke credentials
  - remove from shared locations
  - add to `.gitignore` everywhere

This is not part of the dataset spec, but it is part of project survivability.
