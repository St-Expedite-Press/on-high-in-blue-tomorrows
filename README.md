# The Burning World

This folder is an Obsidian-friendly working vault for a book/whitepaper project: **Canonical Digital Editions Under Conditions of Variance**.

**Start here (read like a document):** [[burning_world]]

**If you want the raw thinking + technical contracts:** [[A_World_Burning/README]]

**If you want the core extraction/preprocessing contract first:** [[A_World_Burning/00_preprocessing_assay]]

---

## Directory Map (what everything is for)

- `burning_world.md` — the compiled, Obsidian-friendly whitepaper.
- `whitepaper/` — prior sectioned draft materials (front matter, sections, appendices).
- `A_World_Burning/` — working corpus + technical contracts + provenance of how the system evolved.
- `abstract_photo_workflows/` — general-purpose “feature surface area” + workflow notes that feed extraction/measurement sections.
- `appendices/` — paper-ready appendices (export-friendly copies).
- `pipeline/` — execution schedule + ingestion contract + notebook etiquette.
- `notebooks/` — working notebooks.
- [[notebooks/DATA_DICTIONARY]] — column/field dictionary for the bootstrap manifests + Parquet ledgers.

---

## Melt Rule (non-destructive)

Nothing gets deleted. When a note is “melted” into the whitepaper:

- the whitepaper section becomes the **readable argument/spec**,
- the originating note remains as **provenance**,
- the section links back to the originating note(s) under “Sources (internal)”.

---

## Repo Hygiene (GitHub)

- Keep large datasets out of Git; treat them as local/S3 assets referenced by manifests, checksums, and ledgers.
- Canonical plate IDs are `plate-###`; canonical structured sources are `plates_structured/plate-###/source/plate-###.jpg`.
