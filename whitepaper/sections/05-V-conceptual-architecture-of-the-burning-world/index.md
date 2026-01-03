<!-- Auto-generated TOC-aligned file. Source of truth: A_World_Burning/26-whitepaper-skeleton.md -->

# V. Conceptual Architecture of The Burning World

[[whitepaper/DRAFT]] | [[whitepaper/MATERIALS_MAP]] | [[A_World_Burning/01_audubon_dual_ledger]] | [[A_World_Burning/33-appendix-b-filesystem-naming-run-ids]]

_TOC-aligned entrypoint. Master outline lives in `A_World_Burning/26-whitepaper-skeleton.md`._

---

## Draft (body text)

The Burning World is an editorial and technical system that treats a work not as a single file but as a population of registered variants measured under reproducible constraints.

This section names the project’s “ontology”: what exists in the system, what is allowed to change, and what is forbidden to overwrite.

### V.1 Plate-centric identity (the atomic unit)

The plate is the atomic unit of identity. Plate identity is defined by stable identifiers and a registry (not by model outputs). All variants attach to a plate identity; no model output is allowed to create or redefine plate identity.

### V.2 Variant registration (how multiplicity enters)

Variants are admitted as first-class objects with provenance: source attribution, acquisition method, access date, integrity checksums, and terms/credit constraints. Variants are allowed to disagree; the system preserves disagreement as evidence.

### V.3 The run (an epistemic event)

Every computational act that produces documentary measurements is a **run**:

- sealed (append-only),
- explicit (declared inputs and outputs),
- auditable (versions, configs, checksums),
- repeatable (or its nondeterminism is documented and bounded).

### V.4 The ledger (a derived view, never the truth)

Ledgers exist to make the manifold queryable at scale. They are derived from plate-local truth and run artifacts, and they are rebuildable. If plate-local artifacts and ledgers disagree, the ledger is wrong.

This “dual-ledger” principle makes it possible to build fast query layers without sacrificing provenance.

### V.5 Stability vs controlled instability

The project distinguishes two regimes:

- **stability**: reproducible measurement of registered variants (the canonical apparatus);
- **instability**: explicitly downstream stress or transform regimes that are labeled, parameterized, and prevented from contaminating documentation.

This is the mechanism that allows the archive to tolerate “violence”: once provenance and measurement are sealed, aggressive downstream transformations become admissible without overwriting evidence.

---

## Sources (internal)

- [[A_World_Burning/01_audubon_dual_ledger]]
- [[A_World_Burning/24-etiquette]]
- [[A_World_Burning/33-appendix-b-filesystem-naming-run-ids]]
- [[A_World_Burning/09-emergence-of-the-burning-world]]

---

## Outline (preserved)
**Purpose:** name the project?s ontology and state transitions.

- V.1 Plate-centric identity (plate is atomic unit)
- V.2 Variant registration (variants attach to plates)
- V.3 Run as epistemic event (sealed, append-only, auditable)
- V.4 Ledger as derived view (fast, disposable; never authoritative)
- V.5 Stability vs controlled instability
  - V.5.a ?Stability? = reproducible measurement pipeline
  - V.5.b ?Instability? = downstream stress tests/transformations, explicitly labeled
- V.6 The archive tolerates violence: why provenance-first enables aggressive downstream work

