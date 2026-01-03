<!-- Auto-generated TOC-aligned file. Source of truth: A_World_Burning/26-whitepaper-skeleton.md -->

# XVI. Interfaces and Access Layers

[[whitepaper/DRAFT]] | [[whitepaper/MATERIALS_MAP]] | [[A_World_Burning/30-whitepaper-toc]] | [[A_World_Burning/28-sources-and-variant-acquisition]]

_TOC-aligned entrypoint. Master outline lives in `A_World_Burning/26-whitepaper-skeleton.md`._

---

## Draft (body text)

The manifold is one thing; interfaces are projections of it for different audiences. The project treats interfaces as access layers over canonical constraints, not as new sources of truth.

### XVI.1 Minimal access (files + manifests)

At minimum, the canon should remain legible through plain file browsing:

- plate directories,
- variant/source records,
- run outputs with manifests,
- derived ledgers as convenience, not authority.

This “no special software required” stance is part of the preservation argument.

### XVI.2 Atlas and query interfaces

Higher-level access layers include:

- an atlas (global figures, QC sheets, outlier galleries),
- retrieval and clustering notebooks (Colab-first),
- optional web viewers (including IIIF exports) for institutional adoption.

### XVI.3 Access control and licensing

Once multi-institution variance mode begins, access layers must respect:

- differing rights and credit requirements,
- restrictions on redistribution of high-res masters,
- public/private partitioning of variants.

The system can still preserve the canonical apparatus by storing checksums and manifests even when bytes cannot be redistributed.

---

## Sources (internal)

- [[A_World_Burning/28-sources-and-variant-acquisition]]
- [[A_World_Burning/33-appendix-b-filesystem-naming-run-ids]]

---

## Outline (preserved)
**Purpose:** show how different audiences actually encounter the manifold.

- XVI.1 Minimal access: file browsing + manifests
- XVI.2 Dataset atlas: global figures + per-plate QC sheets
- XVI.3 Query interfaces
  - XVI.3.a notebook-driven querying (Colab)
  - XVI.3.b CLI querying (optional)
  - XVI.3.c web viewer / IIIF export (optional but likely necessary for institutional adoption)
- XVI.3.d GraphRAG / multimodal RAG (optional; only after provenance is stable)
- XVI.3.e API surfaces (optional; must not become authoritative storage)
- XVI.4 Access control and licensing constraints (if variants come from multiple institutions)

