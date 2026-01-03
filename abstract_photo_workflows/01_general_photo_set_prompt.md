If you want an “abusively massive” exploratory pass on an unknown photo corpus with no EXIF, you can still manufacture a huge metadata universe by extracting (1) file/container signals, (2) classical vision features, (3) deep foundation-model embeddings, (4) dense per-pixel semantics, (5) generative-model latents, (6) forensic provenance signals, and (7) dataset-level relational structure. Below is essentially the maximum useful feature surface area I can think of for downstream tasks up to and including training or conditioning image-gen models.

I’m going to assume: you want features you can store per-image (and sometimes per-patch / per-object), searchable at scale, and composable into training sets, filters, clusters, retrieval indices, prompts, and control signals.

A. File- and container-level features (even when “no metadata”)

1. Byte-level / format signatures
    

- MIME/type, magic bytes, codec, container (JPEG/PNG/WebP/HEIC/TIFF), progressive vs baseline JPEG
    
- Dimensions, aspect ratio, bit depth, color type (RGB/RGBA/gray), chroma subsampling (4:4:4, 4:2:0), ICC profile presence
    
- Compression ratio proxy: file_size / (W*H), JPEG quant tables, Huffman tables, PNG filter usage statistics
    
- Thumbnail presence (some formats), XMP remnants, IPTC remnants (often stripped but sometimes partial)
    

2. Integrity / duplication / lineage
    

- Perceptual hashes: pHash/dHash/aHash/wHash (multiple) + multi-resolution hashes
    
- Exact hashes: SHA256, xxhash
    
- Near-duplicate graph: approximate nearest neighbors over hashes + embeddings
    
- Crop/resize lineage detection: match via keypoints (SIFT/ORB) + RANSAC homographies
    

3. Pipeline fingerprints (forensics-lite)
    

- JPEG quantization table clustering (camera/app families)
    
- Recompression count estimation
    
- Resampling detection (periodicity)
    
- Color management anomalies (missing/odd ICC)
    

Use cases: deduping, stratifying by source pipeline, spotting repost chains, training/val leakage control.

B. Global pixel statistics (cheap, surprisingly powerful)  
4) Color / tone / contrast

- RGB/HSV/Lab histograms (coarse + fine), joint histograms (RG, GB)
    
- Mean/var/skew/kurtosis per channel, per colorspace
    
- Dynamic range, clipping rates (percent near 0/255), gamma estimate
    
- White balance estimate, illuminant estimation
    
- Contrast measures (RMS contrast, Michelson on tiles), entropy
    

5. Texture / sharpness / noise
    

- Laplacian variance (sharpness), Tenengrad, edge density
    
- Noise level estimation (per-channel, spatially varying), ISO-like noise signature proxy
    
- Blur type classification (motion vs defocus) via frequency-domain features
    
- JPEG blocking score, ringing score
    

6. Frequency-domain
    

- FFT radial power spectrum, 1/f slope, high-frequency energy ratio
    
- Wavelet energy across scales/orientations
    
- Periodicity detection (moire, screen/print patterns)
    

7. Composition geometry (still global)
    

- Saliency map statistics (center bias, saliency entropy)
    
- Horizon likelihood (dominant line orientation)
    
- Vanishing point estimate, perspective strength
    
- Symmetry scores (vertical/horizontal), rule-of-thirds energy distribution
    

Use cases: quality control, “look” clustering, training curation, aesthetic tagging, preprocessing decisions.

C. Classical CV local features (pre-deep, still useful)  
8) Keypoints and descriptors

- SIFT/ORB/AKAZE keypoints count, descriptor aggregates
    
- Bag-of-visual-words (BoVW) histograms (train vocab on subset)
    
- Geometric consistency features (repeat patterns, architectural cues)
    

9. Contours and shape summaries
    

- Canny edge maps -> edge density, contour length distributions
    
- HOG descriptors (global + tile)
    
- LBP texture histograms (multi-scale)
    
- Gabor filter bank responses
    

Use cases: fast similarity search, structure clustering, robust to some color shifts.

D. Foundation-model embeddings (your main “universal” backbone)  
These are the highest ROI features for “do anything later.”

10. CLIP-family embeddings (image)
    

- Global embedding (ViT-L/14 class)
    
- Multi-crop embeddings (center + corners + random)
    
- Patchwise CLIP embeddings (feature map from intermediate layers)
    
- Text-conditioned similarity against large tag lexicon (open-vocab tagging)
    

11. Self-supervised vision transformers
    

- DINO/DINOv2: global + patch tokens
    
- iBOT/MAE-style embeddings (reconstruction-aware)
    

12. ConvNet embeddings (still good at textures)
    

- EfficientNet/ConvNeXt pooled features
    
- Places365-style scene embeddings (if you want scene taxonomy)
    

13. Multimodal caption embeddings
    

- Generate captions (see below), then embed captions (text embeddings) so you can index by language and do cross-modal retrieval.
    

Use cases: semantic search, clustering by concept, dataset slicing, retrieval augmentation for captioning/prompting, building training sets for specific themes.

E. Dense semantics (objects, masks, parts, relationships)  
This is where “metadata” explodes: you go from 1 vector per image to thousands of structured attributes.

14. Object detection (open-vocab if possible)
    

- Boxes + class labels + confidence
    
- Count features: number of persons, vehicles, animals, etc.
    
- Co-occurrence graphs and spatial stats (object adjacency, relative positions)
    

15. Instance/semantic segmentation
    

- Per-pixel class maps (semantic segmentation)
    
- Instance masks for objects; shape features per mask: area, perimeter, convexity, eccentricity
    

16. “Segment Anything” style masks (class-agnostic)
    

- Many masks per image at multiple scales
    
- For each mask: compute embedding of the crop (CLIP/DINO), color stats, texture stats
    
- This yields an “object-ish database” from unlabeled images
    

17. Keypoints / pose / layout
    

- Human pose keypoints (for non-identifying pose analytics)
    
- Hand keypoints, face landmarks (again, not for identity; for alignment, blur, pose clusters)
    
- Depth estimation (monocular depth map)
    
- Surface normals estimate
    
- Optical flow only if video; for photos you can still estimate motion blur direction.
    

18. Scene graphs (derived)
    

- Build a scene graph: nodes = detected objects/masks, edges = relations (left-of, above, inside, near, overlaps)
    
- Store graph embeddings for retrieval (“images with person near car under tree”)
    

Use cases: compositional queries, training ControlNet-like conditions (seg maps, depth), automatic prompt extraction, object-level dataset balancing.

F. Text in images (huge for “unknown” corpora)  
19) OCR at multiple levels

- Text presence probability
    
- OCR text + bounding boxes + confidence
    
- Script/language detection
    
- Font-ish features (stroke width, typeface class), sign vs document classification
    

20. Document understanding (if many scans)
    

- Layout detection (title/body/table)
    
- Table extraction into structured rows/cols
    
- Form fields detection
    

Use cases: search, redaction, splitting “photo” vs “document,” building paired image-text datasets.

G. Captioning, tags, and “pseudo-labels”  
Even without any ground truth you can synthesize labels.

21. Caption generation
    

- Short caption, long caption, dense caption (multiple regions)
    
- Store: caption text, per-sentence confidence/entropy proxies, and the LM logprob if you can.
    

22. Tag expansion
    

- Take captions -> extract nouns/entities -> canonicalize -> map to taxonomy
    
- Add synonyms/hypernyms via lexical resources (optional)
    

23. Attribute models
    

- Aesthetic attributes: “moody,” “high key,” “film grain,” “bokeh,” “street,” etc. (use a classifier or prompt-based scoring)
    
- Style attributes: “illustration,” “render,” “photo,” “anime,” “diagram,” “scan,” etc.
    
- NSFW filtering (needed for safe pipelines, even if not your focus)
    

Use cases: dataset browsing UX, curating training subsets, prompt mining, weak supervision.

H. Aesthetics and perceptual quality (for selection + training hygiene)  
24) Aesthetic scoring

- NIMA-like aesthetic score
    
- “Interestingness,” memorability (there are models)
    
- Composition scores (rule-of-thirds adherence, subject centeredness)
    

25. Technical quality scoring
    

- Blur score, noise score, exposure score, color cast score
    
- “Is this usable for print?” heuristics
    
- Watermark/logo detection
    

Use cases: filter junk, prioritize high-quality for finetunes, balance “dirty” vs “clean.”

I. Image-forensics / provenance / manipulation cues (useful even if you’ll manipulate later)  
26) Splice / tamper signals

- Error Level Analysis (ELA) (crude but sometimes helpful)
    
- CFA artifact analysis (if raw-like)
    
- Inconsistency maps (noise residual anomalies)
    

27. AI-generated detection signals
    

- Model-based detectors (imperfect; store as a weak signal only)
    
- Frequency artifacts / upscaling signatures
    
- Diffusion “fingerprints” (again: weak, but useful for stratification)
    

Use cases: separating synthetic from camera images, selecting training domain, avoiding contamination.

J. Geo/time inference without metadata (soft, probabilistic)  
This can be very wrong, but even weak signals can help clustering.

28. Geo-style embeddings
    

- Scene/place recognition embeddings (urban vs rural, architecture style, vegetation climate)
    
- Language from signs (OCR) -> country hints
    
- Sun position + shadow orientation -> approximate time-of-day; combined with vegetation maybe season (very approximate)
    

29. Weather/lighting
    

- Cloud cover estimation, haze, rain/snow likelihood
    
- Indoor/outdoor classifier
    
- Night/day/dusk classifier
    

Use cases: browse by “vibe,” semi-automatic grouping, conditioning.

K. Dataset-level relational structure (the “exokiratory” part)  
This is where you turn extracted features into a navigable universe.

30. Multi-index ANN retrieval
    

- Build separate ANN indices: CLIP global, DINO global, FFT spectrum, color hist
    
- Composite retrieval: weighted fusion for search-by-image or “find similar but different”
    

31. Clustering at multiple resolutions
    

- HDBSCAN / k-means / spectral on embeddings
    
- Hierarchical clustering to get coarse->fine “topics”
    
- Cluster summaries via captioning: pick exemplars, caption, auto-name cluster
    

32. Outlier mining
    

- Isolation forest / LOF on embeddings for weird stuff
    
- Rare-object mining from detector counts
    
- Near-duplicate clusters for spam/reposts
    

33. Active “curriculum” views
    

- Sort by quality, by novelty, by uncertainty (caption entropy), by cluster density
    
- Make a sampling policy for labeling or human review
    

L. Generative-model-oriented features (directly useful for image gen workflows)  
If your endgame includes finetuning diffusion/LoRA/control, extract features that become conditioning, filtering, or training metadata.

34. Diffusion VAE latents
    

- Encode each image into the diffusion VAE latent space (4-channel latent)
    
- Store latents (maybe quantized) or store statistics/low-rank projections
    
- Useful for fast experimentation and clustering closer to gen-model geometry
    

35. Diffusion UNet intermediate features (expensive, but maximal)
    

- Pass image through inversion/encoding pipeline; store intermediate activations summaries
    
- Or approximate by encoding then running a few denoise steps with fixed noise schedule to get “trajectory features”
    

36. Inversion artifacts
    

- DDIM inversion latent, reconstruction error
    
- “Promptability score”: how well captions reconstruct via text-to-image similarity
    

37. Control signals
    

- Edge maps (Canny, HED), depth, normals, segmentation maps, pose maps
    
- Store them as training-ready ControlNet targets
    

38. Prompt mining
    

- Caption -> prompt rewrite variants (short, style-focused, object-focused)
    
- Negative prompt suggestions derived from artifacts (blur/noise/watermark)
    

39. Patch libraries
    

- Using SAM masks or sliding windows: build a patch dataset of textures/materials
    
- Tag patches via CLIP and cluster them (“rust,” “stucco,” “foliage,” “neon sign”)
    
- This is gold for style transfer and texture LoRAs.
    

M. “Any tricks” category (things people forget)  
40) Tile-wise everything

- Compute global features per image AND per tile pyramid (e.g., 256px tiles)
    
- Store tile embeddings and tile quality scores
    
- Enables: “find images with this thing somewhere in it”
    

41. Multi-scale pyramids
    

- Process at multiple resolutions: 256, 512, 1024 (or native)
    
- Many artifacts only appear at certain scales (watermarks, texture, faces)
    

42. Ensemble embeddings
    

- Store 3–5 different embedding families; don’t bet on one
    
- Later you can learn a small fusion model for your domain
    

43. Pseudo-chronology / “event” grouping
    

- Cluster by near-duplicates + background similarity to find “bursts” (same event, different angles)
    
- Build sets suitable for multi-view or temporal narratives
    

44. Weak identity-like grouping without biometrics  
    Important: you can group “same person” in a corpus via face embeddings, but that becomes biometric surveillance fast. If you need something adjacent for editorial/creative purposes, prefer:
    

- Clothing color/texture embeddings
    
- Pose + scene context
    
- Near-duplicate series grouping  
    If you do use face features, keep them for local alignment/blur/dedup only, and avoid building any system that identifies people across contexts.
    

45. Storage strategy (otherwise you drown)
    

- Per-image table: ids, paths, file stats, global embeddings (as arrays), quality scores, hashes
    
- Per-object table: image_id, mask_id, bbox/mask RLE, object embedding, object tags
    
- Per-tile table: image_id, tile_id, coords, tile embedding, tile quality
    
- Indices: FAISS/ScaNN per embedding type
    
- Columnar storage: Parquet/Arrow; compress embeddings (float16 / PQ)
    


Think of the workflow as **progressive revelation**, not a single pass. You are moving from “unknown pile of pixels” to a navigable, generative-ready knowledge surface, and you do that in layers that deliberately separate _cheap certainty_ from _expensive meaning_.

I. Ingest and stabilize  
First, you freeze the dataset. Assign immutable IDs, record file paths, hashes, dimensions, formats, and byte-level stats. Do deduplication and near-duplication immediately so you know what you actually have. Nothing intelligent happens yet; this is about preventing entropy later.

II. Cheap global sensing (full corpus)  
Next you run everything that is fast, deterministic, and model-light across **100%** of images: color statistics, sharpness, noise, compression traits, aspect ratios, frequency spectra, simple saliency. This gives you your first maps: quality distributions, obvious junk, modality splits (photos vs scans vs graphics), and early clusters based on “look” rather than meaning. At this stage you already learn how uneven the corpus is.

III. Universal semantic embedding (full corpus)  
Then you run one or two foundation-model image embeddings (CLIP + one self-supervised model) on the full dataset. This is the backbone. From here on, _everything_ can be queried, clustered, sampled, and compared. You build ANN indices and start doing coarse clustering, outlier detection, and similarity search. Still no interpretation—just structure.

IV. Triage and stratification  
Using signals from II and III, you split the corpus into strata: high-quality vs low-quality, photographic vs non-photographic, dense-scene vs sparse, text-heavy vs text-free, human-present vs not. This step is crucial: it prevents you from wasting expensive models on junk and lets you design different exploration paths per stratum.

V. Expensive semantics (selective, stratified)  
Now you deploy the heavy models, but **not everywhere at once**. Object detection, segmentation, OCR, depth, pose, captioning—all run on targeted subsets defined in IV. Outputs are stored structurally: objects, masks, text blocks, scene graphs. This is where “metadata” explodes, but it is controlled and intentional.

VI. Prompted interpretation (measured, versioned)  
Only after structure exists do you introduce prompt templates. Captioning, tagging, aesthetic scoring, style probes, generative prompt mining—each with fixed, versioned prompts. Outputs are treated as weak labels, not truth. You track uncertainty and disagreement. This layer gives you language access to the dataset without collapsing it into prose.

VII. Dataset-level synthesis  
With embeddings + semantics + prompts in place, you zoom out. You analyze cluster themes, rare modes, transitions, co-occurrence graphs, and quality gradients. You name clusters, identify gaps, find overrepresented motifs, and surface strange corners. This is where editorial or research insight actually happens.

VIII. Generative alignment and control extraction  
If generation is an end goal, you now extract gen-ready artifacts: captions rewritten as prompts, negative prompts, segmentation/depth/edge maps, texture patches, diffusion latents. You test inversion and reconstruction fidelity to see what the dataset is good or bad at generating.

IX. Iteration loop  
Crucially, this is not linear. Insights at VIII send you back to V (“we need better masks here”), or to II (“this noise mode matters”), or to VI (“we need a new probe”). Each pass tightens the map. You never rerun everything—only targeted slices.

X. Freeze + publish the map, not just the data  
The final product is not just a dataset; it’s an _explorable system_: indices, tables, prompt registries, cluster summaries, and provenance trails. At that point you can train models, curate subsets, write about it, or hand the whole thing to another agent and know it won’t hallucinate structure that isn’t there.

In short:  
**stabilize → sense → embed → stratify → deepen → interpret → synthesize → generate → loop**.  
Anything that skips steps or mixes them too early usually ends up either expensive and blind, or clever and useless.