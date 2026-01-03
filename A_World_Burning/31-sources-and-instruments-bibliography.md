# Sources & Instruments Bibliography (Working, Exhaustive-ish)

[[A_World_Burning/README]] | [[A_World_Burning/30-whitepaper-toc]] | [[A_World_Burning/28-sources-and-variant-acquisition]]

This is a **working bibliography** of URLs and reference entrypoints used or implied by the current markdown corpus. It is not a literature review; it is a **provenance aid** for future appendices and audits.

---

## A. Primary corpus sources (Audubon bootstrap)

- Nathan Buchar repository wrapper: `https://github.com/nathanbuchar/audubon-bird-plates`
  - README (raw): `https://raw.githubusercontent.com/nathanbuchar/audubon-bird-plates/master/README.md`
  - Plate index (`data.json`, raw): `https://raw.githubusercontent.com/nathanbuchar/audubon-bird-plates/master/data.json`
  - Commit head lookup (API): `https://api.github.com/repos/nathanbuchar/audubon-bird-plates/commits/master`
- Audubon Birds of America landing: `https://www.audubon.org/birds-of-america`
- Audubon Terms of Use: `https://www.audubon.org/terms-use`
- Upstream plate URL pattern (from `data.json`):
  - `https://www.audubon.org/sites/default/files/boa_plates/plate-<N>-<slug>.jpg`

---

## B. Candidate discovery portals for additional variants (entrypoints only)

These are discovery entrypoints; they should populate a discovery queue, not the canonical registry directly.

- Library of Congress Prints & Photographs search:
  - `https://www.loc.gov/pictures/search/?q=Audubon%20Birds%20of%20America`
- NYPL Digital Collections search:
  - `https://digitalcollections.nypl.org/search/index?keywords=Audubon%20Birds%20of%20America`
- Biodiversity Heritage Library search:
  - `https://www.biodiversitylibrary.org/search?searchTerm=Birds%20of%20America%20Audubon`
- The Metropolitan Museum of Art collection search:
  - `https://www.metmuseum.org/art/collection/search?q=Audubon`

---

## C. “Strange” model instruments (Hugging Face examples)

These are examples referenced in `A_World_Burning/27-strange-models-compendium.md`. Treat them as candidates until licenses and biases are verified.

### C.1 Aesthetic predictors (CLIP-derived)

- `https://huggingface.co/shunk031/aesthetics-predictor-v1-vit-large-patch14`
- `https://huggingface.co/shunk031/aesthetics-predictor-v1-vit-base-patch16`
- `https://huggingface.co/camenduru/improved-aesthetic-predictor`

### C.2 Memorability

- `https://huggingface.co/PerceptCLIP/PerceptCLIP_Memorability`

### C.3 Art-historical (WikiArt)

- `https://huggingface.co/davanstrien/convnext-tiny-224-wikiart`
- `https://huggingface.co/prithivMLmods/WikiArt-Style`
- `https://huggingface.co/prithivMLmods/WikiArt-Genre`

### C.4 Emotion probes (image emotion classification; weak signal)

- `https://huggingface.co/jayanta/google-vit-base-patch16-224-cartoon-emotion-detection`
- `https://huggingface.co/jayanta/microsoft-resnet-50-cartoon-emotion-detection`
- `https://huggingface.co/imamassi/Visual_Emotional_Analysis`

---

## D. “Core stack” research references (papers / canonical model families)

This is a placeholder list for the eventual whitepaper references section; fill with stable citations as you lock models.

- CLIP (original paper; model family used for semantic alignment)
- DINOv2 (self-supervised structure embeddings)
- Segment Anything Model (SAM; class-agnostic mask generation)

---

## E. Protocol references (internal project materials)

- Source/variant discipline: `A_World_Burning/28-sources-and-variant-acquisition.md`
- Strange instruments catalog: `A_World_Burning/27-strange-models-compendium.md`
- Whitepaper skeleton: `A_World_Burning/26-whitepaper-skeleton.md`
- Extraction inventory: `A_World_Burning/00_preprocessing_assay.md`
