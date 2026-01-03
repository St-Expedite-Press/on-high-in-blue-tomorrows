<!-- Auto-generated TOC-aligned file. Source of truth: A_World_Burning/26-whitepaper-skeleton.md -->

# XV. Infrastructure and Storage Design

[[whitepaper/DRAFT]] | [[whitepaper/MATERIALS_MAP]] | [[A_World_Burning/33-appendix-b-filesystem-naming-run-ids]] | [[A_World_Burning/34-appendix-c-feature-extraction-inventory]]

_TOC-aligned entrypoint. Master outline lives in `A_World_Burning/26-whitepaper-skeleton.md`._

---

## Draft (body text)

Infrastructure is not ancillary to the argument; it is where canon becomes real. The storage design encodes what counts as evidence, what counts as measurement, and what counts as interpretation.

### XV.1 Storage doctrine (the canonical “layer split”)

This project enforces a practical doctrine:

- **Files hold artifacts** (images, masks, previews, run outputs).
- **Parquet holds facts** (tabular measurements, manifests-as-rows, indexes-as-rows).
- **Vectors hold perception** (embeddings, segment vectors, ANN indices).
- **Graphs hold meaning** (optional, derived interpretive relations; never primary truth).

The purpose is to keep the documentary layer reversible: you can always resolve a ledger row back to a file path and a run manifest.

### XV.2 Disk ontology and schema discipline

The disk and schema contracts make the system reconstructible:

- stable directory layout and naming law (Appendix B),
- fixed schemas for ledgers and manifests (Appendix B/C),
- explicit model/dependency registry for anything that can change results (Appendix H).

### XV.3 Long-term preservation

Preservation is treated as a design input:

- checksums and periodic revalidation,
- open, inspectable formats where possible (JSON, PNG/SVG, Parquet),
- rebuildability from plate-local truth + sealed run artifacts.

---

## Sources (internal)

- [[A_World_Burning/33-appendix-b-filesystem-naming-run-ids]]
- [[A_World_Burning/34-appendix-c-feature-extraction-inventory]]
- [[A_World_Burning/39-appendix-h-model-cards-and-dependency-registry]]

---

## Outline (preserved)
**Purpose:** specify the storage doctrine and the concrete artifact graph.

- XV.1 Storage doctrine (must be repeated verbatim in the final whitepaper)
  - Files hold artifacts
  - Parquet holds facts
  - Vectors hold perception
  - Graphs hold meaning
- XV.2 Filesystem contract (Appendix B)
- XV.3 Tabular schemas (Appendix C + Appendix H)
- XV.4 Vector storage + compression (float16, PQ) and index versioning
- XV.5 Optional graph layer (Neptune) as derived meaning space
  - XV.5.a nodes/edges ontology
  - XV.5.b ?reverse resolution to disk? requirement
  - XV.5.c graph is derived truth, not primary truth
  - XV.5.d supported graph modes (document which is used)
    - property graph (Gremlin traversal)
    - RDF/OWL (SPARQL queries; ontology reasoning)
  - XV.5.e ontology artifacts (if used)
    - `core.ttl`
    - `audubon.ttl`
    - `burning_world.ttl`
    - `provenance.ttl`
  - XV.5.f bulk ingestion artifacts (if used)
    - nodes/edges tables (CSV/Parquet) with `source_file_path`, `run_id`, `plate_id`, checksum
    - load properties and mapping
  - XV.5.g ingest rejection rules (museum-grade)
    - any node/edge that cannot be reverse-resolved to disk rejects the load
    - any checksum mismatch rejects the load
  - XV.5.h ingest tables vs live DB dependency (prefer tables; DB is optional)
- XV.6 Long-term preservation strategy
  - XV.6.a format choices (Parquet/JSON/PNG/SVG)
  - XV.6.b checksums and periodic revalidation
  - XV.6.c reproducible rebuild from plate truth + run artifacts
- XV.7 Schema and contract versioning (no silent drift)
  - XV.7.a schema version bump rules (when required; how recorded)
  - XV.7.b configuration versioning (config hash; semantic version, if adopted)
  - XV.7.c ?no untracked schema changes? enforcement (validation hard-fails)
- XV.8 Distribution and interchange (optional but adoption-critical)
  - XV.8.a Parquet/Arrow as the canonical fact transport
  - XV.8.b WebDataset/HDF5/TFRecord only as derived packaging (never canonical truth)
  - XV.8.c IIIF export for institutional interoperability
  - XV.8.d Export/import invariants (IDs, checksums, and provenance survive round trips)

