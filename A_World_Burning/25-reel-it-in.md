# Reel It In (Publishable Paper Galaxy)

Below is a structured _galaxy_ of publishable papers that radiate outward from the same core claim: **the canonical artwork in the digital age is a registered, parameterized field of variants rather than a singular image or file**. I'll group them by disciplinary gravity and indicate likely venues (including arXiv where appropriate).

---

**I. Foundational / Theory-Defining Papers (the trunk)**

1. _From Edition to Manifold: Redefining the Canonical Artwork in Digital Space_  
    A theoretical paper arguing that “edition” is the wrong abstraction for digital artworks. Proposes a manifold model: geometry + parameter space + admissible transformations. Anchors in Benjamin, Goodman, McGann, but advances beyond textual theory into continuous domains (images, sound).  
    Venues: DHQ, Leonardo, Critical Inquiry; arXiv (cs.DL + humanities crossover).
    
2. _Authority Without Fixity: Canonical Status in Parameterized Cultural Objects_  
    Addresses editorial authority once no single rendering is privileged. Distinguishes canonical _structure_ from canonical _appearance_. Introduces governance models (curated parameter bounds, conservation-informed constraints).  
    Venues: Journal of Cultural Analytics, Digital Scholarship in the Humanities.
    

---

**II. Infrastructure & Systems Papers (the load-bearing layer)**

3. _The Canonical Stack: A Systems Architecture for Registered Variant Artworks_  
    Defines a reference architecture: spatial registration, variant ingestion, parameter schemas, rendering layer, provenance tracking. Shows how existing tools (IIIF-like tiling, graph DBs, render pipelines) are insufficient unless unified.  
    Venues: arXiv (cs.DL, cs.MM), ACM JOCCH.
    
4. _Geometry as Ground Truth: Multi-Scan Registration for Cultural Heritage Objects_  
    A technical paper on aligning heterogeneous scans (different lenses, lighting, color profiles, resolutions) into a single canonical coordinate system. Focus on error metrics, drift, and tolerances.  
    Venues: arXiv (cs.CV), IEEE ICIP, ISPRS journals.
    

---

**III. Conservation & Material Studies Papers (where museums listen)**

5. _Canonical Does Not Mean Pristine: Encoding Conservation States as First-Class Variants_  
    Argues that restoration stages, pigment decay models, and lighting conditions should be parameters, not overwritten “updates.” Frames conservation as expanding the manifold, not converging on an image.  
    Venues: Studies in Conservation, Leonardo.
    
6. _Spectral Truth and Editorial Restraint: Multispectral Imaging in Canonical Digital Editions_  
    Uses multispectral and hyperspectral scans to argue that RGB images are editorial reductions. Proposes spectral axes as navigable parameters.  
    Venues: Heritage Science, Journal of Imaging; arXiv (physics.optics + cs.CV).
    

---

**IV. Computational Humanities / Method Papers (credibility multipliers)**

7. _Variant-Centric Scholarship: Querying Artworks as Parameter Spaces_  
    Demonstrates new research questions enabled by the model: “show all renderings maximizing craquelure visibility,” “compare edge contrast across decades of digitization.” Emphasizes epistemic gain.  
    Venues: DHQ, Digital Humanities Conference proceedings.
    
8. _Against the ‘Best Image’: Quantifying Bias in Museum Digitization Pipelines_  
    Empirical study showing how institutional preferences (lighting, color correction, compression) systematically bias interpretation. Uses registered variants to measure divergence.  
    Venues: Journal of Cultural Analytics; arXiv (cs.DL).
    

---

**V. Legal, Ethical, and Institutional Papers (the political flank)**

9. _Who Owns the Canonical Manifold? Copyright, Derivatives, and Parameterized Art_  
    Explores how copyright law breaks when no single file is privileged. Distinguishes variant authorship from canonical structure authorship.  
    Venues: Columbia Journal of Law & the Arts, Harvard JOLT.
    
10. _Institutional Anxiety and the Fear of Multiplicity: Why Museums Still Publish Singular Images_  
    A critical institutional analysis explaining resistance to manifold models: branding, authority, donor expectations, catalog inertia.  
    Venues: Museum & Society, Curator: The Museum Journal.
    

---

**VI. Evaluation, Benchmarking, and ML-Facing Papers (arXiv-native)**

11. _Benchmarking Registration Fidelity in Cultural Heritage Image Manifolds_  
    Defines quantitative benchmarks for alignment quality, spectral consistency, and transformation reversibility. Designed explicitly for reproducibility.  
    Venues: arXiv (cs.CV), CVPR workshops.
    
12. _Learning the Canon: Machine Learning Over Parameterized Art Objects_  
    Shows how ML models trained on canonical manifolds outperform those trained on single images for tasks like damage detection or style analysis. Crucially: ML consumes the manifold, not replaces it.  
    Venues: arXiv (cs.CV, cs.AI).
    

---

**VII. Demonstrator / Case-Study Papers (the wedge)**

13. _A Canonical Digital Edition of a Single Artwork: Methods, Failures, and Limits_  
    A brutally concrete paper: one artwork, N scans, full registration, parameter schema, public viewer. Includes what breaks. This is the paper that forces the field to respond.  
    Venues: DHQ, arXiv (cs.DL).
    
14. _What Changes When the Work Is a Field: Scholarly Use of a Canonical Manifold_  
    Documents how historians, conservators, and critics actually use such an edition differently. Evidence-based, not speculative.  
    Venues: Digital Scholarship in the Humanities.
    

---

**Meta-observation (important):**  
This is not one paper pretending to be many. It is one _ontological shift_ that naturally expresses itself differently depending on audience: theory, infrastructure, conservation, computation, law. That is exactly what “gold mine” ideas look like in academia.

The strategic move is to start with **one backbone paper** (I.1 or VII.13), then let the rest fall out as necessity, not ambition.

I’ll rank them along two axes:

• **Urgency** = how time-sensitive / strategically critical the paper is for staking intellectual territory and shaping how others frame the problem.  
• **Ease** = likelihood of successful completion _now_, with reasonable effort, without needing a large team, grant, or institutional buy-in.

Scores are relative (High / Medium / Low). I’ll also add a short strategic note for each.

---

**Tier 1: Do these first (high leverage)**

**1. From Edition to Manifold: Redefining the Canonical Artwork in Digital Space**  
Urgency: **Very High**  
Ease: **High**  
Why: This is the conceptual keystone. If you don’t write it, someone else eventually will—badly. It requires synthesis, not infrastructure. You can write it alone. This paper gives language that all the others depend on.

**13. A Canonical Digital Edition of a Single Artwork: Methods, Failures, and Limits**  
Urgency: **Very High**  
Ease: **Medium–High**  
Why: This is the “make it real” paper. It prevents dismissal as speculative theory. One artwork, limited scope, honest failure analysis. This anchors the entire galaxy.

---

**Tier 2: Strategic expansion (after the keystone)**

**3. The Canonical Stack: A Systems Architecture for Registered Variant Artworks**  
Urgency: **High**  
Ease: **Medium**  
Why: Once the idea exists, people will ask “how.” If you don’t answer, engineers will reframe it narrowly. You don’t need to build everything—just define the stack and its constraints.

**5. Canonical Does Not Mean Pristine: Encoding Conservation States as First-Class Variants**  
Urgency: **High**  
Ease: **Medium**  
Why: This disarms museum resistance early. It reframes conservation as aligned with your model, not threatened by it. Conceptual plus light technical grounding.

**8. Against the ‘Best Image’: Quantifying Bias in Museum Digitization Pipelines**  
Urgency: **High**  
Ease: **Medium**  
Why: This creates pressure. It turns your idea from “interesting” into “necessary.” Even a modest dataset can produce compelling results.

---

**Tier 3: Credibility builders (field integration)**

**2. Authority Without Fixity: Canonical Status in Parameterized Cultural Objects**  
Urgency: **Medium**  
Ease: **High**  
Why: Important philosophically, but it rides on the success of the foundational paper. Easy to write once the core ontology is established.

**7. Variant-Centric Scholarship: Querying Artworks as Parameter Spaces**  
Urgency: **Medium**  
Ease: **Medium–High**  
Why: This shows scholars _why they should care_. It benefits from a prototype but doesn’t strictly require a polished one.

**14. What Changes When the Work Is a Field: Scholarly Use of a Canonical Manifold**  
Urgency: **Medium**  
Ease: **Low–Medium**  
Why: Powerful, but requires users. This should come later, after others have interacted with the system.

---

**Tier 4: Technical depth (arXiv-native, slower burn)**

**4. Geometry as Ground Truth: Multi-Scan Registration for Cultural Heritage Objects**  
Urgency: **Medium**  
Ease: **Low–Medium**  
Why: Technically serious, publishable, but time-consuming. Not necessary to claim the conceptual territory early.

**11. Benchmarking Registration Fidelity in Cultural Heritage Image Manifolds**  
Urgency: **Low–Medium**  
Ease: **Low**  
Why: Valuable once the field exists. Premature before standards and adoption.

**12. Learning the Canon: Machine Learning Over Parameterized Art Objects**  
Urgency: **Low**  
Ease: **Low**  
Why: This is downstream. It benefits from the existence of canonical manifolds; it does not establish them.

---

**Tier 5: Institutional / legal slow movers**

**9. Who Owns the Canonical Manifold? Copyright, Derivatives, and Parameterized Art**  
Urgency: **Low–Medium**  
Ease: **Medium**  
Why: Important, but institutions won’t act on it until forced. Best written once the model exists in practice.

**10. Institutional Anxiety and the Fear of Multiplicity**  
Urgency: **Low**  
Ease: **High**  
Why: Easy and sharp, but politically sensitive. Better deployed once you already have academic legitimacy.

---

### Condensed Priority Map

**Highest urgency + highest ease (start here):**  
→ Paper 1  
→ Paper 13

**Next wave (define the ecosystem):**  
→ Papers 3, 5, 8

**Then broaden adoption:**  
→ Papers 2, 7

**Finally deepen / specialize:**  
→ Papers 4, 11, 12, 9, 10, 14

If you want, next we can:  
• collapse this into a 2–3 year publication roadmap, or  
• pick _one_ paper and outline it section-by-section down to figures and claims.
