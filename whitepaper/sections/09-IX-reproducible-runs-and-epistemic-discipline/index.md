<!-- Auto-generated TOC-aligned file. Source of truth: A_World_Burning/26-whitepaper-skeleton.md -->

# IX. Reproducible Runs and Epistemic Discipline

[[whitepaper/DRAFT]] | [[whitepaper/MATERIALS_MAP]] | [[A_World_Burning/36-appendix-e-reproducibility-protocols]] | [[A_World_Burning/24-etiquette]]

_TOC-aligned entrypoint. Master outline lives in `A_World_Burning/26-whitepaper-skeleton.md`._

---

## Draft (body text)

Reproducibility is the mechanism by which this project earns the right to make claims about variance. Without sealed runs, the manifold collapses into a pile of files and a narrative that cannot be audited.

This section treats runs as lab practice: explicit configuration, version capture, append-only artifacts, and documented failure modes.

### IX.1 The run as an epistemic unit

A **run** is a sealed event. It is not “whatever happened in a notebook.” A run:

- declares its inputs (paths + checksums),
- declares its outputs (paths + checksums),
- captures model identifiers and versions,
- captures configuration (and preferably a config hash),
- records completion or failure modes.

Corrections are new runs. There is no editing of run outputs in place.

### IX.2 Identifiers and sealing

Run IDs must be chosen once and treated as law (sequential, hash-based, or hybrid). The key constraint is that a run ID provides a stable handle for:

- citation (which measurement produced this value?),
- audit (what code/model/config produced it?),
- rebuild (can we reproduce or explain drift?).

### IX.3 Validators (failure-intolerant)

Because the dataset lives in a notebook-driven environment (Colab/Drive), validators are the safety net:

- pre-run structure and schema assertion,
- post-run output registration checks,
- “no unregistered writes” as a hard failure.

This is not overengineering; it is the minimum needed to prevent silent provenance collapse.

### IX.4 Ledgers are derived views (dual-ledger principle)

Ledgers exist for speed, not truth. The authoritative artifacts are plate-local manifests and run outputs. Ledgers are rebuildable indices over those artifacts.

If a ledger disagrees with plate-local truth, the ledger is wrong.

---

## Sources (internal)

- [[A_World_Burning/36-appendix-e-reproducibility-protocols]]
- [[A_World_Burning/24-etiquette]]
- [[A_World_Burning/33-appendix-b-filesystem-naming-run-ids]]
- [[A_World_Burning/01_audubon_dual_ledger]]

---

## Outline (preserved)
**Purpose:** make the system auditable; define what ?a run? is and how it is sealed.

- IX.1 Run ontology
  - IX.1.a Run = sealed event; never edited; never merged
  - IX.1.b Runs are append-only; corrections are new runs
- IX.2 Run identifiers (choose and freeze)
  - IX.2.a sequential
  - IX.2.b hash-based
  - IX.2.c timestamp + short hash (recommended hybrid)
- IX.3 Run manifest schema (Appendix B)
  - IX.3.a required fields (run_id, plate_id, timestamp, models, outputs)
  - IX.3.b config hash, code version, environment capture
  - IX.3.c input list + checksums; output list + checksums
- IX.4 Validators (failure intolerant)
  - IX.4.a filesystem invariant validation (pre-run)
  - IX.4.b schema validation (pre-run)
  - IX.4.c post-run validation (all outputs registered + exist)
- IX.5 Notebook discipline (Appendix E)
  - IX.5.a CPU notebook rules
  - IX.5.b GPU notebook rules
  - IX.5.c forbidden anti-patterns (silent failures, unregistered writes, implicit state)
- IX.6 Ledgers: derived, rebuildable, disposable
  - IX.6.a ledger rebuild protocol
  - IX.6.b ?ledger disagreeing with plate truth? resolution rule
  - IX.6.c Dual-ledger principle (must be explicit)
    - plate-local verbose artifacts = authoritative provenance (?truth?)
    - global ledgers = speed layer (append-only; rebuildable; disposable)
    - if plate-local and ledger disagree, the ledger is wrong
