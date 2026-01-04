from __future__ import annotations

import argparse
import hashlib
import shutil
from pathlib import Path


def sha256_file(path: Path, chunk_size: int = 1024 * 1024) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(chunk_size), b""):
            h.update(chunk)
    return h.hexdigest()


def repo_root() -> Path:
    return Path(__file__).resolve().parents[2]


def parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser(description="Copy repo versioned JSON schemas into a dataset root.")
    p.add_argument("--dataset-root", type=Path, required=True)
    p.add_argument("--schemas-root", type=Path, default=None, help="Defaults to <repo>/schemas/")
    p.add_argument("--overwrite", action="store_true", help="Overwrite even if destination exists.")
    p.add_argument("--dry-run", action="store_true", help="Print actions but do not write.")
    return p.parse_args()


def main() -> int:
    args = parse_args()

    dataset_root: Path = args.dataset_root
    src_root = args.schemas_root or (repo_root() / "schemas")
    dst_root = dataset_root / "schemas"

    if not src_root.exists():
        raise SystemExit(f"Missing schemas root: {src_root}")

    schema_files = sorted([p for p in src_root.glob("*.schema.json") if p.is_file()])
    if not schema_files:
        raise SystemExit(f"No *.schema.json files found in: {src_root}")

    planned: list[tuple[Path, Path, str]] = []
    for src in schema_files:
        dst = dst_root / src.name
        if dst.exists() and not args.overwrite:
            if sha256_file(src) == sha256_file(dst):
                planned.append((src, dst, "skip (identical)"))
                continue
            planned.append((src, dst, "update"))
            continue
        planned.append((src, dst, "write"))

    for src, dst, action in planned:
        print(f"{action}: {src} -> {dst}")

    if args.dry_run:
        return 0

    dst_root.mkdir(parents=True, exist_ok=True)
    for src, dst, action in planned:
        if action.startswith("skip"):
            continue
        shutil.copy2(src, dst)

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
