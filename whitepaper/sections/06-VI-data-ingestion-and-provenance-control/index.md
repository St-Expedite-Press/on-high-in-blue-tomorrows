<!-- Auto-generated TOC-aligned file. Source of truth: A_World_Burning/26-whitepaper-skeleton.md -->

# VI. Data Ingestion and Provenance Control

[[whitepaper/DRAFT]] | [[whitepaper/MATERIALS_MAP]] | [[A_World_Burning/28-sources-and-variant-acquisition]] | [[A_World_Burning/32-appendix-a-corpus-and-source-registry]]

_TOC-aligned entrypoint. Master outline lives in `A_World_Burning/26-whitepaper-skeleton.md`._

---

## Draft (body text)

Ingestion is where canon either begins honestly or begins by erasure. _The Burning World_ treats ingestion as provenance-first and failure-intolerant: sources are registered before computation, and source images become immutable evidence.

### VI.1 Acquisition pathways (bootstrap vs variance mode)

- **Bootstrap mode (current)**: one canonical source image per plate, acquired via a repository wrapper (e.g., GitHub) that points to upstream audubon.org URLs.
- **Variance mode (target)**: multiple institutional digitizations and derivative reproductions per plate, each admitted as a registered variant with explicit provenance.

The key operational move is to treat convenience wrappers (like GitHub repos) as registrable sources, not as implicit truth: commit hash, access date, and per-file checksums become part of the record.

### VI.2 Source + variant registration (minimum fields)

At minimum, ingestion records:

- who/what the source is (institution, repo, scan campaign),
- the exact acquisition method and URL,
- access date (for mutable endpoints),
- rights/credit restrictions where known,
- cryptographic integrity checks (SHA-256).

These are non-negotiable because they prevent silent drift and allow reproducible re-acquisition.

See: [[A_World_Burning/32-appendix-a-corpus-and-source-registry]] and [[A_World_Burning/28-sources-and-variant-acquisition]].

### VI.3 Integrity verification (beyond “file exists”)

Canon under variance requires that ingestion record not only bytes but also container-level fingerprints that help diagnose pipeline differences:

- format/container metadata (JPEG vs TIFF, progressive/baseline, ICC presence),
- compression fingerprints (quantization tables, size ratios),
- exact hashes (sha256) and optional fast hashes (xxhash64),
- optional perceptual hashes for near-duplicate graphs.

These signals support deduping, provenance forensics, and later arguments about institutional digitization bias.

### VI.4 Immutability rules (how evidence stays evidence)

- Source images are never overwritten.
- Corrections occur only as:
  - new variants (new provenance containers), or
  - new runs (new derived artifacts).

Immutability is what makes aggressive downstream work admissible: once evidence is preserved, transformation can be daring without being dishonest.

### VI.5 Drift detection (sources change; the system must notice)

Because URLs and repositories drift, ingestion includes drift detection:

- periodic re-validation of checksums for any “same URL” fetches,
- optional capture of HTTP metadata (ETag/Last-Modified) when available,
- explicit logging of “this source changed” as an event.

---

## Sources (internal)

- [[A_World_Burning/28-sources-and-variant-acquisition]]
- [[A_World_Burning/32-appendix-a-corpus-and-source-registry]]
- [[A_World_Burning/33-appendix-b-filesystem-naming-run-ids]]

---

## Outline (preserved)
**Purpose:** define how images enter, how they are frozen, and how they remain trustworthy.

- VI.1 Acquisition pathways (download, institutional pulls, existing repositories)
- VI.2 Source registry requirements (Appendix A)
  - VI.2.a Source URL / institution / holding record
  - VI.2.b Acquisition timestamp and operator
  - VI.2.c License/credit record + restrictions
- VI.3 Integrity verification
  - VI.3.a Cryptographic checksums (sha256; optional xxhash)
  - VI.3.b Dedup detection (exact + near-duplicate signals)
  - VI.3.c File/container fingerprints (quant tables, ICC presence, progressive/baseline)
- VI.4 Immutability rules
  - VI.4.a Source images never overwritten
  - VI.4.b Corrections occur only as new variants or new runs
- VI.5 Drift detection (re-validate manifest/schema/checksum)
- VI.6 Variant acquisition discipline (explicit protocol)
  - see: `A_World_Burning/28-sources-and-variant-acquisition.md`
