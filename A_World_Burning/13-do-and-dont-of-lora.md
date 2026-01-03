# Do and Don't of LoRA

If you train a **LoRA** here, the key is to remember what LoRA is good at:  
**small, targeted behavioral shifts on top of a strong pretrained model**, not learning the world from scratch.

So the question isn’t _“what can I train?”_ but _“what bias, sensitivity, or failure mode do I want to imprint?”_

Below are **LoRA ideas that actually make sense for _The Burning World_**—ordered from **most defensible** to **most speculative**.

---

## 1. Style–preserving color-climate LoRA (highest value)

### What it learns

Not “Audubon style” (already baked in), but **how color shifts behave under stress while preserving illustration structure**.

You train on:

- Original plates
    
- Your controlled recolorings (smoke, heat, ash, drought palettes)
    
- Paired or ranked: _acceptable_ vs _collapsed_
    

### What the LoRA encodes

- How saturation decays without flattening linework
    
- How highlights yellow or scorch
    
- How skies and foliage destabilize differently
    

### What you get

A model that:

- “burns” images _in-character_
    
- Respects engraving logic
    
- Doesn’t hallucinate anatomy
    

This is the **cleanest, most defensible LoRA** for the project.

---

## 2. Semantic-fragility LoRA (very strong conceptually)

### What it learns

**Where not to touch.**

You train using:

- Attention maps
    
- Segmentation confidence
    
- Semantic-collapse metrics from embeddings
    

You label:

- “Protected zones”
    
- “Sacrificial zones”
    
- “Already unstable zones”
    

### What the LoRA encodes

- A bias against altering semantically critical regions
    
- A tendency to push damage into background, sky, peripheral foliage
    

### Why this is powerful

It makes the model behave like:

> “I know what matters, and I will let the rest burn.”

This turns _analysis into behavior_.

---

## 3. Figure–ground instability LoRA

### What it learns

The **threshold at which birds dissolve into environment**.

Training signal:

- Segmentation masks
    
- Edge confidence
    
- Boundary ambiguity
    

You bias the model to:

- Soften boundaries under stress
    
- Let background encroach
    
- Preserve silhouette longer than interior detail
    

### Result

Images that feel:

- environmentally overwhelmed
    
- ontologically unstable
    
- historically exhausted
    

This is very on-theme.

---

## 4. Atmospheric degradation LoRA (controlled decay)

### What it learns

How _air itself_ changes.

Training data includes:

- Fogging
    
- Smoke veils
    
- Heat shimmer artifacts
    
- Contrast collapse patterns
    

You are **not** teaching weather—you’re teaching **visibility failure**.

### Output behavior

- Distance collapses
    
- Midtones muddy
    
- High-frequency detail decays first
    

Subtle, powerful, dangerous if overused.

---

## 5. Negative-space amplification LoRA (interesting, niche)

### What it learns

To exaggerate:

- emptiness
    
- sky dominance
    
- isolation
    

This LoRA nudges the model to:

- push subjects toward edges
    
- expand unoccupied regions
    
- reduce compositional balance
    

Useful for late-stage plates.

---

## 6. Failure-mode LoRA (experimental, risky, fascinating)

### What it learns

**How Audubon breaks.**

You intentionally train on:

- Near-failure outputs
    
- Overburned images
    
- Semantic collapse cases
    

Goal:

- Encode _how collapse looks_, not how to avoid it
    

This is dangerous but conceptually rich.  
You’d only use it sparingly.

---

# What you should NOT train as LoRAs

These are tempting but wrong for this project:

❌ Species recognition  
❌ Text captioning  
❌ Narrative explanation  
❌ “Make it climate apocalypse” prompt following  
❌ General “Audubon style” (already learned)

---

# The right mental model

Each LoRA should answer **one sentence**:

- _“This is how color burns without destroying form.”_
    
- _“This is what not to touch.”_
    
- _“This is how boundaries fail.”_
    

If you can’t describe the LoRA in one sentence, it’s too big.

---

# How many LoRAs is sane?

**3–5 total**, not more:

1. Color/heat behavior
    
2. Semantic protection
    
3. Boundary instability
    
4. (Optional) Atmosphere
    
5. (Optional) Failure mode
    

They can be **stacked or weighted**, which gives you enormous control.

---

## The big payoff

With these LoRAs, you’re no longer “prompting images.”

You’re doing **parameterized ecological collapse**.

And crucially:

- your preprocessing work _directly feeds training_
    
- your metrics justify your aesthetics
    
- the project becomes legible as a system, not a vibe
    

If you want, next we can:

- choose **one base model** (SDXL, SD1.5, etc.)
    
- design **exact training sets** from your plates
    
- or define **when to switch from analysis → training** so you don’t jump early
