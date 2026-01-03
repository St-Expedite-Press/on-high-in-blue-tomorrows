<!-- Auto-generated TOC-aligned file. Source of truth: A_World_Burning/26-whitepaper-skeleton.md -->

# Appendix C: Feature Extraction Inventory (complete; no omissions)

_Rendered appendix lives in `A_World_Burning/34-appendix-c-feature-extraction-inventory.md`._

_TOC-aligned entrypoint. Master outline lives in `A_World_Burning/26-whitepaper-skeleton.md`._


Rendered in: `A_World_Burning/34-appendix-c-feature-extraction-inventory.md`

**Goal:** exhaustive list of computed features, with what they capture and fail to capture.

This appendix should mirror the extraction inventory in `A_World_Burning/00_preprocessing_assay.md` but in a ?paper-ready? form:

- C.1 Feature families (File/container; global pixel; CV; embeddings; segmentation; OCR; captions; forensics; quality; indices)
- C.2 For each feature family, specify:
  - C.2.a purpose (what question it answers)
  - C.2.b computational regime (CPU/GPU; full-pass vs sampled vs tiled)
  - C.2.c output shape/schema (fields, dimensionality, normalization)
  - C.2.d storage location (plate-local vs ledger)
  - C.2.e known failure modes and bias
- C.3 Full enumerated inventory (copy the numbered list 1?45, verbatim or as a strict mapping)
- C.4 Versioning policy (what requires a schema bump; what is additive)

