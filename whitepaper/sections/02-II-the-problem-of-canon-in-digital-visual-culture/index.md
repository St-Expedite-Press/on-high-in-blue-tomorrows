<!-- Auto-generated TOC-aligned file. Source of truth: A_World_Burning/26-whitepaper-skeleton.md -->

# II. The Problem of Canon in Digital Visual Culture

[[whitepaper/DRAFT]] | [[whitepaper/MATERIALS_MAP]] | [[A_World_Burning/26-whitepaper-skeleton]]

_TOC-aligned entrypoint. Master outline lives in `A_World_Burning/26-whitepaper-skeleton.md`._


**Purpose:** show why ?single-image canon? became default and why it fails under variance.

- II.1 The tacit single-file assumption as editorial inheritance
- II.2 Varieties of variance (enumerate)
  - II.2.a Print states and production differences
  - II.2.b Conservation histories and material changes
  - II.2.c Institutional digitization divergence (equipment + lighting + profiles)
  - II.2.d Computational postprocessing divergence (color management, sharpening, denoise)
  - II.2.e Resolution, framing, cropping, rotation, page borders
  - II.2.f Compression regimes, container rewrites, downsampling artifacts
  - II.2.g Restoration and derivative reproductions (with/without disclosure)
- II.3 Consequences of suppression
  - II.3.a False authority and the invisibility of editorial choice
  - II.3.b Dataset contamination and model behavior (training leakage, bias)
  - II.3.c Scholarly citation ambiguity (what exact image was referenced?)
  - II.3.d Conservator blind spots (damage visibility depends on pipeline)
- II.4 Prior art / parallels (textual criticism, critical editions, stemmatics, apparatus)

---

## Draft (body text)

Digital visual editions inherit a default that made sense in print culture: an edition presents a work as a stable object, and an image stands in for the work. In a variant-rich visual corpus, this convenience becomes an epistemic error: it makes an editorial selection look like an ontological fact.

### II.1 The tacit single-file assumption

Even when projects acknowledge that multiple scans or print states exist, workflows often converge back to a single “representative” image:

- the best-looking scan becomes the de facto canonical rendering;
- other scans become “duplicates” or “noise”;
- differences are treated as technical defects rather than evidence of digitization regimes.

This is not malicious; it is a side effect of file-based publishing and catalog norms. But as soon as similarity is computed (embeddings, clustering, retrieval), the suppressed variance returns as measurable instability.

### II.2 What “variance” includes (and why it matters)

Variance is not one thing. It includes:

- **production variance** (print states, hand-coloring differences, plate wear);
- **material variance** (conservation interventions, pigment drift, paper aging);
- **digitization variance** (lighting, scanner/lens, ICC profiles, white balance);
- **pipeline variance** (sharpening/denoise, background cleanup, compression);
- **framing variance** (crop, rotation, borders, annotations, scale);
- **distribution variance** (re-exports, downsampling, re-compression chains).

Treating these differences as “noise” hides what kind of evidence is being erased. Some variance is about the historical object; some variance is about the digitization pipeline; both can be methodologically meaningful.

### II.3 Why suppression produces false authority

Collapsing variance into a single image produces several downstream failures:

- **citation ambiguity**: what exact rendering was referenced?
- **editorial invisibility**: what choices were made to produce “the” image?
- **dataset contamination**: near-duplicates and pipeline artifacts leak into training/evaluation.
- **conservation blind spots**: damage visibility can depend on lighting/contrast regimes.

The whitepaper’s claim is that canon under variance is not “choose better”—it is “stop pretending choice disappears.”

### II.4 Parallels (and mismatches) with textual criticism

Textual criticism treats variants as evidence, preserved through apparatus and stemmatics. Visual editions share the need for an apparatus, but differ in a crucial way: visual variance is continuous and high-dimensional, and often entangled with digitization pipelines. This project borrows the editorial discipline of apparatus while refusing the single-text convergence model.

---

## Sources (internal)

- [[A_World_Burning/25-reel-it-in]]
- [[A_World_Burning/26-whitepaper-skeleton]]
- [[A_World_Burning/28-sources-and-variant-acquisition]]
