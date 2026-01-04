from __future__ import annotations

import argparse
import json
from collections import defaultdict
from pathlib import Path


def parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser(description="Report exact perceptual-hash collisions for a cpu-baseline run.")
    p.add_argument("--output-root", type=Path, required=True, help="Points at _RUN_OUTPUT/")
    p.add_argument("--run-id", type=str, required=True)
    p.add_argument("--hash", dest="hash_name", type=str, default="ahash", choices=["ahash", "dhash", "phash"])
    return p.parse_args()


def main() -> int:
    args = parse_args()
    run_id = args.run_id

    cpu_files = list(args.output_root.rglob(f"{run_id}/cpu_baseline.json"))
    if not cpu_files:
        raise SystemExit(f"No cpu_baseline.json found for run_id={run_id} under {args.output_root}")

    buckets: dict[str, list[str]] = defaultdict(list)
    for p in cpu_files:
        d = json.loads(p.read_text(encoding="utf-8"))
        h = (d.get("hashes") or {}).get(args.hash_name)
        if not h:
            continue
        buckets[str(h)].append(str(d.get("plate_id", p.parent.parent.name)))

    collisions = [(h, sorted(ids)) for h, ids in buckets.items() if len(ids) > 1]
    collisions.sort(key=lambda x: (-len(x[1]), x[0]))

    print(f"run_id={run_id} hash={args.hash_name} plates={len(cpu_files)} collisions={len(collisions)}")
    for h, ids in collisions:
        print(f"{h} n={len(ids)}: {', '.join(ids)}")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
