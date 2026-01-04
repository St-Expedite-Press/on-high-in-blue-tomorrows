# 43 - OWL Ontology Sketch (v0)

This file sketches an OWL (RDF/OWL) ontology for this repo and dataset.
It is intentionally a planning artifact: names, layers, and modeling decisions.
No serialization yet.

See also:

- `GOVERNANCE_CHECKLIST.md`
- `pipeline/ingestion_contract.md`

## Goal

Represent the corpus as a knowledge graph where:

- Identity is stable (`Plate`, `CorpusRelease`)
- Provenance is explicit (`Run`, `FileArtifact`, `Agent`)
- Measurements and interpretations never overwrite immutables
- Heavy numeric payloads stay in files (Parquet/JSON/PNG/NPY), referenced by URI + checksum

## Design Principles

1. Triples encode relationships and provenance; arrays/rasters stay out-of-graph.
2. Canon is a release-scoped claim: the same plate can have multiple variants without conflict.
3. `Place` is the spatial substrate that derived artifacts reference.
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
- `bws:Plate` (work-level stable identity, e.g. `plate-001`)
- `bws:PlateVariant` (a specific digitization/source lineage)
- `bws:Source` (institution/collection/API endpoint)
- `bws:Acquisition` (how a variant was obtained)
- `bws:Place` (spatial substrate / coordinate system)
- `bws:Run` (append-only computational event)
- `bws:FileArtifact` (anything that exists on disk/S3: JSON/PNG/JPG/Parquet/etc.)
- `bws:Schema` (JSON schema, SHACL shape, etc.)
- `bws:Method` (algorithm family)
- `bws:Model` (specific model checkpoint or versioned instrument)
- `bws:Environment` (runtime: OS/Python/libs/hardware)
- `bws:Measurement` (typed output of a run)
- `bws:FeatureFamily` (what can be measured)
- `bws:Region` (spatial subset of a `Place`)
- `bws:Assertion` (interpretive claim; explicitly downstream)
- `bws:Agent` (human or system)

### Key "Jumping Off Points"

- `CorpusRelease` -> enumerate plates, variants, runs, schemas, ledgers
- `Plate` -> variants, place, runs, assertions
- `PlateVariant` -> acquisition, source, immutable files
- `Run` -> models/config/env, inputs, outputs, validation status
- `FeatureFamily` -> what can be measured vs what was measured
- `Schema` -> what governs writes and validation

## Layering (recommended 4 layers)

### Layer 1: Corpus Identity

Stable identity and catalog facts.

- `Plate` is the stable work-level entity (`plate-001`).
- `PlateVariant` is a specific digitization/source lineage.
- `CorpusRelease` is a versioned bundle of claims about which variants are canonical for a release.

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
- `bws:createdAt` / `bws:observedAt`

Relations:

- `PlateVariant bws:hasSourceImage FileArtifact`
- `Plate bws:hasManifest FileArtifact`
- `FileArtifact bws:conformsTo Schema`

### Layer 3: Process & Runs

Runs are append-only computational events.

Relations:

- `Run bws:aboutPlate Plate`
- `Run bws:aboutVariant PlateVariant` (when a run is variant-specific)
- `Run bws:usesModel Model`
- `Run bws:usesMethod Method`
- `Run bws:usesEnvironment Environment`
- `Run bws:usesInput FileArtifact`
- `Run bws:generates FileArtifact`
- `Run bws:hasMeasurement Measurement`

### Layer 4: Interpretation & Assertions

This is where meaning lives, never in the immutable substrate.

- Segment labels, taxonomies, "foreground vs margin" decisions, historical claims
- Confidence and decision basis are first-class (`Assertion`)

Relations:

- `Assertion bws:aboutPlate Plate`
- `Assertion bws:hasEvidence FileArtifact`
- `Assertion bws:confidenceLiteral xsd:decimal`

## Place Model (spatial substrate)

`Place` is the coordinate system that downstream artifacts reference.

Recommended immutables:

- orientation: rotation, flips
- geometry: width, height, aspect ratio
- tiling: tile size, tile grid, mapping rules
- bounds: image bounds, content bounds, confidence state
- scale: physical dimensions when known (dpi, mm)

Relations:

- `Plate bws:hasPlace Place`
- `Region bws:inPlace Place`
- `Region bws:describedBy FileArtifact` (mask/polygons/bbox JSON)

## Regions & Segments

`Region` is a spatial subset of a `Place`.

Representations should be file-backed:

- bbox JSON
- polygon GeoJSON
- raster mask PNG
- vector contours (RLE, SVG paths, etc.)

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
- `Measurement bws:hasValueFile FileArtifact` (for arrays/rasters/vectors/histograms)

Example feature families (current + likely):

- `bws:CpuBaseline` (geometry, histograms, entropy, hashes, sharpness proxy)
- `bws:Segmentation` (mask + metrics)
- `bws:Embedding` (global embedding, tile embedding, multimodal embedding)
- `bws:Forensics` (compression, ICC, EXIF, noise models)
- `bws:TextExtraction` (OCR, layout, captions)
- `bws:Registration` (alignment transforms between variants)
- `bws:QualityControl` (flags, thresholds, outlier status)

---

## Comprehensive Accounting Inventory (Things We Must Be Able To Represent)

This is the "everything we might have to account for" checklist. Not every project state will have every item, but the ontology should have a home for them.

### Identity and Catalog

- Plate identity (plate_id, plate_number, titles, slugs)
- Plate edition/release membership (`CorpusRelease`)
- Variant identity (what makes a new variant distinct; minimum admissible fields)
- Plate-to-variant crosswalk and canonical declarations per release
- Exclusion log (what was rejected and why)

### Sources, Acquisition, and Rights

- Source institution/collection, holding identifiers, IIIF endpoints, URLs
- Acquisition method (download, IIIF, scan pipeline, manual ingest), timestamps
- License/rights/credit text and constraints
- Terms changes over time

### Core Evidence Files (Immutable)

- Source image file(s) and checksums (per-plate `source.sha256`)
- Plate manifest (`manifest.json`)
- Any raw index (`data.json`) and provenance of its generation
- File format details:
  - format (JPEG/PNG/TIFF), extension
  - dimensions, color mode
  - ICC profile presence/hash
  - EXIF presence
  - compression / quantization signatures
  - bit depth, gamma (when available)

### Storage and Namespaces

- Repo-relative paths vs local disk vs remote store (S3/HTTP)
- Canonical destination policy (e.g., `_RUN_OUTPUT` authoritative until remote store exists)
- URI policy for graph identifiers (stable, dereferenceable when possible)

### Runs (Activities)

- Run ID, timestamps, sharding parameters
- Run intent / notes
- Inputs used (which exact file artifacts, with checksums)
- Outputs written (artifact list)
- Validation status (pass/fail, failure mode, sample errors)

### Environment and Compute

- OS, Python version
- library versions
- hardware (CPU, RAM, GPU type/VRAM)
- container image / digest (if applicable)
- determinism controls (random seeds, nondeterminism notes)

### Schemas and Validation

- Schema authority (repo versioned)
- Schema hash/version used for a run
- SHACL shapes used to validate graph state (future)
- Hard-gate checklist results (plate count, manifest validity, output existence, schema validity, report fields)

### Derived Artifacts (Measurement Layer)

For each derived artifact type, be able to represent:

- what it is (method/model)
- parameters
- geometry/coordinate system (`Place`)
- provenance to inputs
- where it lives (file artifact)
- summary scalars (for fast indexing/QC)

Concrete examples already present in this repo:

- CPU baseline (`cpu_baseline.json`)
  - histograms/stats/entropy/clipping
  - hashes (aHash/dHash/pHash)
  - blur proxy (laplacian variance)
- Segmentation Otsu (`segmentation.json` + `segmentation_mask.png`)
  - threshold, downsampling, polarity, foreground ratio

Likely near-term additions:

- Standardized-luma variants (explicitly labeled derived transforms)
- Adaptive threshold segmentation baselines
- Edge/linework measures
- Thumbnail/raster previews (explicitly derived, never overwriting sources)

### Embeddings and Similarity

- Model identity (checkpoint, license)
- Preprocessing steps and image representation used
- Global embedding vectors
- Tile embeddings and tiling law
- Similarity indices, neighbors, clustering outputs
- Versioned ANN index artifacts and rebuild policy

### Segmentation and Structure (Beyond Otsu)

- Model-based segmentation (SAM/Mask2Former/etc.) as instruments
- Mask representations and conversions (PNG, RLE, polygons)
- Post-processing rules, filtering heuristics
- QC metrics per mask/plate (counts, areas, confidence)
- Explicit non-claims (no semantics unless attached as assertions)

### Registration / Alignment (Variants)

- Intra-variant alignment transforms (homography, thin-plate splines, etc.)
- Control points and residual errors
- Canonical reference space per plate/release

### Text and Layout

- OCR outputs (text, confidence, bounding boxes)
- Layout zones (margins, captions, plate numbers)
- Script/language detection

### Downstream Interpretation Layer (Explicitly Downstream)

- Transformations (e.g., stress regimes, generative edits) as labeled artifacts
- Quarantine: no contamination of measurement layer or core evidence
- Assertion objects linking to evidence (with confidence and justification)

### Publication and Packaging

- Corpus release packaging (what is included, what is excluded)
- Checksums and manifests for publication bundles
- Citation identifiers for plates/variants/runs

### Governance, Policy, and Ethics

- Guardrails and prohibitions (what the system refuses to claim)
- Access controls / redactions if needed
- Audit logs and decision records

---

## OWL Reasoning Profile

Default recommendation:

- OWL 2 RL (or "OWL-lite + SHACL") to keep costs predictable
- Inference is optional and should be materialized offline

## Minimal v0 Commit Targets

1. Namespaces and URI policy (repo-relative vs local disk vs remote store)
2. Class list + core object properties
3. Mapping table: on-disk artifacts -> ontology nodes/edges
4. SHACL shapes for the graph (later, after JSON Schemas stabilize)
