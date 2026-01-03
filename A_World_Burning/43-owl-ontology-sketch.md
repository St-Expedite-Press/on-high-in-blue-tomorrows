# 43 — OWL Ontology Sketch (v0)

This file sketches an OWL (RDF/OWL) ontology for this repo and dataset.
It is intentionally a planning artifact: names, layers, and modeling decisions.
No serialization yet.

## Goal

Represent the corpus as a knowledge graph where:

- Identity is stable (`Plate`, `CorpusRelease`)
- Provenance is explicit (`Run`, `FileArtifact`, `Agent`)
- Measurements and interpretations never overwrite immutables
- Heavy numeric payloads stay in files (Parquet/JSON/PNG/NPY), referenced by URI + checksum

## Design Principles

1. Triples encode relationships and provenance; arrays/rasters stay out-of-graph.
2. Canon is a release-scoped claim: the same plate can have multiple variants without conflict.
3. “Place” is the spatial substrate that derived artifacts reference.
4. All computed outputs are append-only, run-scoped artifacts.
5. Validation constraints live in SHACL and JSON Schema; OWL is for semantics, not policing filesystems.

## External Alignments (recommended, optional)

- PROV-O (`prov:`) for activities, agents, derivations
- Dublin Core (`dcterms:`) for titles, identifiers, bibliographic metadata
- DCAT (`dcat:`) for dataset/catalog concepts if publishing externally

## Upper-Level (Layer 0)

These are the minimal top concepts that every other layer depends on.

### Core Classes

- `bws:CorpusRelease`
- `bws:Plate`
- `bws:PlateVariant`
- `bws:Place`
- `bws:Run`
- `bws:FileArtifact`
- `bws:Schema`
- `bws:Model`
- `bws:FeatureFamily`
- `bws:Measurement`
- `bws:Region`
- `bws:Assertion`

### Key “Jumping Off Points”

- `CorpusRelease` → enumerate plates, runs, schemas, ledgers
- `Plate` → variants, place, runs, assertions
- `Run` → models/config, outputs, validation status
- `FeatureFamily` → what can be measured vs what was measured
- `Schema` → what governs writes and validation

## Layering (recommended 4 layers)

### Layer 1: Corpus Identity

Stable identity and catalog facts.

- `Plate` is the stable work-level entity (`plate-001`).
- `PlateVariant` is a specific digitization/source lineage.
- `CorpusRelease` is a versioned bundle of claims about which variants are canonical.

Relations:

- `CorpusRelease bws:hasPlate Plate`
- `Plate bws:hasVariant PlateVariant`
- `CorpusRelease bws:declaresCanonicalVariant PlateVariant`

### Layer 2: Evidence & Files

Everything that exists on disk or S3 is a `FileArtifact`.

Data properties (typical):

- `bws:relativePath` (for repo-local references)
- `bws:uri` (for S3/HTTP)
- `bws:sha256`
- `bws:mediaType`
- `bws:bytes`

Relations:

- `PlateVariant bws:hasSourceImage FileArtifact`
- `Plate bws:hasManifest FileArtifact`
- `FileArtifact bws:conformsTo Schema`

### Layer 3: Process & Runs

Runs are append-only computational events.

Relations:

- `Run bws:aboutPlate Plate`
- `Run bws:usesModel Model`
- `Run bws:generates FileArtifact`
- `Run bws:usesInput FileArtifact`
- `Run bws:hasMeasurement Measurement`

Recommended: model run configuration as a `FileArtifact` (JSON) and link it with `bws:usesInput`.

### Layer 4: Interpretation & Assertions

This is where “meaning” lives, never in the immutable substrate.

- Segment labels, taxonomies, “foreground vs margin” decisions, historical claims
- Confidence and decision basis are first-class (`Assertion`)

Relations:

- `Assertion bws:aboutPlate Plate`
- `Assertion bws:hasEvidence FileArtifact`
- `Assertion bws:confidenceLiteral xsd:decimal`

## Place Model (spatial substrate)

`Place` is the coordinate system that downstream artifacts reference.

Recommended immutables (mirrors `place.json`):

- orientation: rotation, flips
- geometry: width, height, aspect ratio
- tiling: tile size, tile grid
- bounds: image bounds, content bounds, confidence state
- scale: physical dimensions when known

Relations:

- `Plate bws:hasPlace Place`
- `Region bws:inPlace Place`
- `Region bws:describedBy FileArtifact` (mask polygons, bbox JSON, etc.)

## Regions & Segments

`Region` is a spatial subset of a `Place`.

Representations should be file-backed:

- bbox JSON
- polygon GeoJSON
- raster mask PNG
- vector contours

Relations:

- `Run bws:generates Region`
- `Region bws:describedBy FileArtifact`
- `Region bws:hasMeasurement Measurement`

## Measurements & Feature Families

Measurements are always:

- run-scoped
- feature-family typed
- file-backed when large

Relations:

- `Measurement bws:inFamily FeatureFamily`
- `Measurement bws:computedInRun Run`
- `Measurement bws:hasValueLiteral` (for scalars)
- `Measurement bws:hasValueFile FileArtifact` (for histograms/vectors)

Suggested feature families:

- `bws:CpuBaseline` (container facts, geometry, histograms, entropy, hashes)
- `bws:BoundaryCandidate`
- `bws:Segmentation`
- `bws:Embedding`
- `bws:TextExtraction`

## OWL Reasoning Profile

Default recommendation:

- OWL 2 RL (or “OWL-lite + SHACL”) to keep costs predictable
- Inference is optional and should be materialized offline

## SageMaker Mapping (deployment view)

For managed runs, treat S3 prefixes as the primary namespace:

- Inputs: `s3://…/plates_structured/plate-###/source/plate-###.jpg`
- Outputs: `s3://…/plates_structured/plate-###/runs/run-…/cpu_baseline.json`

In the graph:

- The `Run` node is global; its output `FileArtifact` URIs resolve to S3 keys.
- Ledgers are batch-derived `FileArtifact`s that summarize runs and measurements.

## Minimal v0 Commit Targets

1. Namespaces and URI policy (repo-relative vs S3)
2. Class list + core object properties
3. Mapping table: on-disk artifacts → ontology nodes/edges
4. SHACL shapes for the graph (later, after JSON Schemas stabilize)
