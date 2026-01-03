# Yea, We Need Vectors Too

Vectorization is not a side quest here; it's a **second representation regime**. If raster work is about _degradation, atmosphere, and stress_, vectorization is about **structure, survivability, and what refuses to burn**. Used correctly, it gives you leverage that raster-only pipelines never will.

I’ll break this into **why**, **what kinds**, **how to benchmark**, and **how it fits the paper**.

---

## 1. Why vectorize at all?

Vectorization answers a different question than ML or embeddings:

> _What structural information persists when material detail is stripped away?_

For Audubon plates, this is extremely meaningful because:

- They are already illustrations (not photographs)
    
- They have line discipline, contour logic, and compositional intent
    
- Many were engraved → inherently vector-adjacent
    

Vectorization lets you:

- Separate **form from pigment**
    
- Test which parts of the image are structurally essential
    
- Build a “skeleton” that can survive catastrophic recoloring
    

Conceptually:

> Raster = climate, atmosphere, decay  
> Vector = anatomy, persistence, resistance

---

## 2. Types of vectorization (not all are equal)

### A. Edge-based vectorization (most defensible)

Examples:

- Canny → Potrace-style tracing
    
- Sobel/Laplacian → threshold → path extraction
    

What it captures:

- Contours
    
- Anatomical boundaries
    
- Compositional scaffolding
    

Why it’s good:

- Interpretable
    
- Historically aligned (engraving logic)
    
- Easy to benchmark
    

Use cases:

- Measure edge loss under degradation
    
- Preserve linework while burning color
    
- Generate “burned but intact” variants
    

---

### B. Region / shape vectorization (very powerful)

Examples:

- Segmentation masks → polygonization
    
- Superpixel regions → vector regions
    

What it captures:

- Figure/ground separation
    
- Mass and balance
    
- Ecological zones (sky, foliage, body)
    

This is ideal for:

- Selective recoloring
    
- Differential degradation
    
- Semantic protection LoRAs
    

---

### C. Skeletonization / medial axis (experimental, fascinating)

This reduces shapes to:

- spines
    
- joints
    
- primary axes
    

What it gives you:

- A literal “bone structure” of the plate
    
- A way to say: _this still lives_
    

This is conceptually rich but fragile—use sparingly.

---

### D. Learned vectorization (least defensible here)

Neural SVG extraction models exist, but:

- They hallucinate
    
- They impose modern priors
    
- They’re hard to justify historically
    

I would only use these as **comparative baselines**, not production.

---

## 3. What you can do once you have vectors

This is where things open up.

### A. Structural invariance benchmarks

You can now measure:

- % of vector paths preserved
    
- Path length change
    
- Topology change (splits, merges)
    

Paper-friendly claim:

> “Despite severe chromatic collapse, vector structure remains X% intact.”

---

### B. Vector-guided raster manipulation

Vectors can act as:

- masks
    
- protection zones
    
- anchors
    

Example:

- Burn everything _except_ vector cores
    
- Let background dissolve while skeleton persists
    

This is visually powerful and conceptually clean.

---

### C. Hybrid renderings (very on-theme)

You can produce:

- Raster burned plates over vector ghosts
    
- Vector-only plates with scorched fills
    
- Alternating raster/vector editions
    

This reinforces:

> “What survives is structure, not surface.”

---

### D. Vector embeddings (rare but possible)

You can embed:

- Path statistics
    
- Shape complexity
    
- Curvature distributions
    

This lets you:

- Cluster plates by structural complexity
    
- Identify which species/forms are more resilient
    

---

## 4. Vectorization as a benchmark axis

This is important for the paper.

You can benchmark:

- Raster degradation vs vector stability
    
- Edge entropy vs vector collapse
    
- Semantic drift vs vector preservation
    

This supports a strong claim:

> “Structural representation degrades more slowly than perceptual appearance.”

That’s a real insight about images and history.

---

## 5. How to parameterize vectorization (important)

Vectorization parameters are _not aesthetic knobs_.

They represent:

- Sensitivity to detail
    
- Tolerance for loss
    
- Thresholds of recognition
    

Examples:

- Edge threshold → perceptual tolerance
    
- Path simplification → abstraction pressure
    
- Region merge distance → ecological collapse
    

These can be swept and observed like any other parameter.

---

## 6. Where vectorization fits in your pipeline

Clean placement:

1. **Original raster**
    
2. Lightweight scalar metadata (done)
    
3. Segmentation / structure extraction
    
4. Vectorization (edge + region)
    
5. Raster transformations (burning, color)
    
6. Vector-guided constraints
    
7. Embedding + benchmarking
    

Importantly:

- Vectorization happens **before** aggressive degradation
    
- It becomes a _reference_, not an output artifact only
    

---

## 7. How this reads in a paper

Vectorization gives you language like:

- “Structural persistence”
    
- “Formal resilience”
    
- “Anatomical survivability”
    
- “Skeletonized representations”
    

It lets you say:

> “We distinguish between the degradation of surface appearance and the persistence of formal structure.”

That sentence alone is worth including vectorization.

---

## 8. What not to do

Don’t:

- Replace raster with vector
    
- Aim for perfect SVGs
    
- Overfit vector aesthetics
    

Vectors are **measuring instruments**, not the art itself.

---

## Bottom line

Vectorization gives you:

- A second, orthogonal data modality
    
- Strong benchmarks
    
- Historical alignment
    
- Conceptual depth
    
- Hybrid visual strategies
    

For _The Burning World_, it’s not optional—it’s the **counterpoint to decay**.

If you want, next we can:

- pick **exact vectorization methods**
    
- design **vector benchmarks**
    
- or define **how vectors feed LoRA training or constraints**
