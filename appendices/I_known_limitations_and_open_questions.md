# Appendix I: Known Limitations and Open Questions (Ledger of Uncertainty)

[[A_World_Burning/README]] | [[A_World_Burning/30-whitepaper-toc]] | [[A_World_Burning/26-whitepaper-skeleton]]

This appendix is a deliberately explicit ledger of what remains uncertain, brittle, or undecided. It exists to demonstrate that uncertainty has been documented rather than ignored.

Related:

- Source/variant acquisition discipline: `28-sources-and-variant-acquisition.md`
- Feature inventory: `34-appendix-c-feature-extraction-inventory.md`
- Model registry and license posture: `29-model-library.md`, `39-appendix-h-model-cards-and-dependency-registry.md`

---

## I.1 Dataset boundary and mapping risks

- **Plate identity mapping across institutions**: variant acquisition will eventually require crosswalks between naming conventions, plate numbers, and titles. Ambiguous matches must be logged as such.
- **Bootstrap single-source bias**: the initial corpus is one digitization per plate; variance mode requires expanding sources to avoid conflating “plate identity” with “one pipeline.”
- **Mutable upstream sources**: institutional hosting may silently replace bytes; drift detection must be operational, not aspirational.

---

## I.2 Geometry policy is destiny (and still partially open)

Decisions that shape almost everything downstream:

- border policy (keep borders vs crop-to-content)
- working-resolution policy (do we standardize at 2k/4k? tile only outliers?)
- rotation/deskew policy (do we normalize orientation?)

Open question:

- Which of these are “documentation constraints” vs “analysis conveniences”?

---

## I.3 Segmentation brittleness (Audubon adversarial textures)

Known issues:

- engraving texture causes mask fragmentation
- paper tone and borders become dominant regions
- text inscriptions are repeatedly proposed as objects

Open questions:

- What is the minimal segmentation policy that enables robust region-level measurement without becoming a semantic pipeline?
- What pruning policy is defensible (and how to document it as such)?

---

## I.4 Embedding bias and instability

Known issues:

- different embedding families disagree on neighborhood structure
- framing and border content can dominate semantic embeddings
- embeddings drift under minor resampling or color management changes

Open questions:

- What constitutes “stable” structure across embedding families?
- How should “disagreement” be stored and surfaced (as a first-class phenomenon, not noise)?

---

## I.5 OCR and text handling (optional, but method-shaping)

Known issues:

- OCR can misread engraving texture
- extracting inscriptions introduces additional policies (text region detection, language handling)

Open questions:

- Is inscription text a research axis (binomials, naming) or a nuisance region to be masked?
- If it is included, do we treat it as part of the canonical manifold or as a parallel weak-label layer?

---

## I.6 Licensing and redistribution constraints

Known issues:

- some models declare unknown licenses in HF metadata
- some segmentation checkpoints declare `license:other`
- some probe models are distributed without clear licensing

Open questions:

- Which models are admissible for a publicly released dataset vs only for internal research runs?
- How should “license unknown” be handled (block usage vs allow but mark non-redistributable artifacts)?

---

## I.7 Storage and long-term preservation

Known issues:

- plate-centric truth scales well for 435 plates, but future corpora may not
- Parquet ledgers are rebuildable but require consistent schema versioning

Open questions:

- What is the long-term packaging target (Parquet bundles, WebDataset, IIIF)?
- What is the “frozen release artifact” definition for a published edition?

---

## I.8 Governance and revision policy

Known issues:

- canon-as-infrastructure implies ongoing revision (new variants, new instruments)

Open questions:

- Who is allowed to add variants? under what documentation requirements?
- What constitutes a “breaking change” to the canon (schema bump, new IDs, new constraints)?

---

## I.9 Evaluation: what benchmarks are legitimate?

Known issues:

- standard CV benchmarks don’t map cleanly to engraving plates
- “success” is not classification accuracy; it is variance legibility + auditability

Open questions:

- Which quantitative figures best demonstrate that variance is being preserved rather than collapsed?
- What ablations are mandatory for publication (whole vs segmented embeddings, cross-model neighbor overlap, drift under stress)?
