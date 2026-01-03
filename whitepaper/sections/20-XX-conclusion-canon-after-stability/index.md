<!-- Auto-generated TOC-aligned file. Source of truth: A_World_Burning/26-whitepaper-skeleton.md -->

# XX. Conclusion: Canon After Stability

[[whitepaper/DRAFT]] | [[whitepaper/MATERIALS_MAP]] | [[A_World_Burning/26-whitepaper-skeleton]]

_TOC-aligned entrypoint. Master outline lives in `A_World_Burning/26-whitepaper-skeleton.md`._


---

## Draft (body text)

The single-image canon is a stability strategy that fails under variance. _The Burning World_ proposes a canon that survives instability by shifting the site of authority from “the image” to the apparatus that preserves variants and renders difference measurable.

Canonical status, in this model, is not a claim that one rendering is correct. It is a claim that the edition is constrained enough to be citeable, comparable, and auditable: plate identity is stable; variants are registered with provenance; runs are sealed; ledgers are derived; downstream transformations are quarantined and labeled.

The promise is simple: archives that can compute later without lying now.

---

## Outline (preserved)

- Summarize: canon as constraint; apparatus as infrastructure; variance as evidence
- Restate the promise: archives that can think later without lying now

---

## Legacy: appendix outline (preserved)

The material below was preserved from an earlier compilation and contains appendix/checklist scaffolding. The “live” appendix entrypoints are in `whitepaper/appendices/README.md`, with rendered technical content in `A_World_Burning/32-appendix-a-corpus-and-source-registry.md` through `A_World_Burning/41-appendix-j-glossary.md`.

---

## 4. Appendices (expand until nothing is implicit)

### Appendix A: Corpus and Source Registry (what the dataset is)

Rendered in: `A_World_Burning/32-appendix-a-corpus-and-source-registry.md`

**Goal:** define the population unambiguously; prevent ambiguity about what is ?in?.

- A.1 Corpus boundary statement (Audubon plates 1?435; no exceptions)
- A.2 Plate identity crosswalk
  - A.2.a plate_number ? plate_id (zero padded)
  - A.2.b title, slug, canonical filenames
- A.3 Source registry schema
  - A.3.a institution/source name
  - A.3.b acquisition method and timestamp
  - A.3.c original URL / holding identifier
  - A.3.d license/credit statement
  - A.3.e checksums + file fingerprints
- A.4 Variant registry (if multiple digitizations are added)
  - A.4.a what makes a new ?variant? distinct
  - A.4.b minimum fields for a variant to be admissible
- A.5 Exclusion log (what was rejected and why)

### Appendix B: File System, Naming Conventions, and Run IDs (disk-level ontology)

Rendered in: `A_World_Burning/33-appendix-b-filesystem-naming-run-ids.md`

**Goal:** reconstructibility; file organization as argument.

- B.1 Canonical directory map (current vs planned evolution; decision recorded)
- B.2 Naming law
  - B.2.a plate directories: `plate-###` only
  - B.2.b run directories: chosen run_id scheme; collision rules
  - B.2.c derived artifacts: `<plate_id>__<run_id>__<artifact_type>__<descriptor>.<ext>`
- B.3 Plate manifest schema (full field list + constraints)
- B.4 Run manifest schema (full field list + constraints)
- B.5 Checksum strategy
  - B.5.a `source.sha256` per plate/variant
  - B.5.b optional per-run `run.sha256`
- B.6 Validators (filesystem + schema + run sealing)
- B.7 Ledger rebuild contract (how to regenerate parquet from plate truth)

### Appendix C: Feature Extraction Inventory (complete; no omissions)

Rendered in: `A_World_Burning/34-appendix-c-feature-extraction-inventory.md`

**Goal:** exhaustive list of computed features, with what they capture and fail to capture.

This appendix should mirror the extraction inventory in `A_World_Burning/00_preprocessing_assay.md` but in a ?paper-ready? form:

- C.1 Feature families (File/container; global pixel; CV; embeddings; segmentation; OCR; captions; forensics; quality; indices)
- C.2 For each feature family, specify:
  - C.2.a purpose (what question it answers)
  - C.2.b computational regime (CPU/GPU; full-pass vs sampled vs tiled)
  - C.2.c output shape/schema (fields, dimensionality, normalization)
  - C.2.d storage location (plate-local vs ledger)
  - C.2.e known failure modes and bias
- C.3 Full enumerated inventory (copy the numbered list 1?45, verbatim or as a strict mapping)
- C.4 Versioning policy (what requires a schema bump; what is additive)

### Appendix D: Segmentation Methods and Parameters (no semantic overreach)

**Goal:** segmentation is documented as structure extraction, not meaning assignment.

- D.1 Model registry (SAM variants; Mask2Former; others)
- D.2 Input policies (resizing, tiling, cropping)
- D.3 Mask generation parameters and any filtering heuristics
- D.4 Mask representations and conversions (PNG ? RLE ? polygons)
- D.5 Rejection criteria (hard failures)
- D.6 QC metrics and dashboards
- D.7 What segmentation is explicitly not allowed to claim

### Appendix E: Reproducibility Protocols (lab protocol)

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

### Appendix F: Climate Perturbation Regimes (downstream stress definition)

**Goal:** define stress transforms precisely without contaminating documentation.

- F.1 Parameter axes and their conceptual interpretation
- F.2 Allowed transforms (examples: thermal shift, haze/ash, nocturne artifacts, contrast collapse)
- F.3 Safeguard constraints (edge preservation thresholds, semantic drift ceilings)
- F.4 Prohibitions (no new anatomy; no ?restoration?; no factual climate claims)
- F.5 Logging requirements (transform manifests; parameter capture; run IDs)

### Appendix G: Ethical and Interpretive Guardrails (formal refusals)

**Goal:** prevent automated authority and misuse.

- G.1 Non-claims (no intent inference; no definitive appearance claims)
- G.2 No restorative authority
- G.3 No biometric identity systems (general rule; face embeddings only for local alignment/blur/dedup if ever relevant)
- G.4 Weak-label policy (VLM outputs treated as weak signals; never truth)
- G.5 Institutional respect (credit, licensing, provenance)
- G.6 Security hygiene (secrets management; no `.env` leaks; threat model)

### Appendix H: Model Cards and Dependency Registry (epistemic + legal clarity)

**Goal:** list everything that could bias results or violate licensing.

- H.1 Model list by role
  - embeddings: CLIP, DINOv2, SigLIP, EVA-CLIP, etc.
  - segmentation: SAM, Mask2Former
  - OCR: Tesseract/TrOCR (if used)
  - captioning/VLM: BLIP-2, LLaVA, Qwen2-VL, Florence-2 (if used)
- H.2 For each model:
  - checkpoint ID
  - license
  - known biases
  - input preprocessing
  - output dimensionality + normalization
- H.3 Library dependency registry (Python + OS-level)
- H.4 Reproducibility warnings (where results vary across versions)
- H.5 Hardware tier expectations (if using Colab)
  - H.5.a T4 (16GB) baseline assumptions and safe model set
  - H.5.b L4 (24GB) ?sweet spot? assumptions and expanded model set
  - H.5.c A100 (40GB) optional ?maximal? set (non-blocking)
  - H.5.d dtype policy (fp16/bf16/tf32) and its implications for comparability

### Appendix I: Known Limitations and Open Questions (ledger of uncertainty)

**Goal:** show what remains unresolved, and why that matters.

- I.1 Dataset gaps (missing variants, institutional blind spots)
- I.2 Measurement brittleness (OCR, segmentation, embeddings)
- I.3 Governance questions (who sets constraints? how to revise them?)
- I.4 Evaluation questions (what benchmarks are legitimate?)
- I.5 Sustainability questions (storage cost, long-term verification)

### Appendix J: Glossary of Terms (enforced internal consistency)

**Goal:** prevent incompatible readings by defining loaded terms.

- plate, variant, run, manifest, ledger
- canonical, edition, manifold, apparatus
- provenance, immutability, auditability
- measurement vs interpretation vs transformation
- semantic drift, robustness curve, stability, failure mode

---

## 5. ?Absurdly Exhaustive? Checklists (author-facing, optional in published version)

These are working checklists; they may be moved into a private/internal appendix, but they must exist.

### 5.1 Preprocessing completeness checklist

- All plates registered; manifests valid; sources checksummed
- Baseline scalar facts extracted and stored
- Optional distributions decided (on/off) and documented
- Segmentation executed or explicitly deferred
- Embeddings executed (global; optional segment/tile)
- Ledgers built and rebuildable from plate-local truth
- QC atlas generated; known failures logged

### 5.2 ?No silent failure? checklist (per notebook/run)

- Structure assertion ran before any compute
- Config declared and hashed
- All outputs registered in manifest
- Post-run validation succeeded
- Ledger sync updated
- Run sealed (status complete + checksums recorded)

### 5.3 Citation checklist (for scholarship)

- If citing a source variant: include source registry ID + checksum + access date
- If citing a derived measurement: include run_id + config hash + model IDs + ledger version
- If citing a transformation: include transform run_id + parameter set + safeguard metrics
