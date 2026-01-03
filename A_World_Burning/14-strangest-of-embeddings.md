# Strangest of Embeddings

Yes. There are several **non-obvious / "strange" embedding families** that are unusually well-suited to what you're doing, especially because _The Burning World_ is about **affect, collapse, and atmosphere**, not classification. I'll group these by _what signal they give you_ and _why they're useful_.

---

### 1. Affect / emotion embeddings (but not sentiment)

These are **not “happy / sad” classifiers**; they embed _affective tone_.

What they capture:

- tension vs calm
    
- dread vs openness
    
- agitation, melancholy, eeriness
    
- emotional density rather than polarity
    

How you’d use them:

- Cluster plates by **emotional temperature**
    
- Track how recoloring or degradation _moves_ a plate in affect space
    
- Select images that “feel burned” before they visually look burned
    

Models / approaches:

- CLIP embeddings + emotion-probe heads (linear probes trained on affect datasets)
    
- Multimodal affect models trained on art + emotion tags
    
- Audio–visual affect models repurposed for still images (works surprisingly well)
    

Why this matters:

> You can justify that a plate is “more catastrophic” _before_ it is more damaged.

---

### 2. Arousal–valence–dominance (AVD) embeddings

This is a classic psychology model but rarely used in vision pipelines.

Dimensions:

- **Arousal**: calm ↔ agitated
    
- **Valence**: pleasant ↔ unpleasant
    
- **Dominance**: controlled ↔ overwhelmed
    

Why it’s powerful here:

- “Burning World” lives almost entirely in **low valence + high arousal + low dominance**
    
- You can **numerically show** that the world is losing dominance over itself
    

Use cases:

- Order plates into a psychological arc
    
- Tune transformations until dominance collapses but arousal remains
    
- Compare original Audubon → transformed versions quantitatively
    

This is one of the cleanest bridges between **humanities language and ML metrics**.

---

### 3. Atmosphere / mood embeddings (art-focused)

These are trained on paintings, photographs, and illustrations with labels like:

- ominous
    
- pastoral
    
- desolate
    
- luminous
    
- oppressive
    
- fragile
    

What they’re good at:

- Capturing _ambient feeling_, not objects
    
- Detecting haze, tonal compression, emptiness, imbalance
    

Why this is ideal:  
Audubon plates are already stylized; atmosphere models **don’t fight the illustration**.

Practical uses:

- Measure “atmospheric drift” after each manipulation pass
    
- Select transformations that increase atmosphere without semantic collapse
    
- Train LoRAs to move plates along atmosphere axes instead of color axes
    

---

### 4. Art-historical similarity embeddings (very underrated)

These embed images relative to:

- engraving traditions
    
- lithography
    
- watercolor
    
- 19th-century illustration norms
    

What they give you:

- Distance from “historical plausibility”
    
- A sense of when an image stops being Audubon _and becomes something else_
    

Why this matters:

> Collapse should feel historical, not sci-fi.

You can:

- Keep transformations within a plausible 19th-century visual envelope
    
- Quantify when a plate becomes anachronistic
    

---

### 5. Perceptual stress / instability embeddings (emergent, not labeled)

These are not explicit models but **derived embeddings** built from:

- edge entropy
    
- local contrast variance
    
- boundary uncertainty
    
- figure–ground ambiguity
    
- frequency-domain imbalance
    

You already started this.

What they capture:

- how “tired” an image looks
    
- how unstable its structure is
    
- how close it is to perceptual failure
    

Why they’re special:  
They are **model-agnostic**, explainable, and defensible.

They let you say:

> “This plate is structurally exhausted.”

---

### 6. Narrative tension embeddings (via VLMs)

This sounds odd, but it works.

Method:

- Feed images to a vision-language model
    
- Ask neutral prompts like:
    
    - “Describe the scene in one sentence.”
        
    - “What is about to happen?”
        
- Embed the responses
    

What emerges:

- Latent narrative expectation
    
- Sense of threat, stasis, or aftermath
    

Why useful:  
You’re not asking for _truth_, you’re sampling **cultural narrative priors**.

This tells you:

- Which images imply catastrophe
    
- Which imply endurance
    
- Which feel already post-event
    

---

### 7. Embeddings of _absence_ (negative space sensitivity)

Some models are particularly sensitive to:

- empty sky
    
- blank ground
    
- unused space
    
- imbalance
    

This is gold for _The Burning World_.

You can:

- Quantify emptiness
    
- Drive transformations that increase absence rather than damage
    
- Separate “ruin” from “desertion”
    

---

## How this all fits together

You’re not choosing **one** strange embedding.

You’re building a **stack**:

- Structural / pixel metrics → _what is breaking_
    
- Affect embeddings → _how it feels_
    
- Atmosphere embeddings → _what kind of world it is_
    
- Art-historical distance → _how plausible it remains_
    
- Narrative embeddings → _what it implies_
    

That stack gives you:

- selection
    
- ordering
    
- justification
    
- training signals for LoRAs
    
- and eventually, curatorial control
    

---

## The key insight

You are not trying to extract _meaning_.

You are extracting **pressure, mood, fragility, and expectancy**.

That is exactly where these “strange” embeddings shine.

If you want, next we can:

- pick **3 embeddings to start with**
    
- define **exact prompts or probes**
    
- or design a **composite “Burn Index”** that combines them into one scalar per plate

---

## Operational addendum (so this doesn’t stay abstract)

For the fully documented “instrument catalog” (candidate models + run/ledger discipline), see:

- `A_World_Burning/27-strange-models-compendium.md`

Concrete candidate instruments mentioned there include (examples):

- Aesthetic predictors (CLIP-based): `shunk031/aesthetics-predictor-v1-vit-large-patch14`
- Memorability probe: `PerceptCLIP/PerceptCLIP_Memorability`
- Art-historical (WikiArt) classifiers: `davanstrien/convnext-tiny-224-wikiart`

All of these must be treated as **weak axes**, never as authority.
