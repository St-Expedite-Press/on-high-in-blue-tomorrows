from __future__ import annotations

import argparse
import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import numpy as np
from jsonschema import Draft202012Validator
from PIL import Image
from tqdm import tqdm

Image.MAX_IMAGE_PIXELS = None

DEFAULT_MAX_DIM = 1024


def utc_iso() -> str:
    return datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")


def generate_run_id(models: list[str], note: str) -> str:
    stamp = datetime.now(timezone.utc).strftime("%Y%m%d-%H%M%S")
    payload = "|".join(models) + "|" + note
    short = hashlib.sha1(payload.encode("utf-8")).hexdigest()[:8]
    return f"run-{stamp}-{short}"


def load_schema(path: Path) -> Draft202012Validator:
    schema = json.loads(path.read_text(encoding="utf-8"))
    Draft202012Validator.check_schema(schema)
    return Draft202012Validator(schema)


def resize_fit(img: Image.Image, max_dim: int) -> Image.Image:
    w, h = img.size
    m = max(w, h)
    if m <= max_dim:
        return img
    s = max_dim / m
    return img.resize((max(1, int(round(w * s))), max(1, int(round(h * s)))), resample=Image.BILINEAR)


def otsu_threshold(hist: list[int]) -> int:
    total = float(sum(hist))
    if total <= 0:
        return 127

    sum_total = 0.0
    for i, c in enumerate(hist):
        sum_total += i * float(c)

    sum_b = 0.0
    w_b = 0.0
    var_max = -1.0
    threshold = 127

    for t in range(256):
        c = float(hist[t])
        w_b += c
        if w_b <= 0:
            continue
        w_f = total - w_b
        if w_f <= 0:
            break
        sum_b += float(t) * c
        m_b = sum_b / w_b
        m_f = (sum_total - sum_b) / w_f
        var_between = w_b * w_f * (m_b - m_f) ** 2
        if var_between > var_max:
            var_max = var_between
            threshold = t

    return int(threshold)


def parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser()
    p.add_argument("--dataset-root", type=Path, required=True)
    p.add_argument("--output-root", type=Path, required=True)
    p.add_argument("--shard-index", type=int, default=0)
    p.add_argument("--shard-count", type=int, default=1)
    p.add_argument("--run-id", type=str, default=None)
    p.add_argument("--max-dim", type=int, default=DEFAULT_MAX_DIM)
    p.add_argument("--skip-if-present", action="store_true")
    return p.parse_args()


def main() -> int:
    args = parse_args()
    dataset_root: Path = args.dataset_root
    output_root: Path = args.output_root

    plates_root = dataset_root / "plates_structured"
    schemas_root = dataset_root / "schemas"

    if not plates_root.exists():
        raise SystemExit(f"Missing plates_structured: {plates_root}")
    if not schemas_root.exists():
        raise SystemExit(f"Missing schemas: {schemas_root}")

    plate_schema = load_schema(schemas_root / "plate.manifest.schema.json")
    run_schema = load_schema(schemas_root / "run.manifest.schema.json")
    seg_schema_path = schemas_root / "segmentation.otsu.schema.json"
    seg_schema = load_schema(seg_schema_path) if seg_schema_path.exists() else None

    plates = sorted([p for p in plates_root.iterdir() if p.is_dir() and p.name.startswith("plate-")])
    if len(plates) != 435:
        raise SystemExit(f"Unexpected plate count: {len(plates)}")

    selected = [p for i, p in enumerate(plates) if i % args.shard_count == args.shard_index]

    models = [f"segmentation-otsu-luma-v1(max_dim={args.max_dim})"]
    note = "cheap luma otsu threshold segmentation (downsampled mask)"
    run_id = args.run_id or generate_run_id(models, note)

    report: dict[str, Any] = {
        "run_id": run_id,
        "timestamp": utc_iso(),
        "dataset_root": str(dataset_root),
        "input_root": str(dataset_root),
        "output_root": str(output_root),
        "shard_index": args.shard_index,
        "shard_count": args.shard_count,
        "plates_total": len(plates),
        "plates_selected": len(selected),
        "plates_processed": 0,
        "plates_skipped": 0,
        "decode_failures": 0,
        "schema_failures": 0,
        "errors_sample": [],
    }

    for plate_dir in tqdm(selected, desc="plates"):
        manifest_path = plate_dir / "manifest.json"
        manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
        if list(plate_schema.iter_errors(manifest)):
            report["schema_failures"] += 1
            if len(report["errors_sample"]) < 10:
                report["errors_sample"].append(f"{plate_dir.name}: plate manifest schema failure")
            continue

        src_path = plate_dir / manifest["source_image"]
        if not src_path.exists():
            report["decode_failures"] += 1
            if len(report["errors_sample"]) < 10:
                report["errors_sample"].append(f"{plate_dir.name}: missing source image")
            continue

        out_plate_dir = output_root / "plates_structured" / plate_dir.name
        out_run_dir = out_plate_dir / "runs" / run_id
        out_run_dir.mkdir(parents=True, exist_ok=True)

        out_seg = out_run_dir / "segmentation.json"
        out_mask = out_run_dir / "segmentation_mask.png"
        out_metrics = out_run_dir / "metrics.json"

        if args.skip_if_present and out_seg.exists() and out_mask.exists() and out_metrics.exists():
            report["plates_skipped"] += 1
            continue

        run_manifest = {
            "run_id": run_id,
            "plate_id": plate_dir.name,
            "timestamp": utc_iso(),
            "models": models,
            "outputs": ["segmentation.json", "segmentation_mask.png"],
            "notes": note,
        }

        if list(run_schema.iter_errors(run_manifest)):
            report["schema_failures"] += 1
            if len(report["errors_sample"]) < 10:
                report["errors_sample"].append(f"{plate_dir.name}: run manifest schema failure")
            continue

        try:
            with Image.open(src_path) as img:
                w0, h0 = img.size
                L = img.convert("L")
                Ls = resize_fit(L, args.max_dim)
                ws, hs = Ls.size

                hist = Ls.histogram()
                thr = otsu_threshold(hist[:256])
                arr = np.asarray(Ls, dtype=np.uint8)
                # Foreground = "ink/dark" pixels
                mask = (arr < thr).astype(np.uint8) * 255

                Image.fromarray(mask, mode="L").save(out_mask, format="PNG", optimize=True)

                foreground_ratio = float(mask.mean() / 255.0)
                seg = {
                    "plate_id": manifest["plate_id"],
                    "run_id": run_id,
                    "timestamp": utc_iso(),
                    "source_image": manifest["source_image"],
                    "method": "otsu-luma-v1",
                    "params": {"max_dim": int(args.max_dim), "threshold": int(thr), "polarity": "dark-is-foreground"},
                    "original_geometry": {"width_px": int(w0), "height_px": int(h0)},
                    "mask_geometry": {"width_px": int(ws), "height_px": int(hs)},
                    "scale": {
                        "x": float(ws / w0) if w0 else None,
                        "y": float(hs / h0) if h0 else None,
                    },
                    "outputs": {"mask_png": "segmentation_mask.png"},
                    "foreground_ratio": foreground_ratio,
                }

        except Exception as e:
            report["decode_failures"] += 1
            if len(report["errors_sample"]) < 10:
                report["errors_sample"].append(f"{plate_dir.name}: {type(e).__name__}: {str(e)[:300]}")
            continue

        if seg_schema is not None:
            errs = list(seg_schema.iter_errors(seg))
            if errs:
                report["schema_failures"] += 1
                if len(report["errors_sample"]) < 10:
                    report["errors_sample"].append(f"{plate_dir.name}: segmentation schema failure")
                continue

        out_metrics.write_text(json.dumps(run_manifest, indent=2), encoding="utf-8")
        out_seg.write_text(json.dumps(seg, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
        report["plates_processed"] += 1

    reports_dir = output_root / "reports" / run_id
    reports_dir.mkdir(parents=True, exist_ok=True)
    (reports_dir / "report.json").write_text(json.dumps(report, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(json.dumps(report, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

