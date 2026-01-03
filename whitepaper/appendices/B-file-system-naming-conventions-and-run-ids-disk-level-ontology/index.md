<!-- Auto-generated TOC-aligned file. Source of truth: A_World_Burning/26-whitepaper-skeleton.md -->

# Appendix B: File System, Naming Conventions, and Run IDs (disk-level ontology)

_Rendered appendix lives in `A_World_Burning/33-appendix-b-filesystem-naming-run-ids.md`._

_TOC-aligned entrypoint. Master outline lives in `A_World_Burning/26-whitepaper-skeleton.md`._


Rendered in: `A_World_Burning/33-appendix-b-filesystem-naming-run-ids.md`

**Goal:** reconstructibility; file organization as argument.

- B.1 Canonical directory map (current vs planned evolution; decision recorded)
- B.2 Naming law
  - B.2.a plate directories: `plate-###` only
  - B.2.b run directories: chosen run_id scheme; collision rules
  - B.2.c derived artifacts: `<plate_id>__<run_id>__<artifact_type>__<descriptor>.<ext>`
- B.3 Plate manifest schema (full field list + constraints)
- B.4 Run manifest schema (full field list + constraints)
- B.5 Checksum strategy
  - B.5.a `source.sha256` per plate/variant
  - B.5.b optional per-run `run.sha256`
- B.6 Validators (filesystem + schema + run sealing)
- B.7 Ledger rebuild contract (how to regenerate parquet from plate truth)

