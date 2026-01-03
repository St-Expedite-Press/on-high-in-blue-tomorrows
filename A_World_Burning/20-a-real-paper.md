# Audubon Plates Dataset Enhancement: Overview and Plan

[[A_World_Burning/README]] | [[A_World_Burning/30-whitepaper-toc]] | [[A_World_Burning/26-whitepaper-skeleton]]

The dataset consists of **435 high-resolution bird illustrations** from John James Audubon’s _Birds of America_, compiled by Nathan Buchar[github.com](https://github.com/nathanbuchar/audubon-bird-plates#:~:text=Audubon%20Bird%20Plates). These plates (≈2.9 GB total) were released for education and research, with credit to the Audubon Center at Mill Grove (Mill Grove, PA) and Zebra Publishing[github.com](https://github.com/nathanbuchar/audubon-bird-plates#:~:text=A%20collection%20of%20all%20435,9GB). For example, Plate 420 (_Prairie Starling_) shows two vividly colored starlings against a natural background[github.com](https://github.com/nathanbuchar/audubon-bird-plates#:~:text=A%20collection%20of%20all%20435,9GB) (illustrated below) – a typical scene illustrating birds, flora, sky, and printed text. Each plate is accompanied by metadata (plate number, title, slug, source URL) as per the Buchar collection manifest. The goal is to enrich this core collection into a _feature-rich, provenance-aware dataset_ for publication and reuse.

 

> [!note] Original image embed placeholder (kept for provenance; does not render in Obsidian)
> `![https://github.com/nathanbuchar/audubon-bird-plates](blob:https://chatgpt.com/d8e16967-84dd-4a01-b48b-fd9ac4b32167)`

![Plate 420 – Prairie Starling (audubon.org)](https://www.audubon.org/sites/default/files/boa_plates/plate-420-prairie-starling.jpg)

_Figure: Example Audubon plate (Plate 420, “Prairie Starling”). These hand-colored engravings typically show one or more bird species in naturalistic poses. (Image courtesy Nathan Buchar, 2022[github.com](https://github.com/nathanbuchar/audubon-bird-plates#:~:text=A%20collection%20of%20all%20435,9GB).)_

## Data Ingestion and Preprocessing

1. **Image Acquisition & Verification:** Download all 435 source images (JPEG/TIFF at full resolution) from the Buchar repository or Audubon servers. For reproducibility, store a manifest JSON (validated by schema) listing each plate’s ID, source URL, download timestamp, and SHA-256 checksum. Use scripts (in Python/PIL or OpenCV) to verify each file’s integrity and shape; record any corrupt/missing plates. Maintain a Git-tracked directory or cloud bucket with raw images, protected by hash checks.
    
2. **Normalization & Resampling:** Optionally, produce a standardized downsampled version (e.g. max dimension 2048 px) for faster processing, while retaining full-res originals for archival. Record both resolutions in metadata. Normalize image orientation/color spaces (e.g. ensure all RGB) and strip extraneous EXIF/IPTC (none expected from scans). If plates have varying DPI, log their physical dimensions. Use Python imaging libraries to extract basic header info (format, dimensions, mode) and embed into a Parquet or CSV table of scalars.
    
3. **Color & Pixel Statistics:** Compute per-image _pixel-level statistics_: channel means, standard deviations, histograms (e.g. 32-bin per channel), dominant palette (e.g. k-means clusters), and metadata such as histogram of gradients if needed. These scalars provide quick summaries of color composition and contrast. They can be stored in a tabular format (Parquet) alongside plate metadata. Visualizing global color distribution (e.g. 2D hist or HSV scatter) is encouraged for EDA.
    
4. **Checksum Tracking:** For provenance, compute and store cryptographic hashes (SHA-256) of each raw image and of any intermediate files (e.g. masks, embeddings). Reference these in a **run manifest** for each processing step. This ensures any derived artifact can be traced back to the exact source image. All code (e.g. Colab notebooks) should log library versions and be tagged by a unique run ID.
    

## Feature Extraction – Embeddings and Vectors

1. **Global Image Embeddings:** Use OpenAI’s CLIP or similar models to embed each plate image into a high-dimensional feature space[arxiv.org](https://arxiv.org/abs/2103.00020#:~:text=supervision,often%20competitive%20with%20a%20fully). For example, CLIP (Vision Transformer backbone) yields 512-dimensional image vectors that capture semantic content in a multimodal space[arxiv.org](https://arxiv.org/abs/2103.00020#:~:text=supervision,often%20competitive%20with%20a%20fully). These can be stored (with plate IDs) in a Parquet or HDF5 table for fast retrieval. Document which model/checkpoint and preprocessing (size, normalization) are used. Optionally extract embeddings from multiple CLIP variants (ViT-B/32, ViT-L/14, etc.) or other vision-language models (e.g. OpenAI’s RN50, RN101, or models from Hugging Face) to allow comparisons.
    
2. **Region/Segmentation-Aware Embeddings:** To capture fine-grained content, apply segmentation (see below) and then extract embeddings for each semantic region. For instance, run CLIP on the bird region crop, on flora region crop, etc. This yields _part-level_ descriptors (e.g. bird vs sky vs text) and supports tasks like retrieval (“find all plates with flamingo”). Some recent works incorporate segmentation into feature learning (e.g., [SAM][5]). Although we do not retrain CLIP, we can simulate segmentation-aware embeddings by masking out parts and re-embedding. Store region masks and labels (e.g. “bird_1”, “sky”) and their centroids.
    
3. **Multimodal Text Embeddings:** Use a text encoder (the CLIP text model) to embed plate captions or scientific names. For example, encode the species name (“Icterus gubernator”) or descriptive prompts. These text vectors can be aligned with image embeddings for retrieval. Additionally, consider any available textual descriptions (from Audubon’s engravings) or contemporary iNaturalist observations matched to each bird (as in [2][github.com](https://github.com/upenndigitalscholarship/audubon-birds-of-penn#:~:text=Plate%20images%20from%20Audubon%27s%20Birds,observations%20posted%20with%20a%20license)) to create paired image–text data.
    
4. **Style & Aesthetic Features:** Extract “style” features using models trained on art (e.g. a CNN fine-tuned on WikiArt styles[huggingface.co](https://huggingface.co/datasets/huggan/wikiart#:~:text=Dataset%20containing%2081%2C444%20pieces%20of,labels%20for%20each%20image)). Although Audubon’s illustrations are nature art (more realistic), style embeddings (painting style, brush stroke, color usage) may still be informative. Alternatively, use Gram matrix features or pretrained stylization networks. For emotional tone, one could apply an emotion-recognition model (e.g. “FindingEmo” [48]) on the whole scene, though this is speculative. Tagging images with style or mood attributes (e.g. “pastoral”, “dramatic lighting”) could support digital humanities analysis.
    
5. **Other Semantic Features:** Consider external annotations or computed attributes: e.g., use an object detector (like Detectron2) to check for presence of humans/colonial figures (some plates include people), or to count bird individuals. For _climate degradation_, one could flag if vegetation looks wilted or background shows storm clouds – perhaps train a small CNN on synthetic “drought vs lush” examples to assign a score. For _anatomical stress_, if birds are depicted in distress (injured, entangled), note this manually or via action recognition classifiers. These specialized features would require manual or custom modeling, but could yield novel “scholarly” tags.
    

## Semantic Segmentation

1. **General Segmentation (SAM):** Use Meta’s **Segment Anything Model (SAM)** for zero-shot image segmentation[arxiv.org](https://arxiv.org/abs/2304.02643#:~:text=,URL%20to%20foster%20research%20into). SAM can generate pixel masks for _any_ region given a prompt. We can run SAM in automatic mode (no prompt) to produce a set of region proposals (1B masks were generated in their dataset[arxiv.org](https://arxiv.org/abs/2304.02643#:~:text=,URL%20to%20foster%20research%20into)). For each plate, collect masks corresponding to distinct objects. (In practice, either use the SAM Python interface or through their Google Colab + GPU.)
    
2. **Semantic Labeling of Masks:** Since SAM is class-agnostic, we must label each mask (bird, plant, sky, text, background, etc.). For each mask, compute a CLIP image embedding and score it against text prompts (“bird”, “tree”, “sky”, “water”, “inscription”, etc.). Assign the label with highest similarity. For example, a mask whose CLIP embedding strongly matches “bird” likely corresponds to the illustrated bird. This approach (mask + CLIP) is akin to OVSeg [openreview.net](https://openreview.net/forum?id=6Gzkhoc6YS#:~:text=Personalize%20Segment%20Anything%20Model%20with,shot%20classification) or other works on segment classification. Alternatively, train a small classifier on a few manually labeled masks (transfer learning) to distinguish common categories.
    
3. **OCR for Inscription:** Many Audubon plates have Latin and common names printed. Use a text detection/recognition model to segment and read these regions. For instance, Tesseract OCR[modal.com](https://modal.com/blog/8-top-open-source-ocr-models-compared#:~:text=Tesseract%20is%20the%20most%20established,ready) (modern LSTM engine) can extract text from the printed labels. More advanced models (TrOCR, VisionLLMs) could be tried, but plate text is clear typography. Store the transcribed inscription (Latin binomial, common name, plate number) as metadata. Also mark the text region’s mask so that analyses know these pixels are non-natural content.
    
4. **Refinement:** Check the segmentation quality. For birds and flora, masks should ideally cover the exact pixels of those objects. Manually review a sample; if needed, refine using a U-Net (fine-tuned on a small manually annotated set) or use GrabCut on SAM’s mask. Note: Audubon plates often have complex interlocking poses; some fine detail (wing edges, branch outline) may be missed by a single pass. It may help to treat each color segment (e.g. birds and background) separately.
    
5. **Derived Masks (e.g. sky, water):** If SAM fails to detect background elements like sky, one can derive them heuristically (e.g. all pixels not covered by bird/plant masks in a natural scene may be sky/water). In painting-style plates, backgrounds may be sparse. Optionally use an external scene segmentation model (ADE20K classes) to find “sky” or “water” regions, then cross-check with SAM.
    

Store all masks in e.g. PNG or compressed NPY format, keyed by plate and mask ID. Include the semantic label and mask area. These enable pixel-level analyses (e.g. count bird pixels per plate, measure color distribution on birds vs sky).

## Data Organization & Storage

1. **Schema & Manifests:** Adopt a formal schema for each plate’s metadata and each processing _run_ (as given in the provided JSON schemas). Store plate-level metadata (ID, title, source, license) in a Parquet table or JSON lines. Store run manifests (with run_id, models used, output artifact paths) to track how each feature was generated. This enforces provenance and enables auditability.
    
2. **Tabular Storage (Parquet):** Use Parquet files to store tabular data and small binary arrays. As the HuggingFace Datasets guide notes, Parquet allows embedding images and metadata columns together[huggingface.co](https://huggingface.co/docs/hub/en/datasets-image#:~:text=Parquet%20format). For example, one Parquet file could contain columns: `image_id`, `image_path`, `width`, `height`, `mean_rgb`, `histogram`, `CLIP_embedding` (a fixed-length binary blob or array), etc. Parquet’s compression and columnar layout make queries efficient[discuss.huggingface.co](https://discuss.huggingface.co/t/image-dataset-best-practices/13974#:~:text=2,It%E2%80%99s%20nice%20on%20several%20aspects). Parquet is also easily versioned and has built-in schema.
    
3. **Large File Handling (WebDataset):** The raw images are large (each high-res plate could be many MB). For distributing or training, consider the WebDataset format: tarball shards of image+JSON pairs[huggingface.co](https://huggingface.co/docs/hub/en/datasets-image#:~:text=WebDataset%20format). Each tar (e.g. ~1 GB) contains a batch of plate images and their metadata, which supports streaming training and reduces many small-file overhead. HuggingFace suggests WebDataset for large image collections[huggingface.co](https://huggingface.co/docs/hub/en/datasets-image#:~:text=WebDataset%20format). For smaller scales or final release, one could instead include images in Parquet (with `image` columns) if each is <1 MB[huggingface.co](https://huggingface.co/docs/hub/en/datasets-image#:~:text=Parquet%20format); however, Audubon plates are likely larger, so WebDataset or git-lfs is more practical.
    
4. **Compression:** Store raw images in a lossless format (PNG or original TIFF if available) for archival. For intermediate storage (analysis), JPEG with high quality is fine. Parquet will compress numeric data and embedded images using Snappy or ZSTD. Also compress any artifact archives (zip/tar). Maintain a copy of the final dataset in a public repository or data archive, possibly using cloud storage (e.g. AWS S3, Zenodo) with dataset DOI.
    
5. **Reproducibility Protocol:** All code (notebooks/scripts) should fix random seeds. Log the GPU used (Colab A100) and software environment (CUDA/CuDNN versions, library versions). Each processing step (e.g. “compute CLIP embeddings”) should write a manifest entry with timestamp, input hashes, code version (Git commit), and output hashes. Use workflow tools (e.g. Snakemake, ReproZip) if possible. For further rigor, containerize the environment (Docker) or use Data Version Control (DVC) for dataset snapshots.
    

## Comparison to Other Datasets

- **ImageNet (1.2M images, 1000 classes):** Audubon plates (435 images) are tiny by comparison[en.wikipedia.org](https://en.wikipedia.org/wiki/ImageNet#:~:text=The%20summary%20statistics%20given%20on,24), but each is high-detail art. Unlike web-scraped natural images, these are curated scientific illustrations.
    
- **WikiArt (≈81k paintings, 27 styles)[huggingface.co](https://huggingface.co/datasets/huggan/wikiart#:~:text=Dataset%20containing%2081%2C444%20pieces%20of,labels%20for%20each%20image):** Our dataset is smaller and domain-specific (birds vs general art). WikiArt illustrates that style/genre labels are useful[huggingface.co](https://huggingface.co/datasets/huggan/wikiart#:~:text=Dataset%20containing%2081%2C444%20pieces%20of,labels%20for%20each%20image); we could analogously label plates by “artistic style” (e.g. engraving, lithograph) or by depicted environment (coastal, forest, etc.).
    
- **Bird Datasets (CUB-200: ~12k images[visipedia.github.io](https://visipedia.github.io/datasets.html#:~:text=Caltech), NABirds: ~48k[visipedia.github.io](https://visipedia.github.io/datasets.html#:~:text=NABirds)):** Those are real bird photos with species labels. Audubon plates depict many of the same species, but in art form. We might annotate the scientific species for each plate (Latin name from inscription) to link with these datasets.
    
- **CLIP Benchmarks:** Audubon plates have not appeared in standard vision benchmarks. However, CLIP’s original evaluation included fine-grained tasks like CUB (zero-shot)[arxiv.org](https://arxiv.org/abs/2103.00020#:~:text=supervision,often%20competitive%20with%20a%20fully). We could test how well CLIP’s image/text alignment works on these illustrations (e.g. CLIP rank of correct species name). This provides an internal benchmark.
    

## Applications

- **Digital Humanities:** Scholars can analyze how Audubon depicted species (pose, size, setting) and relate it to historical context. For example, linking Audubon’s plates to modern iNaturalist occurrence data (as in [2][github.com](https://github.com/upenndigitalscholarship/audubon-birds-of-penn#:~:text=Plate%20images%20from%20Audubon%27s%20Birds,observations%20posted%20with%20a%20license)) can support studies of historical ranges and climate impact. Text transcription of inscriptions enables searchable archives of species names. Style/genre tags allow art historians to study the printmaking technique or artistic influences.
    
- **Ecology and Conservation:** Each plate corresponds to a real bird species. By geocoding species ranges and comparing to Audubon’s illustrations, one could study changes in species distribution or population health. The “Burning World” climate project suggests stylistically transforming plates to highlight climate threats; our dataset could serve as the training basis for climate-themed generative art (e.g. making a “climate degradation” version of each plate using style transfer models).
    
- **Artistic Use:** The high-res plates can be used to train or fine-tune generative models (Stable Diffusion, Midjourney LoRAs) for vintage bird art. Fine-tuning via LoRA is efficient[arxiv.org](https://arxiv.org/abs/2106.09685#:~:text=parameters%2C%20is%20prohibitively%20expensive,deficiency%20in%20language%20model) and could capture Audubon’s style (lo-res cues like background composition). Artists can also use extracted masks and embeddings to create new mosaics or AR/VR experiences featuring Audubon art.
    
- **Commercial Tools:** The dataset enables AI tools for archival work: for example, GAN-based restoration can clean up aged/damaged prints[granthaalayahpublication.org](https://www.granthaalayahpublication.org/Arts-Journal/ShodhKosh/article/view/6913#:~:text=Abstract%20)[granthaalayahpublication.org](https://www.granthaalayahpublication.org/Arts-Journal/ShodhKosh/article/view/6913#:~:text=similarity%20preserving%20loss%20functions%2C%20similarity,The%20findings%20in%20the). OCR’d text allows building a searchable database (a knowledge graph of Audubon’s birds). Embeddings could support an “image search” of plates by descriptive query (“brown bird on pine branch”). A curated, citable dataset can underlie museum or educational apps (e.g. interactive guides to Audubon’s works).
    

## Computational Requirements

- **GPU-Intensive Steps:** Extracting CLIP embeddings and running SAM typically require a GPU (Colab A100). CLIP inference on 435 images is fast (<1 s/image) but SAM mask generation might be slower (each image yields hundreds of masks). Fine-tuning or training LoRA models definitely needs GPU.
    
- **CPU Tasks:** Computing histograms, checksums, loading/saving Parquet, OCR (if using CPU-based Tesseract) can be done on CPU. Plan to parallelize CPU-bound tasks (e.g. image reading) for speed.
    
- **Optimizations:** Batch operations (e.g. processing images in arrays) help. Profiling suggests storing intermediate arrays in memory carefully. If resource-constrained, one may skip full-scan of all SAM prompts and instead focus on salient objects.
    

## Storage and Distribution

- **Parquet vs Raw Files:** For final release, use a **Parquet** file for tabular data (metadata + embeddings) because it bundles everything with compression[huggingface.co](https://huggingface.co/docs/hub/en/datasets-image#:~:text=Parquet%20format)[discuss.huggingface.co](https://discuss.huggingface.co/t/image-dataset-best-practices/13974#:~:text=2,It%E2%80%99s%20nice%20on%20several%20aspects). For raw images, due to size we may use git LFS or provide download links. The HuggingFace forum advises Parquet for big, frozen datasets[discuss.huggingface.co](https://discuss.huggingface.co/t/image-dataset-best-practices/13974#:~:text=Option%202.%20Is%20the%20go,like%20parallel%20processing%20or%20streaming) and raw files for small ones[discuss.huggingface.co](https://discuss.huggingface.co/t/image-dataset-best-practices/13974#:~:text=3,especially%20for%20small%20datasets%2C%20however). Since 435 plates is moderate, we could package images in a few tar archives (WebDataset) along with Parquet metadata.
    
- **Compression/Archival:** Archive raw images as high-quality JPEG2000 or PNG (lossless) for preservation. Use ZSTD/Snappy compression for Parquet shards. Maintain a `metadata.parquet` with one row per plate embedding all computed columns. Optionally provide a separate CSV/JSON for simpler access.
    
- **Public Sharing:** Consider hosting on a data repository (Zenodo, Figshare) or a museum digital archive (ensuring compliance with Audubon’s terms[github.com](https://github.com/nathanbuchar/audubon-bird-plates#:~:text=A%20collection%20of%20all%20435,9GB)). For easy ML access, publish a HuggingFace dataset with Parquet+images.
    

## Extensions and Benchmarks

- **LoRA Fine-Tuning:** The plates can train a LoRA on a diffusion model for bird art. Recent work shows LoRA adapts large models with few updates[arxiv.org](https://arxiv.org/abs/2106.09685#:~:text=,reduce%20the%20number%20of%20trainable). Prepare a dedicated directory of images (with license tags) to fine-tune a model on Audubon style.
    
- **Additional Embeddings:** Beyond CLIP, one could extract other embeddings: e.g. DINOv2 or SwAV (self-supervised vision embeddings), or language model embeddings of OCR text. For “emotion” or “colorfulness”, use pretrained CNNs (e.g. VGG) or custom MLPs on pixel features.
    
- **Ablations:** Perform systematic tests: e.g. how many SAM masks vs embedding accuracy? Does segmentation improve image search? Compare CLIP zero-shot label accuracy with/without background masking. For historical art focus, compare with color-histograms only vs full CNN features.
    
- **Evaluation:** Because there is no ground truth “task” on these plates, evaluation can be proxy: e.g. retrieval precision (can we find all plates of “Cardinal” by querying “Cardinal bird”?). Or measure text OCR accuracy against known species names.
    

## Reproducibility Measures

- **Checksums:** We log SHA-256 for every file (raw, intermediate, final). Each manifest row ties a run_id to input/output hashes.
    
- **Schema Enforcement:** Use JSON Schema (as above) to validate all metadata. Enforce types (e.g. `plate_number` 1–435) to catch errors.
    
- **Data Formats:** Store tabular data in Parquet with clearly defined column types. For binary features (like embeddings), consider fixed-size arrays or Feather. Keep code for reading these formats in the repo.
    
- **Provenance Tagging:** Each figure or analysis step should cite which data version and code commit was used. Provide a DOI for the dataset release if possible.
    

**In summary**, this plan details the full pipeline – from raw image ingestion (with hashing and schema-checked metadata) through feature extraction (statistics, embeddings, segmentation) and storage (Parquet/WebDataset) – all with rigorous reproducibility. By comparing to large datasets like ImageNet[en.wikipedia.org](https://en.wikipedia.org/wiki/ImageNet#:~:text=The%20summary%20statistics%20given%20on,24), WikiArt[huggingface.co](https://huggingface.co/datasets/huggan/wikiart#:~:text=Dataset%20containing%2081%2C444%20pieces%20of,labels%20for%20each%20image), and CLIP benchmarks[arxiv.org](https://arxiv.org/abs/2103.00020#:~:text=supervision,often%20competitive%20with%20a%20fully), we see that Audubon’s plates form a unique, smaller-scale corpus with rich application potential (digital humanities, ecology, art restoration, and AI art). The plan includes GPU-dependent steps (SAM, CLIP, model fine-tuning) and also CPU tasks, explicitly noting where optimizations and parallelism can help. All recommendations are backed by recent literature (e.g. SAM segmentation[arxiv.org](https://arxiv.org/abs/2304.02643#:~:text=,URL%20to%20foster%20research%20into), CLIP embeddings[arxiv.org](https://arxiv.org/abs/2103.00020#:~:text=supervision,often%20competitive%20with%20a%20fully), data-format best practices[discuss.huggingface.co](https://discuss.huggingface.co/t/image-dataset-best-practices/13974#:~:text=2,It%E2%80%99s%20nice%20on%20several%20aspects)[discuss.huggingface.co](https://discuss.huggingface.co/t/image-dataset-best-practices/13974#:~:text=3,especially%20for%20small%20datasets%2C%20however), GAN restoration[granthaalayahpublication.org](https://www.granthaalayahpublication.org/Arts-Journal/ShodhKosh/article/view/6913#:~:text=Abstract%20)[granthaalayahpublication.org](https://www.granthaalayahpublication.org/Arts-Journal/ShodhKosh/article/view/6913#:~:text=similarity%20preserving%20loss%20functions%2C%20similarity,The%20findings%20in%20the)). This comprehensive blueprint should support both an academic publication and an open-access museum-style dataset release.

 

**Sources:** Primary dataset described in Buchar’s repository[github.com](https://github.com/nathanbuchar/audubon-bird-plates#:~:text=A%20collection%20of%20all%20435,9GB); methods and comparisons from CLIP and SAM papers[arxiv.org](https://arxiv.org/abs/2103.00020#:~:text=supervision,often%20competitive%20with%20a%20fully)[arxiv.org](https://arxiv.org/abs/2304.02643#:~:text=,URL%20to%20foster%20research%20into); dataset references (WikiArt[huggingface.co](https://huggingface.co/datasets/huggan/wikiart#:~:text=Dataset%20containing%2081%2C444%20pieces%20of,labels%20for%20each%20image), bird datasets[visipedia.github.io](https://visipedia.github.io/datasets.html#:~:text=Caltech)); and data handling best practices[huggingface.co](https://huggingface.co/docs/hub/en/datasets-image#:~:text=Parquet%20format)[discuss.huggingface.co](https://discuss.huggingface.co/t/image-dataset-best-practices/13974#:~:text=2,It%E2%80%99s%20nice%20on%20several%20aspects)[discuss.huggingface.co](https://discuss.huggingface.co/t/image-dataset-best-practices/13974#:~:text=3,especially%20for%20small%20datasets%2C%20however). Each suggestion above is drawn from or inspired by these and other cited works.

## References (cleaned for Obsidian)

- Primary corpus wrapper (GitHub): https://github.com/nathanbuchar/audubon-bird-plates
- Upstream image host (audubon.org plates): `https://www.audubon.org/sites/default/files/boa_plates/plate-<N>-<slug>.jpg`
- CLIP paper: https://arxiv.org/abs/2103.00020
- SAM paper: https://arxiv.org/abs/2304.02643
- LoRA paper: https://arxiv.org/abs/2106.09685
- Hugging Face docs (images + Parquet/WebDataset): https://huggingface.co/docs/hub/en/datasets-image
- Hugging Face forum (image dataset best practices): https://discuss.huggingface.co/t/image-dataset-best-practices/13974
- WikiArt dataset (style comparisons): https://huggingface.co/datasets/huggan/wikiart
- Visipedia dataset index (bird datasets): https://visipedia.github.io/datasets.html
- ImageNet overview (benchmark comparisons): https://en.wikipedia.org/wiki/ImageNet
- OCR models overview (blog): https://modal.com/blog/8-top-open-source-ocr-models-compared
- Restoration paper mentioned: https://www.granthaalayahpublication.org/Arts-Journal/ShodhKosh/article/view/6913
- OpenReview (Personalize SAM with One Shot): https://openreview.net/forum?id=6Gzkhoc6YS

## Citations (raw scrape; preserved verbatim)

```text

[

![](https://www.google.com/s2/favicons?domain=https://github.com&sz=32)

GitHub - nathanbuchar/audubon-bird-plates: All 435 illustrations of John James Audubon's Birds of America.

https://github.com/nathanbuchar/audubon-bird-plates

](https://github.com/nathanbuchar/audubon-bird-plates#:~:text=Audubon%20Bird%20Plates)[

![](https://www.google.com/s2/favicons?domain=https://github.com&sz=32)

GitHub - nathanbuchar/audubon-bird-plates: All 435 illustrations of John James Audubon's Birds of America.

https://github.com/nathanbuchar/audubon-bird-plates

](https://github.com/nathanbuchar/audubon-bird-plates#:~:text=A%20collection%20of%20all%20435,9GB)[

data.json

file://file_000000005048722fac48a6d0d07ded06

](file://file_000000005048722fac48a6d0d07ded06%23:~:text=,turkey.jpg"%20},%20{%20"plate":%202/)[

run.manifest.schema.json

file://file_00000000057c720c9d44ec8201123e0c

](file://file_00000000057c720c9d44ec8201123e0c%23:~:text=,time/)[

plate.manifest.schema.json

file://file_00000000d530722f83fdabc2a54be3ea

](file://file_00000000d530722f83fdabc2a54be3ea%23:~:text=,/)[

run.manifest.schema.json

file://file_00000000057c720c9d44ec8201123e0c

](file://file_00000000057c720c9d44ec8201123e0c%23:~:text=,time"/)[

run.manifest.schema.json

file://file_00000000057c720c9d44ec8201123e0c

](file://file_00000000057c720c9d44ec8201123e0c%23:~:text=,/)[

![](https://www.google.com/s2/favicons?domain=https://arxiv.org&sz=32)

[2103.00020] Learning Transferable Visual Models From Natural Language Supervision

https://arxiv.org/abs/2103.00020

](https://arxiv.org/abs/2103.00020#:~:text=supervision,often%20competitive%20with%20a%20fully)[

![](https://www.google.com/s2/favicons?domain=https://github.com&sz=32)

GitHub - upenndigitalscholarship/audubon-birds-of-penn: Creative Approaches to Data Workshop for Earth Week Data Jam 2022

https://github.com/upenndigitalscholarship/audubon-birds-of-penn

](https://github.com/upenndigitalscholarship/audubon-birds-of-penn#:~:text=Plate%20images%20from%20Audubon%27s%20Birds,observations%20posted%20with%20a%20license)[

![](https://www.google.com/s2/favicons?domain=https://huggingface.co&sz=32)

huggan/wikiart · Datasets at Hugging Face

https://huggingface.co/datasets/huggan/wikiart

](https://huggingface.co/datasets/huggan/wikiart#:~:text=Dataset%20containing%2081%2C444%20pieces%20of,labels%20for%20each%20image)[

![](https://www.google.com/s2/favicons?domain=https://arxiv.org&sz=32)

[2304.02643] Segment Anything

https://arxiv.org/abs/2304.02643

](https://arxiv.org/abs/2304.02643#:~:text=,URL%20to%20foster%20research%20into)[

Personalize Segment Anything Model with One Shot - OpenReview

https://openreview.net/forum?id=6Gzkhoc6YS

](https://openreview.net/forum?id=6Gzkhoc6YS#:~:text=Personalize%20Segment%20Anything%20Model%20with,shot%20classification)[

![](https://www.google.com/s2/favicons?domain=https://modal.com&sz=32)

8 Top Open-Source OCR Models Compared: A Complete Guide

https://modal.com/blog/8-top-open-source-ocr-models-compared

](https://modal.com/blog/8-top-open-source-ocr-models-compared#:~:text=Tesseract%20is%20the%20most%20established,ready)[

![](https://www.google.com/s2/favicons?domain=https://huggingface.co&sz=32)

Image Dataset

https://huggingface.co/docs/hub/en/datasets-image

](https://huggingface.co/docs/hub/en/datasets-image#:~:text=Parquet%20format)[

![](https://www.google.com/s2/favicons?domain=https://discuss.huggingface.co&sz=32)

Image dataset best practices? - Datasets - Hugging Face Forums

https://discuss.huggingface.co/t/image-dataset-best-practices/13974

](https://discuss.huggingface.co/t/image-dataset-best-practices/13974#:~:text=2,It%E2%80%99s%20nice%20on%20several%20aspects)[

![](https://www.google.com/s2/favicons?domain=https://huggingface.co&sz=32)

Image Dataset

https://huggingface.co/docs/hub/en/datasets-image

](https://huggingface.co/docs/hub/en/datasets-image#:~:text=WebDataset%20format)[

![](https://www.google.com/s2/favicons?domain=https://en.wikipedia.org&sz=32)

ImageNet - Wikipedia

https://en.wikipedia.org/wiki/ImageNet

](https://en.wikipedia.org/wiki/ImageNet#:~:text=The%20summary%20statistics%20given%20on,24)[

Datasets | Visipedia

https://visipedia.github.io/datasets.html

](https://visipedia.github.io/datasets.html#:~:text=Caltech)[

Datasets | Visipedia

https://visipedia.github.io/datasets.html

](https://visipedia.github.io/datasets.html#:~:text=NABirds)[

![](https://www.google.com/s2/favicons?domain=https://arxiv.org&sz=32)

[2106.09685] LoRA: Low-Rank Adaptation of Large Language Models

https://arxiv.org/abs/2106.09685

](https://arxiv.org/abs/2106.09685#:~:text=parameters%2C%20is%20prohibitively%20expensive,deficiency%20in%20language%20model)[

![](https://www.google.com/s2/favicons?domain=https://www.granthaalayahpublication.org&sz=32)

GAN-BASED RECONSTRUCTION OF VINTAGE PRINTS | ShodhKosh: Journal of Visual and Performing Arts

https://www.granthaalayahpublication.org/Arts-Journal/ShodhKosh/article/view/6913

](https://www.granthaalayahpublication.org/Arts-Journal/ShodhKosh/article/view/6913#:~:text=Abstract%20)[

![](https://www.google.com/s2/favicons?domain=https://www.granthaalayahpublication.org&sz=32)

GAN-BASED RECONSTRUCTION OF VINTAGE PRINTS | ShodhKosh: Journal of Visual and Performing Arts

https://www.granthaalayahpublication.org/Arts-Journal/ShodhKosh/article/view/6913

](https://www.granthaalayahpublication.org/Arts-Journal/ShodhKosh/article/view/6913#:~:text=similarity%20preserving%20loss%20functions%2C%20similarity,The%20findings%20in%20the)[

![](https://www.google.com/s2/favicons?domain=https://discuss.huggingface.co&sz=32)

Image dataset best practices? - Datasets - Hugging Face Forums

https://discuss.huggingface.co/t/image-dataset-best-practices/13974

](https://discuss.huggingface.co/t/image-dataset-best-practices/13974#:~:text=Option%202.%20Is%20the%20go,like%20parallel%20processing%20or%20streaming)[

![](https://www.google.com/s2/favicons?domain=https://discuss.huggingface.co&sz=32)

Image dataset best practices? - Datasets - Hugging Face Forums

https://discuss.huggingface.co/t/image-dataset-best-practices/13974

](https://discuss.huggingface.co/t/image-dataset-best-practices/13974#:~:text=3,especially%20for%20small%20datasets%2C%20however)[

![](https://www.google.com/s2/favicons?domain=https://arxiv.org&sz=32)

[2106.09685] LoRA: Low-Rank Adaptation of Large Language Models

https://arxiv.org/abs/2106.09685

](https://arxiv.org/abs/2106.09685#:~:text=,reduce%20the%20number%20of%20trainable)[

Datasets | Visipedia

https://visipedia.github.io/datasets.html

](https://visipedia.github.io/datasets.html#:~:text=Caltech)

All Sources

[

![](https://www.google.com/s2/favicons?domain=https://github.com&sz=32)

github

](https://github.com/nathanbuchar/audubon-bird-plates#:~:text=Audubon%20Bird%20Plates)[

data.json

](https://chatgpt.com/c/data.json)[

run.mani...hema.json

](https://chatgpt.com/c/run.manifest.schema.json)[

plate.ma...hema.json

](https://chatgpt.com/c/plate.manifest.schema.json)[

![](https://www.google.com/s2/favicons?domain=https://arxiv.org&sz=32)

arxiv

](https://arxiv.org/abs/2103.00020#:~:text=supervision,often%20competitive%20with%20a%20fully)[

![](https://www.google.com/s2/favicons?domain=https://huggingface.co&sz=32)

huggingface

](https://huggingface.co/datasets/huggan/wikiart#:~:text=Dataset%20containing%2081%2C444%20pieces%20of,labels%20for%20each%20image)[

openreview

](https://openreview.net/forum?id=6Gzkhoc6YS#:~:text=Personalize%20Segment%20Anything%20Model%20with,shot%20classification)[

![](https://www.google.com/s2/favicons?domain=https://modal.com&sz=32)

modal

](https://modal.com/blog/8-top-open-source-ocr-models-compared#:~:text=Tesseract%20is%20the%20most%20established,ready)[

![](https://www.google.com/s2/favicons?domain=https://discuss.huggingface.co&sz=32)

discuss.huggingface

](https://discuss.huggingface.co/t/image-dataset-best-practices/13974#:~:text=2,It%E2%80%99s%20nice%20on%20several%20aspects)[

![](https://www.google.com/s2/favicons?domain=https://en.wikipedia.org&sz=32)

en.wikipedia

](https://en.wikipedia.org/wiki/ImageNet#:~:text=The%20summary%20statistics%20given%20on,24)[

visipedia.github

](https://visipedia.github.io/datasets.html#:~:text=Caltech)[

![](https://www.google.com/s2/favicons?domain=https://www.granthaalayahpublication.org&sz=32)

granthaa...blication

](https://www.granthaalayahpublication.org/Arts-Journal/ShodhKosh/article/view/6913#:~:text=Abstract%20)
```
