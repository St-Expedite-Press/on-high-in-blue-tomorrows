<!-- Auto-generated TOC-aligned file. Source of truth: A_World_Burning/26-whitepaper-skeleton.md -->

# Appendix J: Glossary of Terms (enforced internal consistency)

_TOC-aligned entrypoint. Master outline lives in `A_World_Burning/26-whitepaper-skeleton.md`._


**Goal:** prevent incompatible readings by defining loaded terms.

- plate, variant, run, manifest, ledger
- canonical, edition, manifold, apparatus
- provenance, immutability, auditability
- measurement vs interpretation vs transformation
- semantic drift, robustness curve, stability, failure mode

---

## 5. ?Absurdly Exhaustive? Checklists (author-facing, optional in published version)

These are working checklists; they may be moved into a private/internal appendix, but they must exist.

### 5.1 Preprocessing completeness checklist

- All plates registered; manifests valid; sources checksummed
- Baseline scalar facts extracted and stored
- Optional distributions decided (on/off) and documented
- Segmentation executed or explicitly deferred
- Embeddings executed (global; optional segment/tile)
- Ledgers built and rebuildable from plate-local truth
- QC atlas generated; known failures logged

### 5.2 ?No silent failure? checklist (per notebook/run)

- Structure assertion ran before any compute
- Config declared and hashed
- All outputs registered in manifest
- Post-run validation succeeded
- Ledger sync updated
- Run sealed (status complete + checksums recorded)

### 5.3 Citation checklist (for scholarship)

- If citing a source variant: include source registry ID + checksum + access date
- If citing a derived measurement: include run_id + config hash + model IDs + ledger version
- If citing a transformation: include transform run_id + parameter set + safeguard metrics
