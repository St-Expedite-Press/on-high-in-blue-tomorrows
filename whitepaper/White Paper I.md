The Burning World

**Canonical Digital Editions Under Conditions of Variance**

### Introduction

Digital editions of visual works are routinely constructed around a tacit assumption: that there exists a single image capable of standing in for the work as such. This assumption persists even when the historical object survives only as a distributed population of variants—multiple print states, conservation histories, institutional digitizations, color-management pipelines, resolutions, compressions, restorations, and derivative reproductions. In most contemporary workflows, these differences are either ignored, collapsed into an averaged representative, or treated as noise to be minimized. The result is a form of false authority: a canonical image that appears stable precisely because its internal variance has been suppressed.

_The Burning World_ begins from the premise that this suppression is no longer tenable. As digitization accelerates, archives proliferate, and computational systems increasingly rely on visual datasets for analysis, training, and interpretation, the question of what constitutes a “canonical” digital image becomes unavoidable. When similarity itself is operationalized—measured, embedded, clustered, and queried—the notion of a single authoritative image breaks down. What remains is not an image, but a space of variation.

This project proposes a different definition of canon. Here, “canonical” does not mean authoritative, final, or normative. It means formally constrained. A canonical digital edition, in this sense, is not a single file but a registered manifold: a bounded, well-documented space in which all known digital variants of a work are preserved, parameterized, and made comparable. Canonical status is attached not to an instance but to an infrastructure that renders difference legible rather than invisible.

The Audubon bird-plates corpus serves as the primary case study for this approach. The choice is methodological rather than symbolic. Audubon’s plates exist at the intersection of art, natural history, industrial reproduction, and environmental transformation. They have been digitized repeatedly by different institutions under divergent technical regimes, resulting in substantial variation in color, contrast, scale, damage visibility, and framing. This makes the corpus unusually well suited to testing a model of canon that does not rely on stability. Audubon functions here as a stress case: a corpus where suppressing variance produces misleading certainty, and where acknowledging variance forces a rethinking of editorial practice.

Methodologically, _The Burning World_ enforces a strict separation between documentation and interpretation. Ingestion is provenance-first and treats source images as immutable inputs. Feature extraction, embedding, and segmentation are conducted in sealed, reproducible runs that generate append-only artifacts. Interpretive or generative transformations—whether chromatic perturbations, counterfactual environmental stress tests, or hybrid ML workflows—are explicitly downstream and labeled as such. Machine learning is deployed not as an aesthetic engine or oracle of meaning, but as an epistemic instrument for modeling similarity, difference, and instability within a canonical system.

The title _The Burning World_ names the condition under which this work is situated. It refers not only to environmental crisis but to a broader instability affecting archives themselves: material decay, pigment drift, scanning artifacts, compression loss, and institutional divergence. Climate enters the project not as illustration or moral overlay, but as a controlled stress applied to a formally modeled archive. The question is not how images should look under collapse, but how canonical systems behave when stability can no longer be assumed.

This whitepaper lays out the conceptual framework, technical architecture, methodological discipline, and future extensions of _The Burning World_. It is intended to function simultaneously as an argument, a specification, and an infrastructural guide. Its audience includes digital humanists, computer vision researchers, archivists, editors, and technologists interested in building digital editions that do not erase variance in the name of authority.

---

## Table of Contents

**I. Scope, Audience, and Commitments**  
This section defines who the document is for, how it is intended to be used, and what kinds of claims it explicitly refuses to make. It establishes the ethical and epistemic boundaries within which the project operates.

**II. The Problem of Canon in Digital Visual Culture**  
An analysis of how single-image authority emerged as a default in digital editions, why this model persists, and how it fails in the presence of variant-rich corpora.

**III. Rethinking “Canonical”**  
A formal redefinition of canon as constraint rather than authority, including conceptual parallels to textual criticism and critical editions.

**IV. Case Study Selection: The Audubon Plates**  
A detailed justification of the corpus, including its historical production, digitization history, and methodological extremity.

**V. Conceptual Architecture of The Burning World**  
The ontological commitments of the project: plate-centric identity, variant registration, and the distinction between stability and controlled instability.

**VI. Data Ingestion and Provenance Control**  
How images enter the system, how provenance is preserved, and why immutability matters.

**VII. Feature Extraction and Measurement**  



**VIII. Segmentation Without Semantics**  
Why class-agnostic segmentation is used, and how it enables analysis without premature interpretation.

**IX. Reproducible Runs and Epistemic Discipline**  
Sealed runs, manifests, ledgers, and the infrastructure of auditability.

**X. Canon Under Stress: The Climate Frame**  
Environmental instability as methodological pressure rather than representational claim.

**XI. Interpretation Layers (Explicitly Downstream)**  
Where transformation begins, how it is labeled, and how it is prevented from contaminating documentation.

**XII. Canonical Query and Analysis**  
Similarity search, clustering, outliers, and the practical uses of a canonical manifold.

**XIII. Machine Learning as Instrument, Not Oracle**  
Limits of embeddings, model bias, and the refusal of automated authority.

**XIV. Editorial and Scholarly Implications**  
What this model means for citation, teaching, museums, and libraries.

**XV. Infrastructure and Storage Design**  
File systems, tables, vectors, and long-term preservation.

**XVI. Interfaces and Access Layers**  
How different audiences encounter the canon, and what is lost or gained at each layer.

**XVII. Failure Modes and Open Problems**  
Where this approach breaks, and why those breaks matter.

**XVIII. Roadmap and Extensions**  
Scaling beyond Audubon, interoperability, and governance.

**XIX. What This Project Refuses**  
A formal list of non-claims and prohibitions.

**XX. Conclusion: Canon After Stability**

---

## Appendices

The appendices are not supplementary in the casual sense; they are integral to the project’s claim to seriousness. They exist to ensure that nothing essential is left implicit, undocumented, or dependent on private knowledge.

### Appendix A: Corpus and Source Registry

This appendix provides a complete enumeration of the Audubon corpus used in _The Burning World_. Each plate is listed with stable internal identifiers, source repositories, institutional holdings, acquisition notes, digitization contexts where known, file formats, resolutions, and checksums. Crosswalks between institutional naming conventions are provided to prevent ambiguity. This appendix establishes, unambiguously, what the dataset is and what it is not.

### Appendix B: File System, Naming Conventions, and Run IDs

Here the disk-level ontology of the project is formalized. Directory structures, filename templates, run identifiers, versioning rules, and checksum practices are specified in detail. The goal is reconstructibility: a third party should be able to recreate the project’s structure and reasoning without oral tradition or ad hoc instruction. This appendix treats file organization as a form of argument.

### Appendix C: Feature Extraction Inventory

An exhaustive catalog of all computed features, including pixel statistics, color metrics, perceptual descriptors, embedding models, dimensionalities, normalization strategies, and output formats. Each feature family is accompanied by notes on what it captures, what it ignores, and known failure modes.

### Appendix D: Segmentation Methods and Parameters

Detailed documentation of segmentation approaches, including model versions, parameter settings, tiling strategies, post-processing steps, and rejection criteria. This appendix also explicitly states what semantic claims segmentation is _not_ intended to support.

### Appendix E: Reproducibility Protocols

A procedural account of how runs are sealed, how randomness is controlled, how manifests are generated, and how failures are logged. This appendix reads deliberately like a lab protocol, emphasizing discipline over novelty.

### Appendix F: Climate Perturbation Regimes

A precise definition of what “climate stress” means in computational terms within this project: parameter ranges, transformations, constraints, and prohibitions. By isolating this here, the main text avoids speculative drift.

### Appendix G: Ethical and Interpretive Guardrails

A formal articulation of the project’s refusals: no claims about original intent, no ecological forecasting, no restorative authority, no automated canon formation.

### Appendix H: Model Cards and Dependency Registry

A complete list of models, libraries, versions, licenses, and known biases. This appendix serves both epistemic and legal clarity.

### Appendix I: Known Limitations and Open Questions

A ledger of unresolved issues, including dataset gaps, institutional blind spots, model brittleness, and conceptual risks. This appendix demonstrates that uncertainty has been acknowledged rather than ignored.

### Appendix J: Glossary of Terms

Definitions for all loaded or technical terms used throughout the document, enforcing internal consistency and preventing incompatible external interpretations.

---

Taken together, the main body and appendices are designed to do two things at once: articulate a conceptual shift in how canonical digital editions are understood, and demonstrate—at exhaustive, sometimes tedious length—that this shift can survive implementation, critique, and reuse without collapsing into either mysticism or mere tooling.

If you want next, we can begin filling any single section at full length, or deliberately over-write one appendix to establish tone for the rest.