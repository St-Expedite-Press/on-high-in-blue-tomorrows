## PASS 0 — Fix the ground (one time only)

**Goal:** Make the dataset restart-proof.

- Mount Drive
    
- Build immutable image manifest (`image_id`, path, hash, size)
    
- Deduplicate exact + near duplicates
    
- Freeze IDs forever
    

Nothing else happens until this exists.

---

## PASS 1 — Brutal global sensing (100% coverage)

**Goal:** Extract cheap, orthogonal signals that every later decision rests on.

Run on **every image**, no exceptions.

Outputs (per image):

- File stats, hashes
    
- Color histograms (RGB + Lab)
    
- Sharpness / blur / noise
    
- FFT / frequency energy
    
- Aspect ratio, resolution
    
- CLIP ViT-L global embedding
    
- DINOv2 global embedding
    

Write immediately to Parquet.

**You do not look at images yet.**

This pass gives you:

- First cluster map
    
- Junk detection
    
- Modal splits (photos vs scans vs graphics)
    
- A semantic + structural backbone
    

---

## PASS 2 — Stratification + kill cuts

**Goal:** Decide where _not_ to spend GPU.

Using PASS 1 outputs:

- Flag:
    
    - Low-quality junk
        
    - Text-heavy scans
        
    - Near-duplicates
        
    - Extreme outliers
        
- Create boolean columns in manifest
    

You do not delete anything, but you now have **routing flags**.

This pass saves you hours later.

---

## PASS 3 — Mask explosion (segmentation as force multiplier)

**Goal:** Turn each image into dozens/hundreds of analyzable units.

Run **SAM only**, no labels.

For each image:

- Generate masks at multiple scales
    
- Filter trivial masks (too small, too thin)
    
- For each mask:
    
    - Crop region
        
    - Record mask geometry (area %, solidity)
        
    - Save mask ID linked to image ID
        

You now have a **segment manifest**.

This is the point where the dataset size explodes.

---

## PASS 4 — Segment embedding (this is where meaning appears)

**Goal:** Discover motifs without naming them.

For each segment:

- CLIP embedding
    
- DINO embedding
    
- Color / texture stats
    

Do not caption yet.

Now you can:

- Cluster segments
    
- Find recurring background elements
    
- Detect rare motifs
    
- Separate “foreground” from “infrastructure” statistically
    

This is the most important pass after PASS 1.

---

## PASS 5 — Captioning and language projection (selective)

**Goal:** Add language _after_ structure exists.

Run captioning **only on**:

- Cluster exemplars
    
- High-entropy segments
    
- Outlier segments
    
- Representative full images per cluster
    

Use:

- BLIP-2 for factual
    
- LLaVA for dense / reasoning
    

Store:

- Caption text
    
- Model
    
- Prompt version
    

Now language is mapping structure, not inventing it.

---

## PASS 6 — Secondary semantics (optional but brutal)

**Goal:** Add orthogonal axes where they help.

Run selectively:

- OCR (on text-heavy flags)
    
- Depth estimation (on photographic flags)
    
- Object detection (only if counting matters)
    

Do **not** rerun on everything.

---

## PASS 7 — Re-aggregation and synthesis

**Goal:** Collapse upward without lying.

Aggregate:

- Segment clusters → image-level features
    
- Frequency of motifs per image
    
- Co-occurrence graphs
    

Re-embed captions.  
Compare:

- Image vs segment semantics
    
- Language vs structure
    

This is where interpretation begins—but statistically.

---

## PASS 8 — Generative probing (optional, late)

**Goal:** Test what the dataset _affords_.

- Img2img on cluster exemplars
    
- ControlNet with depth/edges
    
- Re-embed generated outputs
    

Look for:

- Stable styles
    
- Fragile motifs
    
- Holes in the manifold
    

---

## STOP CONDITION (non-negotiable)

You stop extracting when:

- New passes stop changing cluster topology
    
- Segment clusters stabilize across CLIP and DINO
    
- Captions stop introducing new axes
    
- Outliers remain outliers no matter what you throw at them
    

Anything beyond that is indulgence.

---

## The governing principle

Early: **maximize ignorance resolution**  
Middle: **force structure without naming**  
Late: **let language touch only what survived pressure**

Segmentation earns its place here because it **increases the surface area on which pressure can act**. Without it, too much stays smeared inside global embeddings.

If you want next, I can:

- Turn this into a **single master checklist**
    
- Write **pseudo-code notebooks** for each pass
    
- Define **exact Parquet schemas** so this doesn’t sprawl
    
- Or design **visual diagnostics** that tell you when to move to the next pass