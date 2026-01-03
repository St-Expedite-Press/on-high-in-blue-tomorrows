<!-- Auto-generated TOC-aligned file. Source of truth: A_World_Burning/26-whitepaper-skeleton.md -->

# XII. Canonical Query and Analysis

[[whitepaper/DRAFT]] | [[whitepaper/MATERIALS_MAP]] | [[A_World_Burning/34-appendix-c-feature-extraction-inventory]] | [[A_World_Burning/33-appendix-b-filesystem-naming-run-ids]]

_TOC-aligned entrypoint. Master outline lives in `A_World_Burning/26-whitepaper-skeleton.md`._

---

## Draft (body text)

Once variants are registered and measured, canonical work becomes queryable: not as a single image to be looked at, but as a measured space to be navigated.

### XII.1 Similarity as an editorial instrument

Similarity search is not a neutral utility; it is one of the ways canon becomes operational. The project therefore treats retrieval modes as part of the canonical apparatus:

- whole-image similarity (global embeddings),
- motif/part similarity (segment embeddings),
- tile-wise “find the thing somewhere” retrieval,
- multimodal retrieval (text ↔ image) when explicitly labeled as instrumentation.

### XII.2 Clustering, outliers, and lineage graphs

Clustering and outlier mining are the methods by which variance becomes legible:

- clusters can reveal compositional families, digitization regimes, or restoration signatures;
- outliers can reveal damaged scans, unusual crops, or rare visual structures;
- lineage graphs can expose duplicate chains and derivative reproductions.

The goal is not to collapse the corpus into a single representative but to preserve difference while making it navigable.

### XII.3 Query outputs as citations

Query results become citeable only when they can be reconstructed. A citation therefore includes:

- plate identity and variant identity,
- the run(s) and model(s) that produced the embeddings/segments,
- the index artifact version (ANN build),
- the query parameters and stop conditions (if applicable).

---

## Sources (internal)

- [[A_World_Burning/34-appendix-c-feature-extraction-inventory]]
- [[A_World_Burning/33-appendix-b-filesystem-naming-run-ids]]
- [[A_World_Burning/29-model-library]]

---

## Outline (preserved)
**Purpose:** show what becomes possible once variance is registered.

- XII.1 Similarity search modes
  - XII.1.a image â†’ image retrieval (global embeddings)
  - XII.1.b segment/motif retrieval (segment embeddings)
  - XII.1.c tile-wise retrieval (â€œthing somewhere in imageâ€)
  - XII.1.d multimodal retrieval (text â†’ image; caption embeddings)
- XII.2 Clustering and multi-resolution maps
  - XII.2.a hierarchical clustering (coarseâ†’fine)
  - XII.2.b outlier mining and â€œrare modeâ€ discovery
  - XII.2.c near-duplicate and lineage graphs
- XII.3 Dataset atlas deliverables (figures + dashboards)
- XII.4 Query outputs as citations (how to cite a result reproducibly)

