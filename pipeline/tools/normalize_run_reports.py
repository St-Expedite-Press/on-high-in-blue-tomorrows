from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any


def _load_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def _write_json(path: Path, obj: dict[str, Any]) -> None:
    path.write_text(json.dumps(obj, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def normalize_report(report: dict[str, Any]) -> dict[str, Any]:
    dataset_root = report.get("dataset_root")
    input_root = report.get("input_root")

    if dataset_root is None and input_root is not None:
        report["dataset_root"] = input_root
    if input_root is None and dataset_root is not None:
        report["input_root"] = dataset_root

    return report


def iter_report_paths(root: Path) -> list[Path]:
    if root.is_file():
        return [root]
    return sorted(root.glob("**/reports/*/report.json"))


def parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser(description="Normalize run report metadata fields (dataset_root/input_root).")
    p.add_argument(
        "path",
        type=Path,
        help="A report.json path or a directory containing *_RUN_OUTPUT/reports/*/report.json.",
    )
    p.add_argument("--dry-run", action="store_true", help="Print which files would change; do not write.")
    return p.parse_args()


def main() -> int:
    args = parse_args()
    paths = iter_report_paths(args.path)
    if not paths:
        raise SystemExit(f"No report.json files found under: {args.path}")

    changed = 0
    for path in paths:
        original = _load_json(path)
        updated = normalize_report(dict(original))
        if updated != original:
            changed += 1
            if args.dry_run:
                print(f"WOULD_UPDATE {path}")
            else:
                _write_json(path, updated)
                print(f"UPDATED {path}")

    print(f"reports_scanned={len(paths)} reports_changed={changed}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

