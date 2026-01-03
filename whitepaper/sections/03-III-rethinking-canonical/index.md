<!-- Auto-generated TOC-aligned file. Source of truth: A_World_Burning/26-whitepaper-skeleton.md -->

# III. Rethinking ?Canonical?

[[whitepaper/DRAFT]] | [[whitepaper/MATERIALS_MAP]] | [[A_World_Burning/26-whitepaper-skeleton]]

_TOC-aligned entrypoint. Master outline lives in `A_World_Burning/26-whitepaper-skeleton.md`._

---

## Draft (body text)

This project uses “canonical” in a deliberately non-standard way. Canonical does **not** mean final, authoritative, pristine, or normatively correct. It means **formally constrained**: bounded enough that variants can be preserved, compared, cited, and audited without collapsing into a single representative file.

### III.1 Canon as constraint, not authority

The single-image canon is a stability illusion: it looks authoritative precisely because it suppresses internal variance. _The Burning World_ treats that suppression as methodologically untenable. Instead of canon = “the image,” we propose canon = “the rules that make images comparable.”

Canonical status therefore attaches to:

- stable identity (what counts as the same plate/work);
- provenance registration (where a file came from, under what terms, with what integrity checks);
- sealed computation (how measurements were produced, with which versions and parameters).

### III.2 Canonical digital editions as registered manifolds

A canonical edition is not a single file. It is a registered manifold:

- a set of **variants** (files) admitted under explicit provenance constraints;
- a set of **measured axes** (features, segments, embeddings) produced by sealed runs;
- a set of **query operations** (similarity, clustering, outliers) that operate on the measured space.

What makes it canonical is not completeness in any metaphysical sense; it is that the manifold is **bounded and documented**.

### III.3 What counts as a “variant” vs what counts as “registered”

- A **variant** is any specific digital file that claims to depict the plate, even if it differs only in crop, compression, ICC profile, or restoration.
- A **registered variant** is a variant admitted with minimum provenance fields: source attribution, acquisition method, access date, and checksums (plus whatever rights/terms are required).

This distinction prevents discovery artifacts (random URLs, screenshots, uncontrolled derivatives) from silently becoming “data.”

### III.4 Editorial consequences: apparatus becomes primary

Once canon is a manifold, editorial practice changes:

- Citation becomes a path: plate identity + variant identity + (optionally) run identity.
- “Best image” becomes a query result under declared criteria, not an editorial decree.

---

## Sources (internal)

- [[A_World_Burning/25-reel-it-in]]
- [[A_World_Burning/28-sources-and-variant-acquisition]]
- [[A_World_Burning/33-appendix-b-filesystem-naming-run-ids]]
- [[A_World_Burning/32-appendix-a-corpus-and-source-registry]]

---

## Outline (preserved)
**Purpose:** define canon as constraint + infrastructure rather than authority.

- III.1 Canonical ? normative: canon as bounded space, not final image
- III.2 Canonical digital edition as a registered manifold
  - III.2.a What counts as a ?variant? (definition + minimum metadata)
  - III.2.b What counts as ?registered? (constraints + documentation)
  - III.2.c Parameterization: axes not knobs (link to parameter discipline)
- III.3 Canonical constraints
  - III.3.a Identity constraints (stable IDs; non-negotiable mapping)
  - III.3.b Provenance constraints (checksums + source registry)
  - III.3.c Process constraints (sealed runs; append-only; validators)
  - III.3.d Representation constraints (storage doctrine: artifacts/facts/perception/meaning)
- III.4 Editorial consequences: the apparatus becomes primary
  - III.4.a Citation becomes a path in the manifold (plate_id + variant_id/run_id)
  - III.4.b ?Best image? becomes a query result, not an editorial decree
