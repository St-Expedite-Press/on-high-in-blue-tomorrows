# A Shape Dimly Glowing

Good-this is exactly the right moment to ask this, because **what you ask the vision models determines whether this becomes analysis or just ornament**.

I’ll answer in three layers:

1. **What kinds of semantic data are actually extractable**
    
2. **What questions you can legitimately ask vision models**
    
3. **How those questions map to _The Burning World_** (i.e., why you’d bother)
    

---

## 1. What “semantic data” means _in this project_

You already have:

- structural data (pixels, histograms, edges)
    
- bibliographic data (plate number, species name)
    
- physical metadata (size, orientation, entropy)
    

Semantic data sits _between_ pixels and meaning.

It answers questions like:

- _What parts of this image matter most?_
    
- _What does the image seem to be “about” visually?_
    
- _Where is attention concentrated?_
    
- _How similar is this plate to others in a non-obvious way?_
    

Crucially:  
**semantic ≠ textual truth**  
Semantic here means _perceptual meaning_, not taxonomy correctness.

---

## 2. Categories of questions you can ask vision models

Think in terms of **query families**, not models.

---

### A. Salience & attention

_(What draws the eye? What “counts” visually?)_

Questions:

- Which regions dominate visual attention?
    
- Is attention centralized or dispersed?
    
- Does the bird overpower the background, or dissolve into it?
    
- Where would a non-human observer “look first”?
    

Data you get:

- saliency heatmaps
    
- ranked regions by importance
    
- attention centroids
    
- foreground dominance scores
    

Why this matters:

- Climate catastrophe often reads as **loss of focal clarity**
    
- You can later degrade, distort, or exaggerate _only_ salient zones
    

---

### B. Figure–ground semantics

_(What is subject vs environment?)_

Questions:

- What is confidently “organism” vs “world”?
    
- How clean is the separation?
    
- Where does the plate already blur figure and ground?
    

Data you get:

- segmentation masks
    
- confidence gradients at boundaries
    
- ambiguous zones (neither clearly bird nor background)
    

Why this matters:

- “Burning World” is fundamentally about **environment overwhelming subject**
    
- Ambiguous zones are where narrative pressure lives
    

---

### C. Visual similarity & clustering

_(Which plates belong together perceptually?)_

Questions:

- Which plates look similar despite different species?
    
- Are there latent visual families (dark plates, open skies, dense foliage)?
    
- Which plates are outliers?
    

Data you get:

- embeddings
    
- clusters
    
- distance matrices
    
- nearest-neighbor graphs
    

Why this matters:

- Lets you apply **systemic transformations** without repetition
    
- You can say: _this catastrophe expresses differently across visual regimes_
    

---

### D. Semantic stability & fragility

_(What survives distortion? What breaks quickly?)_

Questions:

- How much alteration before a plate stops “reading” as itself?
    
- Which regions tolerate chromatic stress?
    
- Which plates collapse semantically under noise, blur, or tint?
    

Data you get:

- similarity drop-off curves
    
- robustness scores
    
- per-region sensitivity
    

Why this matters:

- Catastrophe is not uniform
    
- Some species/worlds endure; others fail immediately
    

---

### E. Latent concepts (used carefully)

_(What ideas does the model associate with the image?)_

Questions (carefully framed):

- Does the image evoke “bird”, “animal”, “landscape”, “sky”?
    
- Does it drift toward “texture”, “pattern”, “abstraction” under stress?
    
- Does semantic drift accelerate after certain transformations?
    

Data you get:

- concept similarity scores
    
- semantic drift trajectories
    
- confidence decay
    

Why this matters:

- You can track **semantic extinction**
    
- The plate stops being “about” a bird before it stops depicting one
    

---

## 3. What you should **not** ask vision models

This is just as important.

Do **not** ask:

- “What species is this?” (you already know; model errors add nothing)
    
- “Is this realistic?” (aesthetic normativity)
    
- “Generate a burning version” (authorial abdication)
    
- “Describe this image” (language noise)
    

Those turn the model into a narrator or illustrator.

You want it as an _instrument_, not a voice.

---

## 4. How this feeds _The Burning World_

Here’s the key conceptual move:

> You are not showing climate change.  
> You are showing **semantic failure under environmental stress**.

Vision models let you:

- quantify _when_ meaning breaks
    
- localize _where_ it breaks
    
- vary _how_ it breaks across plates
    

Later, when you alter coloration, atmosphere, or materiality:

- you won’t be guessing
    
- you’ll be operating along fault lines the system already revealed
    

That gives the series internal coherence without uniformity.

---

## 5. A clean mental model to keep you honest

When asking a vision model anything, you should be able to say:

> “If I removed the final images, this data would still be meaningful.”

If the answer is no, you’re drifting toward gimmick.

---

## Where this leaves you next

From here, the logical next steps are:

- define **3–5 semantic questions you care about**
    
- decide which are _measurement_ vs _guidance_
    
- only then pick specific models (CLIP, DINO, SAM, etc.)
    

If you want, next we can:

- design a **semantic question schema** (so every run asks the same things), or
    
- map **which questions justify ML and which don’t**, or
    
- sketch how semantic data becomes _constraints_ for color and atmosphere.
    

You’re doing this exactly in the right order.
