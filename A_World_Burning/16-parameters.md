# Parameters

Parameter tuning and observation are where this stops being a one-off experiment and becomes a **controlled scientific instrument**. The trick is to tune **without collapsing into brute-force hyperparameter search**, and to observe **without losing interpretability**. Here's a clean framework you can actually defend in a paper.

---

## 1. First principle: parameters are _axes_, not knobs

You should treat every tunable parameter as representing a **conceptual dimension**, not a convenience variable.

Examples:

- Color temperature → thermal stress
    
- Saturation decay → ecological exhaustion
    
- Background threshold → atmospheric encroachment
    
- Edge preservation weight → species resilience
    
- Segmentation confidence cutoff → semantic fragility
    

Paper language:

> “Parameters are defined to correspond to interpretable environmental or perceptual dimensions, rather than model-internal heuristics.”

This framing matters.

---

## 2. Parameter classes (you should separate these explicitly)

### A. Structural parameters (rarely tuned)

These should be fixed early and almost never changed.

Examples:

- Image resolution
    
- Segmentation model choice
    
- Embedding backbone (e.g. CLIP variant)
    
- Histogram bin counts (if used)
    

Method:

- Choose once
    
- Justify historically or technically
    
- Freeze
    

Observation:

- Stability across runs
    
- No need for sweeps
    

---

### B. Transform parameters (actively tuned)

These are the heart of the work.

Examples:

- Saturation multiplier
    
- Hue drift amplitude
    
- Contrast compression curve
    
- Atmospheric opacity
    
- Noise injection scale
    

How to tune:

- **1D sweeps first**, not grids
    
- Keep all other parameters fixed
    
- Sweep monotonically (e.g. 0.0 → 1.0)
    

What you observe:

- Directionality in embeddings
    
- Onset of semantic instability
    
- Variance across plates
    

Deliverable:

- “Response curves” per parameter
    

---

### C. Safeguard parameters (critical, often overlooked)

These prevent collapse.

Examples:

- Max allowable semantic drift
    
- Min edge preservation score
    
- Protected-region weights
    
- Failure cutoffs
    

Tuning strategy:

- Tune _against failure_, not aesthetics
    
- Find the cliff edge
    
- Step back one notch
    

Paper framing:

> “Safeguard parameters were tuned to maximize degradation while preserving semantic legibility.”

---

## 3. Observation modes (you need more than visuals)

### A. Scalar tracking (your backbone)

For each parameter sweep, track:

- Mean embedding distance
    
- Variance across plates
    
- Affect shift magnitude
    
- Structural preservation score
    

This gives you:

- Curves
    
- Inflection points
    
- Comparability across runs
    

This is what goes in tables.

---

### B. Trajectory plots (extremely important)

Instead of snapshots, you show **motion through embedding space**.

Example:

- x-axis: saturation decay
    
- y-axis: affect distance from baseline
    
- color: semantic stability
    

This answers:

> “Does the system move coherently, or jitter randomly?”

---

### C. Plate-level sensitivity analysis

Some plates will break early. That’s not noise—it’s data.

Observe:

- Which species collapse first
    
- Which compositions resist degradation
    
- Which backgrounds absorb stress
    

This supports claims like:

> “Certain visual ecologies are more resilient.”

---

### D. Failure observation (document this explicitly)

You must show:

- Where failure begins
    
- How it propagates
    
- Which parameters trigger it
    

You are allowed—even encouraged—to include a “failure gallery.”

That’s intellectual honesty.

---

## 4. Parameter interaction (only after 1D sweeps)

You should **not** start with multi-parameter grids.

Correct order:

1. Single-parameter sweeps
    
2. Identify sensitive axes
    
3. Pairwise interactions only where justified
    
4. Never more than 2–3 parameters at once
    

Observation target:

- Nonlinear amplification
    
- Protective interactions
    
- Unexpected stabilization
    

Paper framing:

> “We observe nonlinear interactions between chromatic degradation and semantic boundary preservation.”

---

## 5. Observation cadence (when to look)

A common mistake is over-observing.

Recommended cadence:

- Full scalar logging: every run
    
- Embedding snapshots: every N steps
    
- Visual inspection: only at inflection points
    

This keeps the project sane.

---

## 6. Parameter logging & provenance (this matters)

Every run should log:

- Parameter values
    
- Hardware
    
- Model versions
    
- Seed
    
- Timestamp
    

You already built the run manifests—this is where they shine.

Paper line:

> “All transformations are fully parameterized and reproducible.”

Reviewers love this.

---

## 7. What you do _not_ tune

Explicitly state this:

- You do not tune for beauty
    
- You do not tune for realism
    
- You do not tune for model agreement
    

Instead:

> “Parameters are tuned to maximize controlled deviation along interpretable axes.”

That’s a strong methodological stance.

---

## 8. The meta-observation (this is the real insight)

As you tune and observe, you’ll realize:

- Some parameters behave universally
    
- Others are plate-specific
    
- Some induce smooth transitions
    
- Others cause phase changes
    

This lets you claim:

> “Visual collapse is not uniform; it exhibits threshold behavior dependent on composition and subject.”

That’s publishable insight, not tooling.

---

## If you want next steps

We can:

- Define a **parameter schema** (JSON/YAML) for runs
    
- Design a **minimal sweep plan** (e.g. 12 runs total)
    
- Specify **exact plots** for the paper
    
- Or identify which parameters should become **LoRA training signals**
    

At this point, you’re not tuning models—you’re **mapping a space of historical fragility**.
