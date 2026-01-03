# Starting to Look Real Formal (Filesystem + Graph Contract)

Below is a **production-grade, failure-intolerant filesystem + graph ingestion contract** designed to support **Amazon Neptune as the canonical knowledge graph**, with **brutal rejection rules** and **provable lineage** from pixel → embedding → interpretation.

This is written as if it were going to be audited by a museum, a journal, or a federal archive. Nothing hand-wavy. Nothing “best effort.”

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
    If it can’t be reverse-resolved to disk → it doesn’t exist.
    

---

## II. Canonical directory hierarchy (final)

```
burning-world-series/
│
├── datasets/
│   └── audubon/
│       ├── raw/                         # Untouched source material
│       │   ├── img/
│       │   │   └── ranges/              # 1-99/, 100-199/, etc
│       │   ├── data.json
│       │   └── README.md
│       │
│       ├── structured/                  # Plate-centric canonical form
│       │   └── plate-XXX/
│       │       ├── manifest.json
│       │       ├── source.sha256
│       │       ├── source/
│       │       │   └── plate-XXX.original.jpg
│       │       ├── derived/
│       │       │   ├── input_image.json
│       │       │   └── image_header.json
│       │       ├── runs/
│       │       │   └── run-YYYYMMDD-HHMMSS-<hash>/
│       │       │       ├── run.manifest.json
│       │       │       ├── config.json
│       │       │       ├── outputs/
│       │       │       │   ├── embeddings/
│       │       │       │   ├── segments/
│       │       │       │   ├── metrics/
│       │       │       │   └── visuals/
│       │       │       └── run.sha256
│       │       └── viz/                 # Human-readable previews only
│       │
│       ├── ledgers/
│       │   ├── plates.parquet
│       │   ├── runs.parquet
│       │   ├── embeddings.parquet
│       │   ├── segments.parquet
│       │   └── neptune_ingest.parquet
│       │
│       ├── schemas/
│       │   ├── plate.manifest.schema.json
│       │   ├── run.manifest.schema.json
│       │   ├── embedding.schema.json
│       │   ├── segment.schema.json
│       │   └── neptune.node.schema.json
│       │
│       └── validators/
│           ├── filesystem.py
│           ├── schemas.py
│           ├── checksums.py
│           └── neptune_contract.py
│
├── graph/
│   ├── neptune/
│   │   ├── nodes/
│   │   ├── edges/
│   │   ├── bulk_load/
│   │   └── mapping/
│   │
│   └── ontology/
│       ├── core.ttl
│       ├── audubon.ttl
│       ├── burning_world.ttl
│       └── provenance.ttl
│
├── notebooks/
├── scripts/
└── docs/
```

---

## III. File naming law (strict)

### 1. Plate identifiers (immutable)

```
plate-001 … plate-435
```

• Zero-padded  
• No aliases  
• Never inferred from filenames after bootstrap

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
    → abort
    

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
  "config_hash": "sha256:…",
  "inputs": [
    "source/plate-123.original.jpg"
  ],
  "outputs": [],
  "neptune_nodes": [],
  "status": "incomplete"
}
```

**Rules**

- outputs list must be populated before status → `complete`
    
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

**Filesystem → Parquet → CSV → Neptune**

```
ledgers/*.parquet
   ↓
graph/neptune/bulk_load/
   ├── nodes.csv
   ├── edges.csv
   └── load.properties
```

Each row must include:

- `source_file_path`
    
- `run_id`
    
- `plate_id`
    
- `checksum`
    

If any row cannot be reverse-resolved → **entire load rejected**

---

## VII. Ontology discipline (non-optional)

You must maintain:

- `core.ttl` → generic graph concepts
    
- `audubon.ttl` → species, plates, taxonomy
    
- `burning_world.ttl` → counterfactual constructs
    
- `provenance.ttl` → run, artifact, derivation
    

**No node enters Neptune without ontology grounding.**

---

## VIII. What this system gives you

• Museum-grade auditability  
• Paper-ready reproducibility  
• Zero silent drift  
• Safe ML experimentation  
• Ability to retract or supersede interpretations without deleting history  
• A graph that can survive 20 years of reinterpretation

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
    
- Design the “Burning World” ontology layer
    
- Map this directly to a paper methods section
    

Just say where to drill next.
