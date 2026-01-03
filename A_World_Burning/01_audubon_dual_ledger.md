# Audubon Dual Ledger (Architecture)

Here is the **entire architecture, printed cleanly and contiguously**, with no omissions, no compression, and no commentary interleaved. This is the canonical specification you build against.

---

## PLATE-CENTRIC, DUAL-LEDGER ARCHITECTURE

**Authoritative spec v1**

### Core principle

- **The plate is the atomic unit**
    
- **Runs are sealed events**
    
- **Ledgers are derived, never authoritative**
    
- **Nothing overwrites source**
    
- **Everything is restartable**
    

---

## 1. Canonical directory structure

```
burning-world-series/
├── audubon-bird-plates-…/
│   ├── plates/
│   │   ├── plate-001/
│   │   │   ├── source/
│   │   │   │   └── plate-1-wild-turkey.jpg
│   │   │   ├── manifest.json
│   │   │   ├── runs/
│   │   │   │   ├── run-0001/
│   │   │   │   │   ├── embeddings/
│   │   │   │   │   ├── segments/
│   │   │   │   │   ├── captions/
│   │   │   │   │   └── metrics.json
│   │   │   │   └── run-0002/
│   │   │   ├── viz/
│   │   │   └── cache/
│   │   ├── plate-002/
│   │   └── …
│   ├── ledger/
│   │   ├── plates.parquet
│   │   ├── embeddings.parquet
│   │   ├── segments.parquet
│   │   └── runs.parquet
│   ├── schemas/
│   ├── validators/
│   └── directory_map.md
├── notebooks/
└── directory_map.md
```

---

## 2. Plate-local manifest (authoritative identity record)

### `schemas/plate.manifest.schema.json`

```json
{
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "$id": "https://burning-world-series/schemas/plate.manifest.schema.json",
  "title": "Plate Manifest",
  "type": "object",
  "required": [
    "plate_id",
    "plate_number",
    "title",
    "source_image"
  ],
  "properties": {
    "plate_id": {
      "type": "string",
      "pattern": "^plate-[0-9]{3}$"
    },
    "plate_number": {
      "type": "integer",
      "minimum": 1,
      "maximum": 435
    },
    "title": {
      "type": "string"
    },
    "scientific_name": {
      "type": ["string", "null"]
    },
    "common_names": {
      "type": "array",
      "items": { "type": "string" },
      "default": []
    },
    "source_image": {
      "type": "string",
      "description": "Relative path to canonical source image"
    },
    "license": {
      "type": "string"
    },
    "notes": {
      "type": ["string", "null"]
    }
  },
  "additionalProperties": false
}
```

**Rules**

- This file never stores ML output
    
- This file changes only to correct factual errors
    
- This file defines plate identity forever
    

---

## 3. Run-level manifest (sealed execution record)

### `schemas/run.manifest.schema.json`

```json
{
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "title": "Plate Run Manifest",
  "type": "object",
  "required": [
    "run_id",
    "plate_id",
    "timestamp",
    "models",
    "outputs"
  ],
  "properties": {
    "run_id": {
      "type": "string"
    },
    "plate_id": {
      "type": "string"
    },
    "timestamp": {
      "type": "string",
      "format": "date-time"
    },
    "models": {
      "type": "array",
      "items": { "type": "string" }
    },
    "outputs": {
      "type": "array",
      "items": { "type": "string" }
    },
    "notes": {
      "type": ["string", "null"]
    }
  },
  "additionalProperties": false
}
```

**Rules**

- One run = one sealed event
    
- Runs are never edited
    
- Runs are never merged
    
- Runs are only summarized upward
    

---

## 4. Dual-ledger model (non-negotiable)

### A. Plate-local data (authoritative provenance)

- Lives under `plates/plate-XXX/runs/`
    
- Complete, verbose, redundant
    
- Used for:
    
    - debugging
        
    - reconstruction
        
    - trust
        
    - provenance
        

### B. Global ledger (fast comparative layer)

- Lives under `ledger/*.parquet`
    
- Append-only
    
- Flattened
    
- Disposable
    
- Used for:
    
    - clustering
        
    - statistics
        
    - visualization
        
    - selection
        

**If plate-local data and ledger disagree, the ledger is wrong.**

---

## 5. Validators (minimal, strict)

### Plate validator

- Ensures `manifest.json` conforms to schema
    
- Ensures `source_image` exists
    

```python
import json
from jsonschema import Draft202012Validator

def validate_plate(plate_dir, schema):
    manifest = json.load(open(plate_dir / "manifest.json"))
    Draft202012Validator(schema).validate(manifest)

    src = plate_dir / manifest["source_image"]
    assert src.exists(), f"Missing source image: {src}"
```

### Run validator

- Ensures run references a valid plate
    
- Ensures declared outputs exist
    
- Ensures run folder is sealed
    

Validators must run:

- at notebook start
    
- before ledger aggregation
    
- before destructive cleanup
    

---

## 6. Operational rules (these do not bend)

1. Source images are immutable
    
2. Plate manifests are authoritative
    
3. Runs are append-only
    
4. Ledgers are derived and disposable
    
5. Every quantitative datum exists twice:
    
    - once locally (truth)
        
    - once globally (speed)
        
6. Any schema change requires an explicit version bump
    
7. If validation fails, the pipeline stops
    

---

## 7. What this architecture guarantees

- You can rerun extraction indefinitely
    
- You can diff runs across time
    
- You can delete and rebuild the ledger at will
    
- You can hand a single plate folder to another person and it is complete
    
- You never lose provenance
    
- You never wonder where a number came from
    

This is not a pipeline.  
This is an **archival system that tolerates violence**.

---

If you want the **next concrete step**, the only sensible options are:

1. Plate directory bootstrapper (current flat plates → plate-XXX dirs)
    
2. Ledger parquet schemas (embeddings / segments / runs)
    
3. Ledger aggregation notebook (plate → ledger)
    
4. Run ID semantics (hash-based vs sequential vs hybrid)
    

Say which.
