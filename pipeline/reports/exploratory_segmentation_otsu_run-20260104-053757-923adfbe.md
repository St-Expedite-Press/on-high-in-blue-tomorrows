# Exploratory Run Report — Segmentation (Otsu Luma)

Run ID: `run-20260104-053757-923adfbe`  
Date (UTC): `2026-01-04T05:37:57Z`  
Run output root: `audubon-bird-plates-copy-1/_RUN_OUTPUT/`

## What We Ran

This exploratory run generated a cheap, CPU-only segmentation per plate using Otsu thresholding on luma:

- Convert to grayscale luma (`L`), downsample to `max_dim=1024` (aspect-preserving).
- Compute Otsu threshold on the 0–255 luma histogram.
- Emit a binary mask where “dark is foreground” (`luma < threshold`).

Artifacts written (append-only, per plate):

- `plates_structured/<plate_id>/runs/<run_id>/metrics.json`
- `plates_structured/<plate_id>/runs/<run_id>/segmentation.json`
- `plates_structured/<plate_id>/runs/<run_id>/segmentation_mask.png`

Run-level report:

- `reports/<run_id>/report.json`

## Outcome (High-Level)

The run completed cleanly:

- Plates processed: `435/435`
- Decode failures: `0`
- Schema failures: `0`
- Plates skipped: `0`

Outputs present:

- `segmentation.json`: `435`
- `segmentation_mask.png`: `435`

## Summary Statistics (Quick QC)

These values are informative (variance/QC), not “ground truth”:

- Otsu threshold (luma, 0–255): min `150`, median `175`, p99 `199`, max `202`
- Foreground ratio (“dark is foreground”): min `0.0255`, median `0.2535`, p99 `0.6532`, max `0.7106`
- Mask geometries: `73` unique (expected due to aspect ratio preservation under `max_dim=1024`)
  - Most common: `843×1024` (`237` plates), `1024×604` (`117` plates)

## What It Appears To Capture

This is a “first-pass ink-vs-paper” separation:

- Dark lines, text, and heavy pigment become foreground.
- Bright paper/background becomes background.

This primarily captures scan presentation (digitization pipeline tone, exposure, whitening, and framing), not artistic intent.

Because it’s global thresholding on luma, it is sensitive to digitization tone (scanner whitening, exposure) and the corpus-wide highlight clipping already observed in the CPU baseline.

## Issues Observed (And Why They Matter)

### 1) Sensitivity to digitization tone / highlight clipping

Plates with very low foreground ratio are likely cases where the scan is extremely bright/whitened or heavily clipped at high luma, making “ink” occupy very little of the downsampled mask.

Lowest foreground ratio examples:

- `plate-009` (fg `0.0255`, threshold `192`)
- `plate-015` (fg `0.0529`, threshold `181`)
- `plate-150` (fg `0.0544`, threshold `178`)
- `plate-013` (fg `0.0612`, threshold `179`)

These overlap with the “blown highlights” outliers from the CPU baseline run, which is consistent: global thresholding becomes less stable when a large fraction of pixels are pegged at maximum luma.

### 2) Extremes are not necessarily “bad”

Very high foreground ratio can happen for legitimate reasons (dense linework, dark background, heavy borders/crops), but they should be candidates for inspection because they can indicate:

- unusual framing or background,
- severe underexposure,
- compression artifacts that darken large regions.

Highest foreground ratio examples:

- `plate-279` (fg `0.7106`, threshold `200`)
- `plate-240` (fg `0.6811`, threshold `186`)
- `plate-273` (fg `0.6725`, threshold `187`)

### 3) Mask is intentionally downsampled

The segmentation mask is not at original resolution; it is a derived artifact for QC/triage. It should not be treated as a final segmentation surface for publication without either:

- re-running at higher resolution, or
- defining an upsampling/alignment policy as another derived artifact.

## How This Might Be Improved (Future Work)

While preserving provenance discipline (derived outputs only):

- Add an optional derived standardization step (e.g., percentile-based luma normalization) and run Otsu on the standardized luma as a separate run “model”.
- Add local/adaptive thresholding (still CPU-cheap) as an alternative baseline to reduce sensitivity to global exposure.
- Add a second mask polarity and store both (dark-foreground vs light-foreground) if plate backgrounds vary.
- If moving toward semantic segmentation, register a model in `A_World_Burning/29-model-library.md` and treat it as an explicit instrument with documented failure modes.

Any such normalization/adaptive method should be evaluated comparatively against this run as the baseline anchor, not treated as a replacement.

## What Else There Is To Do Next (If We’re Happy With This Run)

1. Build an “inspection list” export for outliers:
   - lowest/highest foreground ratio,
   - lowest/highest thresholds,
   - combined with CPU baseline clipping metrics.
2. Decide what segmentation is for (QC routing vs canonical measurement vs downstream interpretation), and encode that as policy.
3. If the next stage is embeddings/semantic segmentation, define the smallest model set and the exact artifacts to write under `runs/<run_id>/`.

## Conclusion

Operationally, this segmentation run is a success (complete coverage, no decode/schema failures). Epistemically, it functions as a fast, interpretable triage layer that is predictably sensitive to digitization tone—especially highlight clipping—so it should be used as a QC and routing signal rather than a final segmentation claim.
