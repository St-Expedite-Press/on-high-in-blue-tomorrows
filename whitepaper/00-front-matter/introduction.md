# Introduction

Primary introduction seed: `White Paper I.md`

Expanded whitepaper outline (includes the working introduction text): `A_World_Burning/26-whitepaper-skeleton.md`

---

## Draft Introduction (current working text)

Digital editions of visual works are routinely constructed around a tacit assumption: that there exists a single image capable of standing in for the work as such. This assumption persists even when the historical object survives only as a distributed population of variants—multiple print states, conservation histories, institutional digitizations, color-management pipelines, resolutions, compressions, restorations, and derivative reproductions. In most contemporary workflows, these differences are either ignored, collapsed into an averaged representative, or treated as noise to be minimized. The result is a form of false authority: a canonical image that appears stable precisely because its internal variance has been suppressed.

_The Burning World_ begins from the premise that this suppression is no longer tenable. As digitization accelerates, archives proliferate, and computational systems increasingly rely on visual datasets for analysis, training, and interpretation, the question of what constitutes a “canonical” digital image becomes unavoidable. When similarity itself is operationalized—measured, embedded, clustered, and queried—the notion of a single authoritative image breaks down. What remains is not an image, but a space of variation.

This project proposes a different definition of canon. Here, “canonical” does not mean authoritative, final, or normative. It means formally constrained. A canonical digital edition, in this sense, is not a single file but a registered manifold: a bounded, well-documented space in which all known digital variants of a work are preserved, parameterized, and made comparable. Canonical status is attached not to an instance but to an infrastructure that renders difference legible rather than invisible.

The Audubon bird-plates corpus serves as the primary case study for this approach. The choice is methodological rather than symbolic. Audubon’s plates exist at the intersection of art, natural history, industrial reproduction, and environmental transformation. They have been digitized repeatedly by different institutions under divergent technical regimes, resulting in substantial variation in color, contrast, scale, damage visibility, and framing. This makes the corpus unusually well suited to testing a model of canon that does not rely on stability. Audubon functions here as a stress case: a corpus where suppressing variance produces misleading certainty, and where acknowledging variance forces a rethinking of editorial practice.

Methodologically, _The Burning World_ enforces a strict separation between documentation and interpretation. Ingestion is provenance-first and treats source images as immutable inputs. Feature extraction, embedding, and segmentation are conducted in sealed, reproducible runs that generate append-only artifacts. Interpretive or generative transformations—whether chromatic perturbations, counterfactual environmental stress tests, or hybrid ML workflows—are explicitly downstream and labeled as such. Machine learning is deployed not as an aesthetic engine or oracle of meaning, but as an epistemic instrument for modeling similarity, difference, and instability within a canonical system.

The title _The Burning World_ names the condition under which this work is situated. It refers not only to environmental crisis but to a broader instability affecting archives themselves: material decay, pigment drift, scanning artifacts, compression loss, and institutional divergence. Climate enters the project not as illustration or moral overlay, but as a controlled stress applied to a formally modeled archive. The question is not how images should look under collapse, but how canonical systems behave when stability can no longer be assumed.

This whitepaper lays out the conceptual framework, technical architecture, methodological discipline, and future extensions of _The Burning World_. It is intended to function simultaneously as an argument, a specification, and an infrastructural guide. Its audience includes digital humanists, computer vision researchers, archivists, editors, and technologists interested in building digital editions that do not erase variance in the name of authority.
