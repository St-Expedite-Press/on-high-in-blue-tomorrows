from __future__ import annotations

import argparse
import hashlib
import json
import math
from datetime import datetime, timezone
from pathlib import Path

import numpy as np
from jsonschema import Draft202012Validator
from PIL import Image
from tqdm import tqdm

Image.MAX_IMAGE_PIXELS = None

TILE_SIZE = 512
HIST_BINS = 256
LAPLACE_MAX_DIM = 1024
PHASH_BITS = 8
PHASH_FACTOR = 4


def utc_iso() -> str:
    return datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")


def sha256_file(path: Path, chunk_size: int = 1024 * 1024) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(chunk_size), b""):
            h.update(chunk)
    return h.hexdigest()


def generate_run_id(models: list[str], note: str) -> str:
    stamp = datetime.now(timezone.utc).strftime("%Y%m%d-%H%M%S")
    payload = "|".join(models) + "|" + note
    short = hashlib.sha1(payload.encode("utf-8")).hexdigest()[:8]
    return f"run-{stamp}-{short}"


def resize_fit(img: Image.Image, max_dim: int) -> Image.Image:
    w, h = img.size
    m = max(w, h)
    if m <= max_dim:
        return img
    s = max_dim / m
    return img.resize((max(1, int(round(w * s))), max(1, int(round(h * s)))), resample=Image.BILINEAR)


def laplacian_variance(gray_img: Image.Image) -> float:
    g = resize_fit(gray_img, LAPLACE_MAX_DIM)
    a = np.asarray(g, dtype=np.float32)
    ap = np.pad(a, ((1, 1), (1, 1)), mode="edge")
    out = ap[:-2, 1:-1] + ap[2:, 1:-1] + ap[1:-1, :-2] + ap[1:-1, 2:] - 4.0 * ap[1:-1, 1:-1]
    return float(np.var(out))


def hist_stats(hist: list[int]) -> dict:
    total = int(sum(hist))
    if total <= 0:
        return {
            "total": 0,
            "min": None,
            "max": None,
            "mean": None,
            "std": None,
            "clipped_low_ratio": None,
            "clipped_high_ratio": None,
        }
    mn = next((i for i, c in enumerate(hist) if c), 0)
    mx = next((255 - i for i, c in enumerate(reversed(hist)) if c), 255)
    mean = sum(i * c for i, c in enumerate(hist)) / total
    s2 = sum((i - mean) ** 2 * c for i, c in enumerate(hist)) / total
    return {
        "total": total,
        "min": int(mn),
        "max": int(mx),
        "mean": float(mean),
        "std": float(math.sqrt(s2)),
        "clipped_low_ratio": float(hist[0] / total),
        "clipped_high_ratio": float(hist[-1] / total),
    }


def entropy(hist: list[int]) -> float | None:
    total = float(sum(hist))
    if total <= 0:
        return None
    ent = 0.0
    for c in hist:
        if c:
            p = c / total
            ent -= p * math.log2(p)
    return float(ent)


def ahash(img: Image.Image, size: int = 8) -> str:
    g = img.convert("L").resize((size, size), Image.BILINEAR)
    a = np.asarray(g, dtype=np.float32)
    m = a.mean()
    bits = (a > m).astype(np.uint8).flatten()
    v = 0
    for b in bits:
        v = (v << 1) | int(b)
    return f"{v:0{(size * size) // 4}x}"


def dhash(img: Image.Image, size: int = 8) -> str:
    g = img.convert("L").resize((size + 1, size), Image.BILINEAR)
    a = np.asarray(g, dtype=np.float32)
    diff = (a[:, 1:] > a[:, :-1]).astype(np.uint8).flatten()
    v = 0
    for b in diff:
        v = (v << 1) | int(b)
    return f"{v:0{(size * size) // 4}x}"


def phash(img: Image.Image, hash_bits: int = PHASH_BITS, highfreq_factor: int = PHASH_FACTOR) -> str:
    n = hash_bits * highfreq_factor
    g = img.convert("L").resize((n, n), Image.BILINEAR)
    a = np.asarray(g, dtype=np.float32)
    idx = np.arange(n)
    k = idx.reshape(-1, 1)
    cos = np.cos(np.pi / n * (idx + 0.5) * k).astype(np.float32)
    d1 = cos @ a
    d2 = (cos @ d1.T).T
    d = d2[:hash_bits, :hash_bits].flatten()
    med = np.median(d[1:]) if d.size > 1 else np.median(d)
    bits = (d > med).astype(np.uint8)
    v = 0
    for b in bits:
        v = (v << 1) | int(b)
    return f"{v:0{(hash_bits * hash_bits) // 4}x}"


def load_schema(path: Path) -> Draft202012Validator:
    schema = json.loads(path.read_text(encoding="utf-8"))
    Draft202012Validator.check_schema(schema)
    return Draft202012Validator(schema)


def parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser()
    p.add_argument("--dataset-root", type=Path, required=True)
    p.add_argument("--output-root", type=Path, required=True)
    p.add_argument("--shard-index", type=int, default=0)
    p.add_argument("--shard-count", type=int, default=1)
    p.add_argument("--run-id", type=str, default=None)
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
    cpu_schema_path = schemas_root / "cpu.baseline.schema.json"
    cpu_schema = load_schema(cpu_schema_path) if cpu_schema_path.exists() else None

    plates = sorted([p for p in plates_root.iterdir() if p.is_dir() and p.name.startswith("plate-")])
    if len(plates) != 435:
        raise SystemExit(f"Unexpected plate count: {len(plates)}")

    selected = [p for i, p in enumerate(plates) if i % args.shard_count == args.shard_index]
    models = ["cpu-baseline-v1"]
    note = "cpu baseline: container geometry hist entropy hashes laplacian"
    run_id = args.run_id or generate_run_id(models, note)

    report = {
        "run_id": run_id,
        "timestamp": utc_iso(),
        "dataset_root": str(dataset_root),
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

        out_cpu = out_run_dir / "cpu_baseline.json"
        out_metrics = out_run_dir / "metrics.json"

        if args.skip_if_present and out_cpu.exists() and out_metrics.exists():
            report["plates_skipped"] += 1
            continue

        run_manifest = {
            "run_id": run_id,
            "plate_id": plate_dir.name,
            "timestamp": utc_iso(),
            "models": models,
            "outputs": ["cpu_baseline.json"],
            "notes": note,
        }

        if list(run_schema.iter_errors(run_manifest)):
            report["schema_failures"] += 1
            if len(report["errors_sample"]) < 10:
                report["errors_sample"].append(f"{plate_dir.name}: run manifest schema failure")
            continue

        baseline = {
            "plate_id": manifest["plate_id"],
            "run_id": run_id,
            "timestamp": utc_iso(),
            "source_image": manifest["source_image"],
            "source_file": {
                "bytes": int(src_path.stat().st_size),
                "extension": src_path.suffix.lower().lstrip("."),
                "format": None,
                "sha256": sha256_file(src_path),
            },
            "geometry": {"width_px": None, "height_px": None, "megapixels": None, "aspect_ratio": None, "mode": None},
            "tiling": {"tile_size_px": TILE_SIZE, "tiles_x": 1, "tiles_y": 1, "total_tiles": 1},
            "decode": {"ok": False, "error": None},
            "pixel_stats": None,
            "hashes": None,
        }

        try:
            with Image.open(src_path) as img:
                baseline["source_file"]["format"] = img.format
                w, h = img.size
                baseline["geometry"] = {
                    "width_px": int(w),
                    "height_px": int(h),
                    "megapixels": float(round((w * h) / 1_000_000, 3)),
                    "aspect_ratio": float(w / h),
                    "mode": img.mode,
                }
                tiles_x = (w + TILE_SIZE - 1) // TILE_SIZE
                tiles_y = (h + TILE_SIZE - 1) // TILE_SIZE
                baseline["tiling"] = {
                    "tile_size_px": TILE_SIZE,
                    "tiles_x": int(tiles_x),
                    "tiles_y": int(tiles_y),
                    "total_tiles": int(tiles_x * tiles_y),
                }

                rgb = img.convert("RGB")
                raw = rgb.histogram()
                Rh, Gh, Bh = raw[0:256], raw[256:512], raw[512:768]
                L = rgb.convert("L")
                Lh = L.histogram()

                baseline["pixel_stats"] = {
                    "colorspace": "as-decoded",
                    "rgb_histograms": {"bins": HIST_BINS, "R": Rh, "G": Gh, "B": Bh},
                    "l_histogram": {"bins": HIST_BINS, "L": Lh},
                    "rgb_stats": {"R": hist_stats(Rh), "G": hist_stats(Gh), "B": hist_stats(Bh)},
                    "luma_stats": hist_stats(Lh),
                    "entropy": {"R": entropy(Rh), "G": entropy(Gh), "B": entropy(Bh), "L": entropy(Lh)},
                    "laplacian_var": laplacian_variance(L),
                }
                baseline["hashes"] = {"ahash": ahash(rgb), "dhash": dhash(rgb), "phash": phash(rgb)}
                baseline["decode"] = {"ok": True, "error": None}

        except Exception as e:
            report["decode_failures"] += 1
            baseline["decode"] = {"ok": False, "error": f"{type(e).__name__}: {str(e)[:300]}"}

        if cpu_schema is not None:
            errs = list(cpu_schema.iter_errors(baseline))
            if errs:
                report["schema_failures"] += 1
                if len(report["errors_sample"]) < 10:
                    report["errors_sample"].append(f"{plate_dir.name}: cpu baseline schema failure")
                continue

        out_metrics.write_text(json.dumps(run_manifest, indent=2), encoding="utf-8")
        out_cpu.write_text(json.dumps(baseline, indent=2), encoding="utf-8")
        report["plates_processed"] += 1

    reports_dir = output_root / "reports" / run_id
    reports_dir.mkdir(parents=True, exist_ok=True)
    (reports_dir / "report.json").write_text(json.dumps(report, indent=2), encoding="utf-8")
    print(json.dumps(report, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
