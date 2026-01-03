# A_World_Burning — Working Corpus + Whitepaper Materials

This directory is the **single flat workspace** for _The Burning World_: planning notes, technical contracts, and whitepaper scaffolding. Nothing is thrown away; later documents consolidate earlier ones without deleting them.

If you only read a few things, start here:

- Whitepaper seed (intro + ToC): [[whitepaper/White Paper I]] (`..\whitepaper\White Paper I.md`)
- Whitepaper master outline (executable ToC + appendix pointers): [[26-whitepaper-skeleton]] (`26-whitepaper-skeleton.md`)
- Whitepaper ToC map (Obsidian-friendly links): [[30-whitepaper-toc]] (`30-whitepaper-toc.md`)
- Whitepaper compiled draft (paper-shaped, Obsidian-friendly): [[42-whitepaper-draft]] (`42-whitepaper-draft.md`)
- Preprocessing/extraction inventory (the "do we have everything?" list): [[00_preprocessing_assay]] (`00_preprocessing_assay.md`)
- Addenda that were discovered later (kept separate to avoid disturbing the main assay): [[00_preprocessing_assay_addendum]] (`00_preprocessing_assay_addendum.md`)
- Filled appendices (paper-ready technical specifications):
  - Appendix A (corpus + source registry): [[32-appendix-a-corpus-and-source-registry]] (`32-appendix-a-corpus-and-source-registry.md`)
  - Appendix B (filesystem + run IDs): [[33-appendix-b-filesystem-naming-run-ids]] (`33-appendix-b-filesystem-naming-run-ids.md`)
  - Appendix C (feature extraction inventory): [[34-appendix-c-feature-extraction-inventory]] (`34-appendix-c-feature-extraction-inventory.md`)
- Model library (embedding/segmentation registry + alias hygiene): [[29-model-library]] (`29-model-library.md`)
- Source/variant acquisition discipline (how to go get variants without losing provenance): [[28-sources-and-variant-acquisition]] (`28-sources-and-variant-acquisition.md`)

---

## How This Folder Is Organized (without subfolders)

The file prefixes are **chronological / iterative**, not “finished draft order”.

There are three “layers” of material:

1. **Core contracts (canonical constraints)**  
   These are the closest to “finished law” and should change only with explicit version bumps.
2. **Paper-facing specifications (appendix-grade)**  
   These turn the contracts into a citeable methods apparatus.
3. **Working notes / ideation**  
   These are the raw thinking that produced the contracts; they remain valuable and are not deleted.

---

## Core Contracts (treat as law)

- [[00_preprocessing_assay]] - exhaustive "what must be acquired/extracted/derived" through preprocessing
- [[00_preprocessing_assay_addendum]] - no-edit addenda (prompt registry, packaging, schema versioning, security hygiene)
- [[33-appendix-b-filesystem-naming-run-ids]] - disk ontology, run sealing, naming law, ledger rebuild contract
- [[28-sources-and-variant-acquisition]] - variant/source registry discipline (variance mode)
- [[29-model-library]] - model registry + pinning rules + license hygiene

---

## Whitepaper Materials

- [[whitepaper/White Paper I]] - seed draft (introduction + ToC)
- [[26-whitepaper-skeleton]] - expanded outline (argument + spec + infrastructure guide)
- [[30-whitepaper-toc]] - Obsidian-friendly ToC map (links into this directory)
- [[42-whitepaper-draft]] - compiled, paper-shaped draft (read in one file)

---

## Filled Appendices (paper-ready)

- [[32-appendix-a-corpus-and-source-registry]] - Appendix A
- [[33-appendix-b-filesystem-naming-run-ids]] - Appendix B
- [[34-appendix-c-feature-extraction-inventory]] - Appendix C

## Drafted Appendices (D-J; ready to expand)

- [[35-appendix-d-segmentation-methods-and-parameters]] - Appendix D
- [[36-appendix-e-reproducibility-protocols]] - Appendix E
- [[37-appendix-f-climate-perturbation-regimes]] - Appendix F
- [[38-appendix-g-ethical-and-interpretive-guardrails]] - Appendix G
- [[39-appendix-h-model-cards-and-dependency-registry]] - Appendix H
- [[40-appendix-i-known-limitations-and-open-questions]] - Appendix I
- [[41-appendix-j-glossary]] - Appendix J

---

## Notebooks (bootstrap ground truth)

These two are treated as “do not edit except deliberately” baseline artifacts:

- `notebooks/audubon_bird_plates_setup.ipynb`
- `notebooks/audubon_bird_plates_handoff.ipynb`

Note: `notebooks.ipnyb` exists but is empty; ignore unless you intentionally use it as a placeholder.

---

## Current Canon (what is true right now)

- Canonical identifiers are `plate-###` (zero-padded).
- In the canonical structured layer, the source image is `source/plate-###.jpg`.
- `runs/` is append-only; derived outputs only ever appear under a run directory.
- Schema contract lives under `schemas/`, and ledgers under `ledger/`.

Next safe computation:

- CPU baseline run (`cpu-baseline-v1`) to produce first comparable measurements without ML inference.

---

## Ontology Work

- OWL sketch (planning, no serialization): [[43-owl-ontology-sketch]] (`43-owl-ontology-sketch.md`)

---

## Working Notes (kept, not erased)

These are the “concept development archive”. They are not obsolete; they are provenance for the project’s conceptual evolution:

- Architecture + planning: [[01_audubon_dual_ledger]], [[02_first_extract_plan]], [[07_the_evolving_data_plan]], [[23-phases-and-schedules]]
- Models + workflows: [[04_sane_model_roster]], [[05_cost_optimization]], [[06_faster_cheaper_shittier_maybe_better]], [[21-more-on-the-model-thing]], [[24-etiquette]]
- "Strange" embeddings + probes: [[14-strangest-of-embeddings]], [[27-strange-models-compendium]]
- Big picture / publication framing: [[19-the-big-one]], [[20-a-real-paper]], [[25-reel-it-in]]
- Sources/bibliography: [[31-sources-and-instruments-bibliography]]

---

## Obsidian Rendering Notes (practical)

- Keep code fenced (```python / ```json / etc.) so it doesn’t turn into headings.
- Prefer markdown tables with explicit header separators; Appendices A–C and the model library follow this.
- Use the ToC map (`30-whitepaper-toc.md`) as the “graph spine” in Obsidian: it links sections and appendices cleanly.
