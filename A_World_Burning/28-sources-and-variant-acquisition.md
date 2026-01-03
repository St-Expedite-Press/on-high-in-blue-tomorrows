# Sources & Variant Acquisition (Exhaustive)

[[A_World_Burning/README]] | [[A_World_Burning/30-whitepaper-toc]] | [[A_World_Burning/32-appendix-a-corpus-and-source-registry]]

This document is the **source-side complement** to the extraction inventory: it enumerates what we might “go get”, how we register it, and how we avoid silently collapsing variance during acquisition.

It is written to support two modes:

- **Mode A (bootstrap, current):** one canonical source image per plate (435 total)
- **Mode B (true variance):** multiple variants per plate across institutions/digitizations/pipelines, all preserved and comparable

It is intentionally over-documented.

---

## 1. Current primary source (bootstrap corpus)

The current bootstrap corpus is derived from Nathan Buchar’s repository:

- Repo: `https://github.com/nathanbuchar/audubon-bird-plates`
- Raw files (as fetched at acquisition time):
  - `https://raw.githubusercontent.com/nathanbuchar/audubon-bird-plates/master/README.md`
  - `https://raw.githubusercontent.com/nathanbuchar/audubon-bird-plates/master/data.json`
- Shape: 435 plates, range-binned directories (e.g., `plates/1-99`, …)
- Credits requirement (as stated in the repo README):
  - “Courtesy of the John James Audubon Center at Mill Grove, Montgomery County Audubon Collection, and Zebra Publishing.”
- Terms reference (as stated in the repo README):
  - `https://www.audubon.org/terms-use`
- Plate download URLs are hosted at audubon.org (see `data.json` in the repo):
  - Pattern: `https://www.audubon.org/sites/default/files/boa_plates/plate-<N>-<slug>.jpg`

**Acquisition discipline note:** GitHub repositories and upstream hosts drift. When you ingest, record:

- repo branch name used (this repo uses `master`, not `main`)
- repo commit SHA at time of ingestion (example: `826e403a53d30eb48fcc0dfcd054f7ff4e1259d5` was the `master` head when this was checked)
- for each file: checksum + acquisition URL + access date

This turns “a GitHub repo” into a properly registered source.

**Key consequence:** even though the GitHub repo is a convenient wrapper, the “source-of-record” for the files is the audubon.org hosted plate image URLs referenced in `data.json`.

### 1.1 Concrete `data.json` record shape (bootstrap mapping contract)

Each entry in `data.json` provides the minimum crosswalk from plate identity to upstream URL. Example fields:

- `plate`: integer (1–435)
- `name`: human-readable title string
- `slug`: slugified title (used in URLs and filenames)
- `fileName`: canonical filename used in the repo
- `download`: the upstream file URL (audubon.org)

Example (plate 1 pattern, as seen in `data.json`):

- `plate`: `1`
- `name`: `Wild Turkey`
- `slug`: `wild-turkey`
- `fileName`: `plate-1-wild-turkey.jpg`
- `download`: `https://www.audubon.org/sites/default/files/boa_plates/plate-1-wild-turkey.jpg`

This record is the backbone of deterministic acquisition and plate mapping.

---

## 2. What counts as a “source” vs a “variant” (definitions)

### Source

A **source** is a provenance container: an institution/repository/scan campaign from which one or more plate images are acquired.

Minimum source fields:

- `source_id` (stable internal identifier)
- `source_name` (human-readable)
- `source_type` (repo / institutional digital collection / IIIF service / scan campaign / private)
- `source_homepage_url` (optional)
- `source_terms_url` (required if public)
- `credit_line_required` (required if known)
- `license_or_use_restrictions` (text + link(s))

### Variant

A **variant** is a specific digital image file that claims to depict a given plate (or a plate region) under some digitization regime.

Two files can be variants even if “the content is the same”:

- different resolution / crop / framing
- different color management pipeline
- different compression
- different restoration / cleaning
- different lighting / scanner

Minimum variant fields:

- `variant_id` (stable internal identifier)
- `plate_id` (or plate_number) mapping (may be provisional until verified)
- `source_id` (which source the file came from)
- acquisition metadata:
  - `acquired_at` (timestamp)
  - `acquired_by` (operator)
  - `acquisition_method` (download / IIIF / API / scrape / manual capture / scan)
  - `acquisition_url` (exact URL)
  - `access_date` (for mutable sources)
- integrity metadata:
  - `sha256` (required)
  - optional `xxhash64` (fast rechecks)
  - container fingerprints (format; progressive; ICC; quant tables, etc.)
- identity confidence:
  - `plate_match_method` (filename parse / embedded metadata / institutional catalog / manual)
  - `plate_match_confidence` (high/medium/low)
  - `plate_match_notes` (required if not high)

---

## 3. Source archetypes (where variants actually come from)

This is an explicit taxonomy so we don’t treat everything as “a URL”.

### 3.1 Curated repository wrappers (e.g., GitHub)

- Pros: stable file list; easy automation; often includes crosswalk metadata (like `data.json`)
- Risks:
  - repository can be updated without warning
  - files may be recompressed/re-exported
  - license terms may be outside the repo (as here: audubon.org terms)

Acquisition discipline:

- record the repo commit hash / tag used
- record the upstream URLs for every file if the repo is a mirror

### 3.2 Institution-hosted static images (direct file URLs)

- Pros: “official” image release point; stable URLs sometimes
- Risks:
  - silent updates (file replaced at same URL)
  - CDN behaviors (content negotiation; varying compression)

Acquisition discipline:

- always record access date
- optionally store HTTP response headers (ETag/Last-Modified) if available
- recheck periodically for drift

### 3.3 IIIF image services (recommended when available)

IIIF changes what “variant” means: you can request **the same source** at different sizes/regions, reproducibly.

- Pros:
  - deterministic region/size extraction
  - deep zoom capability
  - explicit service manifests
- Risks:
  - service policy changes; rate limits
  - “default” color conversions may still vary by server implementation

Acquisition discipline:

- store IIIF manifest URL
- store exact IIIF image request URLs used (region/size/rotation/quality)

Practical note (IIIF Image API mental model):

- canonical request pattern (IIIF Image API 2.x style):
  - `/iiif/2/<identifier>/<region>/<size>/<rotation>/<quality>.<format>`
- always record:
  - the full request URL
  - the returned bytes checksum
  - the manifest JSON checksum (and ideally store the manifest itself)

### 3.4 Bulk digital library search portals

These often provide derivative JPEGs; “original scan” may be gated.

- Pros: huge reach for discovering variants
- Risks: derivative-only; inconsistent metadata; ambiguous naming

Acquisition discipline:

- treat portal downloads as variants of variants
- attempt to locate the highest-fidelity downloadable master where possible

### 3.5 New scan campaigns (in-house or partner)

- Pros: maximal control + documentable conditions; can become gold-standard “canonical constraints”
- Risks: expensive; introduces new pipeline that must itself be documented as variance

Acquisition discipline:

- treat scan settings as first-class provenance (scanner model, illumination, ICC, raw outputs)
- preserve raw captures even if you also produce rendered derivatives

---

## 4. Source discovery (how to find candidate variants without contaminating the dataset)

This project should treat discovery as **non-authoritative** until provenance is registered.

Recommended discovery tactics:

- Start from known corpus metadata (plate number + title + slug)
- Search by plate number + “Audubon” + title string
- Search for plate thumbnails in institutional catalogs
- Search for IIIF manifests where available

Discovery output is *not* “data”; it is a queue:

- `discovery_queue.parquet` (or JSON) with fields:
  - query
  - candidate URL
  - source guess
  - discovered_at
  - discovered_by
  - notes

Only after a candidate passes acquisition + integrity does it enter the dataset as a variant.

---

## 5. Acquisition protocol (the “no silent variance collapse” procedure)

### 5.1 Always capture the policy environment

For every source, capture:

- Terms of Use URL (and ideally a stored snapshot)
  - `https://www.audubon.org/terms-use`
- Any credit line requirements (exact text)
- Any technical restrictions (rate limits; embargoes)

**Recommendation:** store a timestamped HTML snapshot for each terms page you rely on:

- `sources/<source_id>/terms/terms-use_<YYYYMMDD>.html`
- plus `sha256` of that snapshot

If the source is a repository wrapper (GitHub, etc.), also capture:

- repository URL
- branch or tag
- commit SHA
- file list (paths) and checksums

### 5.2 Always capture the acquisition transaction

For every downloaded file, record:

- request URL
- access date/time (UTC)
- response headers (ETag, Last-Modified, Content-Type, Content-Length) when available
- file checksum

### 5.3 Always capture file/container fingerprints

Record:

- format/container type
- progressive vs baseline JPEG
- chroma subsampling
- ICC profile presence + hash
- JPEG quant tables (hash or clustered ID)

Purpose: later you can cluster by pipeline (institution A vs institution B) even when images look similar.

### 5.4 Never “clean up” at acquisition time

Forbidden at acquisition:

- auto-rotate, auto-crop, auto-contrast
- recompressing to “standardize”
- stripping embedded profiles without recording

Acquisition must preserve the file as received. Normalization, if any, is a **derived run**.

---

## 6. Plate mapping / crosswalks (the identity problem)

### 6.1 Plate identity is canonical; filenames are not

Canonical internal identity:

- `plate_id = plate-###` (zero padded)
- `plate_number = 1..435`

External naming may vary wildly:

- different title spellings
- missing plate numbers
- alternate slugs
- partial crops of plates

### 6.2 Plate mapping methods (ordered by trust)

- (1) Direct plate number in institutional metadata → map to `plate_number`
- (2) Direct plate number in filename
- (3) Strong title/slug match (normalized string compare)
- (4) Visual match to known plate exemplar (embedding similarity) — *allowed for mapping only, not for truth*
- (5) Manual adjudication

If mapping is not high confidence, record it as provisional and do not merge into canonical plate truth without review.

---

## 7. Multi-variant storage patterns (how to extend beyond the bootstrap)

Current bootstrap assumes **exactly one** source image in `plate-###/source/`.

To support variance properly, you need one of these evolutions:

### Option A: Variant subdirectories under each plate

```
plate-###/
  variants/
    variant-0001/
      source/
        <original filename>
      variant.manifest.json
      source.sha256
```

Pros: all plate material co-located.  
Cons: plate directories become heavy; tooling must learn variants.

### Option B: Dataset-level variants store + pointers in plate manifests

```
variants/
  <variant_id>/
    source/...
    variant.manifest.json
```

Plate manifest stores `canonical_variant_id` (and/or pointers to all known variants).

Pros: avoids bloating plate dirs; clean separation.  
Cons: requires robust indexing and pointer discipline.

### Non-negotiable either way

- variants are immutable evidence
- canonical plate identity does not change
- derived runs are attached to (plate_id, variant_id) pairs

---

## 8. “Sources” beyond Audubon.org (what we should be prepared to ingest)

This is not an endorsement list; it is a preparedness list.

Candidate source classes to design for:

- institutional digital collections (often with search portals)
- IIIF services (best-case reproducibility)
- scanned book facsimiles (page-level variance; cropping issues)
- private scans (highest risk; best documentation required)

**Implementation note:** do not hardcode assumptions about:

- DPI metadata presence
- ICC profiles
- consistent naming
- stable URLs

### 8.1 Concrete discovery entrypoints (examples; not endorsements)

These URLs are useful *starting points* for discovering candidate variants or related holdings. They should feed the discovery queue, not the canonical registry directly.

- Library of Congress Prints & Photographs search:
  - `https://www.loc.gov/pictures/search/?q=Audubon%20Birds%20of%20America`
- NYPL Digital Collections search:
  - `https://digitalcollections.nypl.org/search/index?keywords=Audubon%20Birds%20of%20America`
- Biodiversity Heritage Library search:
  - `https://www.biodiversitylibrary.org/search?searchTerm=Birds%20of%20America%20Audubon`
- The Metropolitan Museum of Art collection search:
  - `https://www.metmuseum.org/art/collection/search?q=Audubon`

If any of these yield IIIF manifests or stable item identifiers, capture those as first-class source metadata (IIIF is the best-case reproducibility mode).

---

## 9. Audit deliverables (what makes the sources “publishable”)

At minimum, publish (or be able to publish privately):

- source registry (Appendix A in the whitepaper)
- variant registry (all files + checksums + mapping confidence)
- exclusion log (what you rejected and why)
- drift report (periodic rechecks of URLs + checksums where applicable)

---

## 10. Legal/credit discipline (operationally enforceable)

This must be machine-checkable, not “remembered”.

- store required credit line per source
- store terms URL and snapshot hash
- store license/restrictions text and any required attribution format
- ensure any exported dataset card includes this verbatim

---

## 11. Failure modes (source-side)

- Silent upstream file replacement at the same URL
- CDN or content negotiation changing file bytes over time
- Recompressed mirrors that erase provenance cues
- Ambiguous plate mapping leading to wrong plate associations
- “Helpful” normalization that destroys variance evidence

Mitigations:

- checksums + periodic drift rechecks
- container fingerprints
- explicit mapping confidence fields
- keep raw immutable artifacts; put normalization into runs
