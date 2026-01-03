# Etiquette (Templates + Standards)

Below is a **general, reusable template plus strict Pythonic guidelines** for how **CPU-only** and **GPU-required** notebooks should be written in this project. This is meant to be copy-pasted and treated as _law_, not style advice.

I’ll separate this into:  
A. Shared rules (apply to all notebooks)  
B. CPU notebook template + guidelines  
C. GPU notebook template + guidelines  
D. Anti-patterns (what will silently destroy provenance if allowed)

No fluff.

---

## A. SHARED RULES (ALL NOTEBOOKS)

These apply universally.

### 1. Notebooks are execution units, not exploration scratchpads

A notebook must be:

- deterministic
    
- re-runnable
    
- self-validating
    
- failure-intolerant
    

If you want to “poke around,” that happens **outside** the pipeline.

---

### 2. Mandatory notebook structure (in order)

Every notebook must have these sections, in this order:

1. **Header comment** (purpose, scope, writes)
    
2. **Environment & hardware detection**
    
3. **Structure & naming assertion**
    
4. **Configuration block**
    
5. **Pure functions**
    
6. **Execution loop**
    
7. **Validation & registration**
    
8. **Ledger / graph sync**
    
9. **Final report + explicit STOP**
    

No section may be skipped.

---

### 3. Zero implicit state

Forbidden:

- relying on variables defined in previous notebooks
    
- mutable globals modified mid-run
    
- implicit working directories
    

Every path must be derived from `DATASET_ROOT`.

---

### 4. Writes must be explicit and registered

Any file written must:

- have a declared destination
    
- be registered in a run manifest or ledger
    
- be checksum-verifiable
    

If a file is written but not registered → **hard failure**.

---

## B. CPU NOTEBOOK TEMPLATE (REFERENCE)

Use this for:

- manifests
    
- validation
    
- scalar metadata
    
- ledgers
    
- graph prep
    
- statistics
    
- indexing
    

### CPU notebooks NEVER:

- request a GPU
    
- batch tensors
    
- store large arrays
    
- loop silently over failures
    

---

### CPU Notebook Template

```python
# ============================================================
# NBXX — <TITLE>
# ------------------------------------------------------------
# Purpose:
#   - <exactly what this notebook does>
#
# Writes:
#   - <explicit list of files>
#
# Does NOT:
#   - use GPU
#   - mutate images
#   - perform ML inference
# ============================================================

# -----------------------------
# ENVIRONMENT
# -----------------------------

import os
import sys
from pathlib import Path
import json

assert "COLAB_GPU" not in os.environ, "GPU detected in CPU-only notebook"

# -----------------------------
# PROJECT HANDOFF
# -----------------------------

from project_handoff import (
    DATASET_ROOT,
    PLATES_STRUCTURED,
    LEDGER_DIR,
)

# -----------------------------
# STRUCTURE ASSERTION
# -----------------------------

from validators.filesystem import assert_structure
assert_structure(DATASET_ROOT)

# -----------------------------
# CONFIG (IMMUTABLE)
# -----------------------------

CONFIG = {
    "background_threshold": 245,
    "entropy_bins": 256,
}

# -----------------------------
# PURE FUNCTIONS ONLY
# -----------------------------

def compute_entropy(hist: list[float]) -> float:
    ...

# -----------------------------
# EXECUTION
# -----------------------------

results = []

for plate_dir in sorted(PLATES_STRUCTURED.iterdir()):
    ...

# -----------------------------
# VALIDATION
# -----------------------------

assert len(results) == 435, "Missing plate results"

# -----------------------------
# WRITE OUTPUTS
# -----------------------------

out_path = LEDGER_DIR / "plates.parquet"
write_parquet(results, out_path)

# -----------------------------
# FINAL REPORT
# -----------------------------

print("✔ CPU preprocessing complete")
print("✔ No GPU used")
print("✔ Safe to proceed")

# -----------------------------
# STOP
# -----------------------------
raise SystemExit("NBXX complete")
```

---

### CPU Notebook Guidelines (Hard)

✔ Favor **scalar summaries**  
✔ Favor **streaming reads**  
✔ Use **assert**, not `if`  
✔ Fail early  
✔ Prefer Parquet for tabular outputs  
✔ Never store per-pixel arrays

---

## C. GPU NOTEBOOK TEMPLATE (REFERENCE)

Use this for:

- segmentation
    
- embeddings
    
- generative transforms
    
- LoRA training
    
- batch inference
    

GPU notebooks are **dangerous**: they must be even stricter.

---

### GPU Notebook Template

```python
# ============================================================
# NBXX — <TITLE>
# ------------------------------------------------------------
# Purpose:
#   - <what model is run and why>
#
# Writes:
#   - run-scoped artifacts only
#
# Requires:
#   - GPU
# ============================================================

# -----------------------------
# ENVIRONMENT
# -----------------------------

import os
import torch

assert torch.cuda.is_available(), "GPU required but not available"

device = torch.device("cuda")

print("GPU:", torch.cuda.get_device_name(0))

# -----------------------------
# PROJECT HANDOFF
# -----------------------------

from project_handoff import (
    DATASET_ROOT,
    PLATES_STRUCTURED,
)

# -----------------------------
# STRUCTURE ASSERTION
# -----------------------------

from validators.filesystem import assert_structure
assert_structure(DATASET_ROOT)

# -----------------------------
# RUN INITIALIZATION
# -----------------------------

from runs import start_run

plate_dir = ...
run_dir = start_run(
    plate_dir=plate_dir,
    models=["sam-vit-h"],
    note="primary semantic segmentation"
)

# -----------------------------
# CONFIG (HASHED)
# -----------------------------

CONFIG = {
    "model": "sam-vit-h",
    "checkpoint": "...",
    "threshold": 0.5,
}

write_config(run_dir, CONFIG)

# -----------------------------
# MODEL LOAD (EXPLICIT)
# -----------------------------

model = load_model(CONFIG).to(device)
model.eval()

# -----------------------------
# EXECUTION LOOP
# -----------------------------

for plate_dir in PLATES_STRUCTURED.iterdir():
    with torch.no_grad():
        ...

    save_outputs(...)
    register_output(run_dir, ...)

# -----------------------------
# VALIDATION
# -----------------------------

validate_run(run_dir)

# -----------------------------
# FINALIZE RUN
# -----------------------------

finalize_run(run_dir)

print("✔ GPU run complete")
print("✔ All outputs registered")

raise SystemExit("NBXX complete")
```

---

### GPU Notebook Guidelines (Hard)

✔ One model family per notebook  
✔ One conceptual operation per run  
✔ Always log model version + checkpoint  
✔ Always record device + precision  
✔ Never mix CPU preprocessing logic  
✔ No “quick previews” without registration  
✔ Always support batch size = 1 fallback

---

## D. ABSOLUTE ANTI-PATTERNS (FORBIDDEN)

These will destroy your dataset if allowed:

❌ Silent `try/except` blocks  
❌ Writing files without registration  
❌ Overwriting artifacts  
❌ Using randomness without a logged seed  
❌ Mutating source images  
❌ Mixing segmentation + embedding + transformation in one notebook  
❌ Relying on notebook execution order  
❌ Treating Neptune as primary storage

---

## E. Mental Model (Important)

Think of notebooks as:

> **Controlled experiments whose outputs must survive hostile scrutiny**

If a notebook cannot be:

- audited
    
- rerun in six months
    
- explained line by line
    

It does not belong in the pipeline.

---

### Where this leaves you

You are now at the point where:

- the tech stack can be finalized
    
- GPU usage can be budgeted
    
- the pipeline can scale safely
    
- reviewers cannot accuse you of hand-waving
    

If you want next, I can:

- convert this into a literal `NOTEBOOK_RULES.md`
    
- generate boilerplate notebooks NB00–NB06
    
- write a pre-commit validator for Colab
    
- design a failure-injection test suite
    

Say which.

Maybe final tech stack?

Below is a **fully specified, end-to-end tech stack** for _The Burning World_ project as it exists **now**, scaled to where you are headed (Neptune + A100 + publication-grade reproducibility). This is written as a **design document**, not a shopping list.

I’ll break it into layers, explain _why each is chosen_, and flag **hard vs optional** components.

---

## 0. High-level architecture (one sentence)

**Immutable files on disk → append-only ledgers → derived graph in Amazon Neptune → analysis & generation notebooks that never overwrite evidence.**

Everything flows in that direction only.

---

## 1. Execution environment

### Primary environment

**Google Colab Pro / Pro+**

- GPU: **NVIDIA A100 (40GB)**
    
- CPU: sufficient for preprocessing, validation, Parquet I/O
    
- Storage: ephemeral compute + mounted Google Drive (for now)
    

**Why**

- Fast iteration
    
- Zero infra friction
    
- A100 handles SAM, CLIP, DINOv2, LoRA without compromise
    

**Constraints**

- Stateless kernels → reinforces discipline
    
- No background daemons → notebook scheduling matters
    

---

### Secondary / future environment (optional)

**AWS EC2 (p4d / g5) + S3**

Only needed once:

- dataset stabilizes
    
- you want persistent GPU jobs
    
- Neptune ingestion moves fully into AWS
    

---

## 2. Storage & filesystem layer (ground truth)

### Current

**Google Drive (mounted)**

Used for:

- source images
    
- derived artifacts
    
- ledgers
    
- schemas
    
- notebooks
    

**Why acceptable now**

- Human inspectability
    
- Versionable at directory granularity
    
- Easy sharing during research phase
    

**Known limits**

- Not ideal for long-term cold storage
    
- Latency under parallel GPU writes
    

---

### Planned evolution

**S3 (authoritative) + Drive (working mirror)**

- S3 = archival truth
    
- Drive = working copy / staging
    
- Checksums guarantee equivalence
    

---

## 3. Data formats (non-negotiable choices)

### Images

- **JPEG / PNG** on disk only
    
- Never stored inside Parquet
    
- Never embedded in Neptune
    

**Rationale**

- Images are primary evidence
    
- Graphs and tables reference them, never replace them
    

---

### Tabular / numeric data

**Apache Parquet + PyArrow**

Used for:

- plate ledger
    
- run ledger
    
- embedding ledger
    
- segmentation ledger
    
- Neptune ingest tables
    

**Why Parquet**

- Columnar → fast scans
    
- Schema-enforced
    
- Compresses scalars well
    
- Language-agnostic (Python, R, Spark, Java)
    

---

### Configuration & manifests

**JSON (strict schemas)**

- plate.manifest.json
    
- run.manifest.json
    
- config.json
    
- input_image.json
    

**Why**

- Human-readable
    
- Validatable
    
- Stable for long-term archiving
    

---

## 4. Validation & failure enforcement layer

### Libraries

- `jsonschema` (Draft 2020-12)
    
- custom filesystem validators
    
- SHA-256 checksums (hashlib)
    

### Philosophy

- Fail early
    
- Fail loud
    
- Fail globally
    

**No warnings. No partial success.**

---

## 5. Core Python stack (CPU)

### Standard

- `python 3.11+`
    
- `pathlib`
    
- `json`
    
- `hashlib`
    
- `datetime (timezone-aware)`
    

### Numeric / CV (CPU)

- `numpy`
    
- `scipy`
    
- `opencv-python`
    
- `Pillow`
    
- `scikit-image`
    

### Data

- `pyarrow`
    
- `pandas` (only for light inspection)
    

### Visualization

- `matplotlib`
    
- `seaborn` (sparingly)
    
- `plotly` (for interactive figures)
    

---

## 6. GPU / ML stack (critical)

### Framework

**PyTorch 2.x**

- CUDA 12
    
- AMP / bfloat16 support
    
- TorchScript optional
    

---

### Segmentation models (definite)

1. **SAM (Segment Anything)**
    
    - `sam-vit-h` (primary)
        
    - `sam-vit-l` (fallback)
        
    - Task: ontology break (bird / flora / ground / sky / inscription)
        
2. **Mask2Former**
    
    - For structured multi-class segmentation
        
    - Benchmark vs SAM
        
3. **U²-Net**
    
    - Lightweight foreground/background baseline
        

---

### Embedding models (definite)

1. **CLIP**
    
    - ViT-L/14
        
    - OpenCLIP variants
        
    - Baseline semantic embedding
        
2. **DINOv2**
    
    - Self-supervised structure
        
    - Excellent for morphology / pose
        
3. **EVA-CLIP**
    
    - Higher fidelity aesthetic embeddings
        

---

### Embedding models (experimental / unconventional)

- **SigLIP** (Google)
    
- **BiomedCLIP**
    
    - Surprising utility for anatomical stress
        
- **ImageBind**
    
    - Future-proof multimodal alignment
        

---

### Generative / transformation models (later phase)

- Stable Diffusion XL (control-only)
    
- LoRA-based fine-tuning (style grammar, not anatomy)
    
- ControlNet (segmentation-conditioned)
    

---

## 7. Graph layer (authoritative semantics)

### Database

**Amazon Neptune**

- Property graph (Gremlin)
    
- RDF/OWL support (TTL ontologies)
    

### Role

- Store relationships, not data
    
- Enable queries like:
    
    - “Which visual stress motifs co-occur with predatory posture?”
        
    - “Which transformations invert Audubon’s staging logic?”
        

---

### Ontologies

- `core.ttl`
    
- `audubon.ttl`
    
- `burning_world.ttl`
    
- `provenance.ttl`
    

---

## 8. Neptune ingestion stack

### Data prep

- Parquet → CSV (schema-controlled)
    
- Explicit node & edge tables
    

### Validation

- Reverse path resolution
    
- Checksum verification
    
- Run ID existence
    

### Query layer

- Gremlin for traversal
    
- SPARQL for semantic reasoning
    

---

## 9. Notebook orchestration

### Structure

- One notebook per epistemic phase
    
- CPU and GPU notebooks separated
    
- No hidden state
    

### Supporting utilities

- `project_handoff.py`
    
- `validators/`
    
- `runs/`
    

---

## 10. Versioning & reproducibility

### Code

- Git (commit hash recorded per run)
    

### Data

- Append-only
    
- Checksummed
    
- Schema-validated
    

### Models

- Exact checkpoint IDs logged
    
- No “latest” tags
    

---

## 11. Monitoring & metrics (lightweight)

- Progress bars (`tqdm`)
    
- Runtime logging per plate
    
- GPU memory tracking (torch.cuda)
    

---

## 12. What this stack enables (concretely)

You can now:

- Defend every pixel transformation in a paper
    
- Reconstruct any figure from disk + graph
    
- Train LoRAs without dataset contamination
    
- Produce counterfactual climate imagery _without hallucination_
    
- Treat Audubon as a **visual system**, not a set of pictures
    
- Hand this dataset to an institution without apology
    

---

## 13. What you are ready to formalize **right now**

✔ Tech stack locked  
✔ GPU budget estimable  
✔ Notebook schedule fixed  
✔ Graph integration justified  
✔ Methods section draftable

---

### Next logical steps (pick one)

1. Lock **exact model list + checkpoints**
    
2. Write **NB06 (Segmentation Benchmarking)** skeleton
    
3. Design **Neptune node/edge schemas**
    
4. Draft **paper Methods + Dataset Card**
    
5. Plan **Burning World transformation grammar**
    

Say which one you want to drill into next.
