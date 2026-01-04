# Starting to Look Real Formal (Filesystem + Graph Contract)

Below is a **production-grade, failure-intolerant filesystem + graph ingestion contract** designed to support **Amazon Neptune as the canonical knowledge graph**, with **brutal rejection rules** and **provable lineage** from pixel ΓåÆ embedding ΓåÆ interpretation.

This is written as if it were going to be audited by a museum, a journal, or a federal archive. Nothing hand-wavy. Nothing ΓÇ£best effort.ΓÇ¥

---

## I. Governing principles (non-negotiable)

1. **Files are evidence.**  
    Every file must be attributable to:
    
    - a plate
        
    - a run
        
    - a model or algorithm
        
    - a configuration hash
        
    - a timestamp
        
2. **Graphs are derived truth, not primary truth.**  
    Neptune stores _relationships and interpretations_.  
    Filesystem stores _grounded artifacts_.
    
3. **No silent failure.**  
    Any deviation from naming, schema, or linkage:
    
    - hard error
        
    - run aborted
        
    - nothing written
        
4. **Append-only semantics.**  
    No overwrites. Ever.  
    Corrections are new runs.
    
5. **Every node in Neptune must be traceable to a file path.**  
    If it canΓÇÖt be reverse-resolved to disk ΓåÆ it doesnΓÇÖt exist.
    

---

## II. Canonical directory hierarchy (final)

```
burning-world-series/
Γöé
Γö£ΓöÇΓöÇ datasets/
Γöé   ΓööΓöÇΓöÇ audubon/
Γöé       Γö£ΓöÇΓöÇ raw/                         # Untouched source material
Γöé       Γöé   Γö£ΓöÇΓöÇ img/
Γöé       Γöé   Γöé   ΓööΓöÇΓöÇ ranges/              # 1-99/, 100-199/, etc
Γöé       Γöé   Γö£ΓöÇΓöÇ data.json
Γöé       Γöé   ΓööΓöÇΓöÇ README.md
Γöé       Γöé
Γöé       Γö£ΓöÇΓöÇ structured/                  # Plate-centric canonical form
Γöé       Γöé   ΓööΓöÇΓöÇ plate-XXX/
Γöé       Γöé       Γö£ΓöÇΓöÇ manifest.json
Γöé       Γöé       Γö£ΓöÇΓöÇ source.sha256
Γöé       Γöé       Γö£ΓöÇΓöÇ source/
Γöé       Γöé       Γöé   ΓööΓöÇΓöÇ plate-XXX.original.jpg
Γöé       Γöé       Γö£ΓöÇΓöÇ derived/
Γöé       Γöé       Γöé   Γö£ΓöÇΓöÇ input_image.json
Γöé       Γöé       Γöé   ΓööΓöÇΓöÇ image_header.json
Γöé       Γöé       Γö£ΓöÇΓöÇ runs/
Γöé       Γöé       Γöé   ΓööΓöÇΓöÇ run-YYYYMMDD-HHMMSS-<hash>/
Γöé       Γöé       Γöé       Γö£ΓöÇΓöÇ run.manifest.json
Γöé       Γöé       Γöé       Γö£ΓöÇΓöÇ config.json
Γöé       Γöé       Γöé       Γö£ΓöÇΓöÇ outputs/
Γöé       Γöé       Γöé       Γöé   Γö£ΓöÇΓöÇ embeddings/
Γöé       Γöé       Γöé       Γöé   Γö£ΓöÇΓöÇ segments/
Γöé       Γöé       Γöé       Γöé   Γö£ΓöÇΓöÇ metrics/
Γöé       Γöé       Γöé       Γöé   ΓööΓöÇΓöÇ visuals/
Γöé       Γöé       Γöé       ΓööΓöÇΓöÇ run.sha256
Γöé       Γöé       ΓööΓöÇΓöÇ viz/                 # Human-readable previews only
Γöé       Γöé
Γöé       Γö£ΓöÇΓöÇ ledgers/
Γöé       Γöé   Γö£ΓöÇΓöÇ plates.parquet
Γöé       Γöé   Γö£ΓöÇΓöÇ runs.parquet
Γöé       Γöé   Γö£ΓöÇΓöÇ embeddings.parquet
Γöé       Γöé   Γö£ΓöÇΓöÇ segments.parquet
Γöé       Γöé   ΓööΓöÇΓöÇ neptune_ingest.parquet
Γöé       Γöé
Γöé       Γö£ΓöÇΓöÇ schemas/
Γöé       Γöé   Γö£ΓöÇΓöÇ plate.manifest.schema.json
Γöé       Γöé   Γö£ΓöÇΓöÇ run.manifest.schema.json
Γöé       Γöé   Γö£ΓöÇΓöÇ embedding.schema.json
Γöé       Γöé   Γö£ΓöÇΓöÇ segment.schema.json
Γöé       Γöé   ΓööΓöÇΓöÇ neptune.node.schema.json
Γöé       Γöé
Γöé       ΓööΓöÇΓöÇ validators/
Γöé           Γö£ΓöÇΓöÇ filesystem.py
Γöé           Γö£ΓöÇΓöÇ schemas.py
Γöé           Γö£ΓöÇΓöÇ checksums.py
Γöé           ΓööΓöÇΓöÇ neptune_contract.py
Γöé
Γö£ΓöÇΓöÇ graph/
Γöé   Γö£ΓöÇΓöÇ neptune/
Γöé   Γöé   Γö£ΓöÇΓöÇ nodes/
Γöé   Γöé   Γö£ΓöÇΓöÇ edges/
Γöé   Γöé   Γö£ΓöÇΓöÇ bulk_load/
Γöé   Γöé   ΓööΓöÇΓöÇ mapping/
Γöé   Γöé
Γöé   ΓööΓöÇΓöÇ ontology/
Γöé       Γö£ΓöÇΓöÇ core.ttl
Γöé       Γö£ΓöÇΓöÇ audubon.ttl
Γöé       Γö£ΓöÇΓöÇ burning_world.ttl
Γöé       ΓööΓöÇΓöÇ provenance.ttl
Γöé
Γö£ΓöÇΓöÇ notebooks/
Γö£ΓöÇΓöÇ scripts/
ΓööΓöÇΓöÇ docs/
```

---

## III. File naming law (strict)

### 1. Plate identifiers (immutable)

```
plate-001 ΓÇª plate-435
```

ΓÇó Zero-padded  
ΓÇó No aliases  
ΓÇó Never inferred from filenames after bootstrap

---

### 2. Run identifiers (collision-resistant)

```
run-YYYYMMDD-HHMMSS-<8char_hash>
```

Where `<hash>` = SHA-1(models + config + code_version)[:8]

**Failure conditions**

- duplicate run ID
    
- missing config.json
    
- timestamp mismatch  
    ΓåÆ abort
    

---

### 3. Derived artifact naming

Every derived file **must encode its lineage**:

```
<plate_id>__<run_id>__<artifact_type>__<descriptor>.<ext>
```

Examples:

```
plate-123__run-20260112-142233-acde9123__embedding__clip-vit-l14.npy
plate-123__run-20260112-142233-acde9123__segment__sam-mask-004.png
plate-123__run-20260112-142233-acde9123__metric__entropy.json
```

**No freeform names. Ever.**

---

## IV. Run manifest (required, enforced)

`run.manifest.json`

```json
{
  "run_id": "run-20260112-142233-acde9123",
  "plate_id": "plate-123",
  "timestamp": "2026-01-12T14:22:33Z",
  "models": [
    "clip-vit-l14",
    "sam-vit-h"
  ],
  "code_version": "git:9f3c2a1",
  "config_hash": "sha256:ΓÇª",
  "inputs": [
    "source/plate-123.original.jpg"
  ],
  "outputs": [],
  "neptune_nodes": [],
  "status": "incomplete"
}
```

**Rules**

- outputs list must be populated before status ΓåÆ `complete`
    
- neptune_nodes must be resolvable to graph IDs
    

---

## V. Brutal failure system (what gets rejected)

### A. Filesystem validation (pre-run)

Reject if:

- plate directory missing required subdirs
    
- more than one file in `source/`
    
- checksum mismatch
    
- manifest schema violation
    

### B. Run-time validation

Abort immediately if:

- any output path does not match naming law
    
- output not registered in run.manifest
    
- array dimensions inconsistent with metadata
    
- image mutated without declaring transform
    

### C. Post-run validation

Reject entire run if:

- run.sha256 mismatch
    
- missing ledger entry
    
- Neptune ingest file incomplete
    
- orphaned graph nodes detected
    

---

## VI. Amazon Neptune integration (authoritative graph)

### 1. What goes into Neptune

**Nodes**

- Plate
    
- Image
    
- Segment
    
- Embedding
    
- Species
    
- MorphologicalFeature
    
- EnvironmentalCondition
    
- Transformation
    
- Run
    

**Edges**

- `DERIVED_FROM`
    
- `SEGMENTS`
    
- `EMBEDS`
    
- `TRANSFORMS`
    
- `IMPLIES`
    
- `OBSERVED_IN`
    
- `GENERATED_BY`
    

---

### 2. Neptune bulk ingestion pipeline

**Filesystem ΓåÆ Parquet ΓåÆ CSV ΓåÆ Neptune**

```
ledgers/*.parquet
   Γåô
graph/neptune/bulk_load/
   Γö£ΓöÇΓöÇ nodes.csv
   Γö£ΓöÇΓöÇ edges.csv
   ΓööΓöÇΓöÇ load.properties
```

Each row must include:

- `source_file_path`
    
- `run_id`
    
- `plate_id`
    
- `checksum`
    

If any row cannot be reverse-resolved ΓåÆ **entire load rejected**

---

## VII. Ontology discipline (non-optional)

You must maintain:

- `core.ttl` ΓåÆ generic graph concepts
    
- `audubon.ttl` ΓåÆ species, plates, taxonomy
    
- `burning_world.ttl` ΓåÆ counterfactual constructs
    
- `provenance.ttl` ΓåÆ run, artifact, derivation
    

**No node enters Neptune without ontology grounding.**

---

## VIII. What this system gives you

ΓÇó Museum-grade auditability  
ΓÇó Paper-ready reproducibility  
ΓÇó Zero silent drift  
ΓÇó Safe ML experimentation  
ΓÇó Ability to retract or supersede interpretations without deleting history  
ΓÇó A graph that can survive 20 years of reinterpretation

Most importantly:  
**It keeps interpretation downstream from evidence.**

---

## IX. Immediate next actions (recommended)

1. Freeze this directory + naming contract as LAW.md
    
2. Implement `validators/filesystem.py` first
    
3. Stub Neptune node/edge schemas
    
4. Do _one_ CLIP+SAM run end-to-end with full rejection enabled
    
5. Only then scale
    

If you want next:

- I can design the exact Neptune node/edge schemas
    
- Write the Gremlin or SPARQL patterns
    
- Create the validator code skeletons
    
- Design the ΓÇ£Burning WorldΓÇ¥ ontology layer
    
- Map this directly to a paper methods section
    

Just say where to drill next.
