# Appendix F: Climate Perturbation Regimes (Downstream Stress Definition)

[[A_World_Burning/README]] | [[A_World_Burning/30-whitepaper-toc]] | [[A_World_Burning/26-whitepaper-skeleton]]

This appendix defines what “climate stress” means **computationally** in _The Burning World_. It exists to keep the main text honest: stress transforms are downstream of documentation runs, parameterized, and auditably constrained.

Core separation (non-negotiable):

- ingestion + measurement runs produce documentation artifacts (canonical manifold)
- stress runs produce interpretive/transform artifacts (explicitly downstream)

Related:

- Run sealing discipline: `33-appendix-b-filesystem-naming-run-ids.md`
- Measurement inventory: `34-appendix-c-feature-extraction-inventory.md`
- Segmentation discipline (for localized stress): `35-appendix-d-segmentation-methods-and-parameters.md`

---

## F.1 What “climate stress” is (in this project)

Climate stress is a set of **parameterized image perturbations** used as methodological pressure:

- to test how canonical systems behave under instability
- to measure robustness and drift in embeddings/segmentations under controlled change
- to make variance visible, rather than pretending the archive is stable

It is not:

- a claim about what historically happened to a specific plate
- a forecast or ecological model
- a restoration or correction pipeline

---

## F.2 Stress axes (define the knobs; do not improvise)

Each stress regime is defined as a vector of parameters. Example axes (conceptual families):

### F.2.1 Chromatic stress

- temperature shift (warm/cool)
- selective pigment fade (channel- or band-weighted attenuation)
- paper yellowing / tanning (global or border-weighted)

### F.2.2 Atmospheric stress

- haze/ash veil (contrast compression + color cast + low-frequency fog)
- soot deposition (darkening + texture overlay)
- particulate speckling (stochastic but seeded)

### F.2.3 Luminance/contrast collapse

- dynamic range compression (tone curve)
- localized contrast loss (region- or tile-based)

### F.2.4 Material decay proxies (archive instability, not “climate truth”)

- foxing-like spot fields (parametric, seeded)
- edge fray / paper wear (border-weighted erosion)
- compression re-encoding stress (pipeline fingerprint perturbation)

### F.2.5 Geometric instability (used sparingly; high-risk)

- slight warps (page curl proxy)
- micro-misalignment / scan skew (small rotations, translations)

Geometric stress must be tightly bounded; it can destroy comparability if it is not logged and constrained.

---

## F.3 Localizing stress (segmentation-conditional regimes)

One distinctive methodological move in this project is to apply stress **conditionally**:

- background/paper can decay differently than bird/flora
- inscriptions can be excluded from stress or stressed separately

Requirements:

- if you localize stress, you must cite the segmentation run(s) used
- the stress run manifest must record which masks/regions were used and how

---

## F.4 Safeguard constraints (prevent semantic fabrication)

Stress runs must be bounded by safeguards that are measurable.

### F.4.1 Prohibitions (hard)

- no new anatomy (no invented limbs/beaks/birds)
- no “restoration” claims
- no replacing missing content with hallucinated content

### F.4.2 Measurable guardrails (recommended)

Guardrails are stored as metrics per transformed image:

- edge preservation:
  - compare edge maps (Canny/Sobel) original vs stressed; record an overlap score
- embedding drift ceilings:
  - compute cosine distance in at least two embedding spaces (e.g., CLIP + DINOv2)
  - record drift; optionally enforce max drift for “documentation-adjacent” stress modes
- segmentation stability:
  - measure how mask topology changes (mask count distribution, fragmentation)

The key is not to prevent change; it is to prevent undocumented, uncontrolled change.

---

## F.5 Run logging requirements (stress runs are still runs)

Every stress regime run must record:

- `run_id` (as usual)
- transform family (e.g., `climate/haze`, `climate/pigment_fade`)
- parameter vector (full, not summarized)
- random seed(s)
- input identity:
  - plate_id, variant_id (if applicable)
  - input checksum(s)
- outputs + checksums
- safeguard metrics (edge preservation, drift stats)

Output naming law still applies:

`<plate_id>__<run_id>__<artifact_type>__<descriptor>.<ext>`

Example descriptors:

- `climate-haze-alpha0p35`
- `paper-yellowing-k0p12`

---

## F.6 Regime catalog (how to keep this from drifting)

Maintain a registry of stress regimes (versioned, like prompts):

- regime_id
- regime_name
- parameter schema
- allowed ranges
- notes (what it is meant to test)
- version + created_at

Do not edit regimes in place without bumping version.
