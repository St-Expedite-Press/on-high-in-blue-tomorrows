# Exploratory Run Report - CPU Baseline

Run ID: `run-20260104-043258-877a06a6`  
Date (UTC): `2026-01-04T04:32:58Z`  
Run output root: `audubon-bird-plates-copy-1/_RUN_OUTPUT/`

## What We Ran

This exploratory run generated a "CPU baseline" feature bundle per plate:

- Image geometry (width/height/megapixels/aspect ratio)
- Histogram-based pixel stats for RGB and luma (min/max/mean/std)
- Entropy estimates per channel
- Clipping ratios at 0 and 255 (luma)
- Laplacian variance (blur/detail proxy)
- Perceptual hashes (`ahash`, `dhash`, `phash`)
- Run manifests (`metrics.json`) + a run report (`report.json`)

## Outcome (High-Level)

The run completed cleanly:

- Plates processed: `435/435`
- Decode failures: `0`
- Schema failures: `0`
- Plates skipped: `0`

This indicates the dataset scaffold is consistent (expected `plates_structured/` layout, schema files present, and all source images decodable under the current PIL configuration).

## Summary Statistics (Quick QC)

These are useful to detect drift/outliers, not to "judge" images:

- Megapixels: median `28.737`, p99 `112.917`, max `117.220`
- Laplacian variance: median `590.185`, p1 `231.411`, p99 `1650.142`
- Luma entropy: median `3.987`, p1 `1.187`, p99 `7.285`
- Luma clipping (highlights): median `0.547269`, p99 `0.903535`, max `0.940942`
- Luma clipping (shadows): median `0.00002224`, p99 `0.00055814`, max `0.00678071`

Notable: highlight clipping is widespread in this corpus (very high `clip_L_high_ratio`), while crushed blacks are comparatively rare.

## Issues Observed (And Why They Matter)

### 1) Report field name mismatch (`input_root` vs `dataset_root`)

- The run's `report.json` used `input_root`, while `pipeline/sagemaker/cpu_baseline_job.py` used `dataset_root`.
- Root cause: "Run All" was executed in `notebooks/cpu_baseline_sagemaker_style.ipynb`, which used `input_root` by design (environment-first notebook contract).

Mitigation applied:

- Standardized on `dataset_root` and kept `input_root` as an alias across both notebook and CLI paths.

### 2) Highlight clipping is prevalent

This is likely a property of digitization pipelines (scanner exposure/background/paper glare/whitening) rather than a bug in our run. It matters because it can:

- distort downstream embeddings/segmentation (especially for white backgrounds and faint linework),
- confound comparisons across institutions (different tone curves),
- inflate false similarity for washed-out plates.

Examples with extreme highlight clipping:

- `plate-009` (`clip_L_high_ratio ≈ 0.9409`)
- `plate-015` (`≈ 0.9321`)
- `plate-150` (`≈ 0.9250`)

### 3) Blur / low-detail candidates (low Laplacian variance)

Low Laplacian variance can indicate blur, heavy compression, or very smooth/washed imagery. These are candidates for visual inspection and possible re-acquisition.

Lowest Laplacian variance examples:

- `plate-317` (`laplacian_var ≈ 189.4`)
- `plate-072` (`≈ 198.7`)
- `plate-207` (`≈ 204.4`)

### 4) Hash collision (aHash)

We observed one exact aHash collision:

- `plate-310` and `plate-382` share `ahash=ffffffcf81818181`.

Interpretation:

- This does not necessarily mean duplicates; aHash is low-resolution and can collide for visually similar plates or similar framing/background.

## How These Issues Might Be Addressed (Future Work)

### Standardize run metadata fields

- Keep `dataset_root` as the canonical report key.
- Keep `input_root` as an alias for notebook-style execution environments.
- Add a tiny report normalizer step for older runs if needed.

### Tone / clipping robustness

Options (in increasing interpretive intensity):

- Record color-management signals (ICC presence/hash, EXIF presence, JPEG subsampling/quantization) to explain variance sources.
- Add a normalized-luma representation (e.g., percentile-based contrast normalization) for downstream embeddings as a derived artifact, never overwriting sources.
- Add detection + routing: plates with extreme clipping go through a separate measurement branch with extra warnings and different parameters.

### Better duplicate / near-duplicate detection

- Move from exact-hash collisions to Hamming-distance clustering (especially pHash).
- Track candidate clusters for manual review; do not auto-deduplicate without provenance rules.

### Expand the baseline feature set safely

Without adding ML inference, we can still add cheap, reproducible, interpretable features:

- edge density metrics, simple background/foreground separation heuristics,
- downsampled thumbnails (strictly derived, explicitly labeled),
- compression/encoding forensics fields (where available).

## What Else There Is To Do Next

If we're happy with this exploratory baseline, the next useful steps are:

1. Write an aggregator to produce a single QC table (CSV/Parquet) from all `cpu_baseline.json`.
2. Add pHash near-duplicate clustering + an inspection list export.
3. Formalize thresholds/guardrails ("too clipped", "too blurry", "too small", "too anomalous") and how they affect downstream runs.
4. Decide whether to treat tone normalization as a separate downstream interpretation-layer artifact (recommended) vs part of measurement (risky).

## Note: What "Clipping" Means Here

Clipping is what happens when pixel values hit the hard limits of a representable range and everything beyond those limits collapses to a single value.

For 8-bit images, the luma range is 0-255:

- Anything darker than 0 becomes 0 (shadow clipping).
- Anything brighter than 255 becomes 255 (highlight clipping).

In this run, the very high `clip_L_high_ratio` indicates a large fraction of pixels are pegged at maximum luma. That strongly suggests scanner exposure, aggressive background whitening, or tone-curve normalization during digitization - not something intrinsic to the plates themselves.

Why this matters:

- Once clipping happens, information is irreversibly lost; you can't recover detail that was never recorded.
- That makes clipping a measurement/provenance concern (comparability across institutions), not an aesthetic one.

## Conclusion

This exploratory run is a success operationally (all plates processed, no schema/decode failures) and already reveals meaningful variance signals (especially highlight clipping). The key next step is to use these signals to route and compare future runs without overwriting the core dataset.
