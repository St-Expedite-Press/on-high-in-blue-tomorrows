<!-- Auto-generated TOC-aligned file. Source of truth: A_World_Burning/26-whitepaper-skeleton.md -->

# I. Scope, Audience, and Commitments

[[whitepaper/DRAFT]] | [[whitepaper/MATERIALS_MAP]] | [[A_World_Burning/26-whitepaper-skeleton]]

_TOC-aligned entrypoint. Master outline lives in `A_World_Burning/26-whitepaper-skeleton.md`._


---

## Outline (preserved)

**Purpose:** define the boundaries of what this whitepaper asserts, how it will be evaluated, and what it refuses.

- I.1 Intended audiences and what each needs
- I.2 Definitions (canon, edition, variant, manifold, run, ledger, provenance)
- I.3 Evidence taxonomy and the ?no untagged claims? rule
- I.4 Epistemic separation doctrine: documentation vs interpretation vs transformation
- I.5 Ethics and guardrails (privacy/biometrics, institutional authority, restoration claims, environmental claims)
- I.6 Commitments to reproducibility (determinism where possible, logged nondeterminism where not)
- I.7 Commitments to long-term preservation (formats, checksums, rebuildability)
- I.8 Threat model / operational hygiene (secrets, accidental contamination, drift)

---

## Draft (body text)

This whitepaper is simultaneously:

- an argument: that “canon” for digital visual works must shift from **single-image authority** to a **bounded, comparable space of variants**;
- a specification: that canon becomes operational only through explicit constraints (identity, provenance, run sealing, naming);
- a protocol: that documentation, measurement, and interpretation must be separated so variance is preserved rather than erased.

The core claim is strict but not mystical: canonical status attaches to an **infrastructure** that makes difference legible, citeable, and auditable—not to a file that pretends to be stable.

### Evidence taxonomy (the “no untagged claims” rule)

To keep the boundary between documentation and interpretation explicit, every claim in this project should fall into one of these buckets:

- **[MEASURED]**: directly recorded from stored artifacts/ledgers/manifests.
- **[DERIVED]**: computed from measured fields; formula or procedure is stated.
- **[INTERPRETIVE]**: argumentative framing, critical reading, or humanities synthesis.
- **[SPECULATIVE / FUTURE WORK]**: proposals not yet implemented or validated.

### Separation doctrine (documentation vs interpretation vs transformation)

_The Burning World_ enforces an operational boundary:

- **Documentation**: acquisition + provenance + immutability constraints.
- **Measurement**: extraction/segmentation/embedding runs (sealed, versioned, append-only).
- **Interpretation**: scholarly argument and reading of patterns in measured space.
- **Transformation**: pixel-altering, counterfactual, or generative procedures (explicitly downstream and labeled).

### Refusals (what the canon will not claim)

Canonical infrastructure is powerful; the project explicitly refuses:

- claims of “restoring” the true original appearance;
- ecological forecasting presented as documentary evidence;
- automated canon formation (“the model says this is canonical”).

See: [[A_World_Burning/38-appendix-g-ethical-and-interpretive-guardrails]] and Section XIX.

---

## Sources (internal)

- [[A_World_Burning/26-whitepaper-skeleton]]
- [[A_World_Burning/24-etiquette]]
- [[A_World_Burning/38-appendix-g-ethical-and-interpretive-guardrails]]
- [[A_World_Burning/36-appendix-e-reproducibility-protocols]]
- [[A_World_Burning/33-appendix-b-filesystem-naming-run-ids]]
