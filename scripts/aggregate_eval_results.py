#!/usr/bin/env python3
"""Aggregate designer-filled eval CSVs into a single summary JSON.

Reads every CSV under docs/superpowers/evals/results/<date>-<designer>/*.csv
and emits a structured summary to stdout (or a file via --out).

Output JSON shape:
{
  "meta": {
    "generated_at": "...",
    "designers": [...],
    "result_folders": [...],
    "total_tests_filled": N,
  },
  "per_test": {
    "<test_id>": {
      "command": "...",
      "level": "L<n>",
      "type": "anchor" | "probe",
      "parent_anchor": "..." | null,
      "n_responses": N,
      "avg_score": float | null,
      "score_variance": float | null,
      "pass_rate_per_behaviour": {"behaviour text": 0.83, ...},
      "responses": [
        {"designer": "...", "score": int|null, "pass_fail": "✓✓✗", "surprised_by": "...",
         "screenshot_links": [...], "agent_version": "...", "run_date": "...", "notes": "..."}
      ]
    }
  },
  "per_command": {
    "/design": {
      "n_tests": N,
      "avg_score": float,
      "weak_tests": ["test_id with avg score < 3"],
    }
  },
  "per_level": {
    "L3": {"n_tests": N, "avg_score": float, "weak_tests": [...]}
  },
  "hot_fixes": [
    # probes with pass_rate < 0.5 — these are concrete optimization targets
    {"test_id": "...", "parent_anchor": "...", "pass_rate": 0.4,
     "behaviour": "...", "command": "...", "level": "L3"}
  ],
  "screenshots": [
    {"test_id": "...", "designer": "...", "link": "..."}
  ]
}

Usage:
    python3 scripts/aggregate_eval_results.py docs/superpowers/evals/results/ [--out summary.json]
"""

from __future__ import annotations

import argparse
import csv
import json
import re
import statistics
import sys
from collections import defaultdict
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

LEVEL_FROM_FILENAME = re.compile(r"L(\d)[-_]")
TEST_ID_LEVEL = re.compile(r"^L(\d)-")
PASS_CHAR = "✓"
FAIL_CHAR = "✗"
PARTIAL_CHAR = "~"


def detect_level(filename: str, test_id: str) -> str:
    """L0..L3 from filename first, fall back to test_id prefix."""
    m = LEVEL_FROM_FILENAME.search(filename)
    if m:
        return f"L{m.group(1)}"
    m = TEST_ID_LEVEL.match(test_id)
    if m:
        return f"L{m.group(1)}"
    return "L?"


def parse_pass_fail(value: str, n_behaviours: int) -> list[float | None]:
    """Parse a pass/fail string into per-behaviour scores.

    Each character maps to: ✓ → 1.0, ✗ → 0.0, ~ → 0.5, anything else → None.
    Returns a list of length n_behaviours; pads or truncates as needed.
    """
    if not value:
        return [None] * n_behaviours
    result: list[float | None] = []
    for char in value:
        if char == PASS_CHAR:
            result.append(1.0)
        elif char == FAIL_CHAR:
            result.append(0.0)
        elif char == PARTIAL_CHAR:
            result.append(0.5)
        else:
            # Skip whitespace, commas, other separators
            continue
    # pad / truncate to expected length
    if len(result) < n_behaviours:
        result.extend([None] * (n_behaviours - len(result)))
    return result[:n_behaviours]


def split_behaviours(raw: str) -> list[str]:
    """Split expected_behaviours field into bullets.

    Accepts either newline-separated or '|'-separated bullets.
    """
    if not raw:
        return []
    # Try newline first, then pipe
    if "\n" in raw:
        bullets = [b.strip("- *• ") for b in raw.split("\n") if b.strip()]
    else:
        bullets = [b.strip("- *• ") for b in raw.split("|") if b.strip()]
    return bullets


def extract_links(value: str) -> list[str]:
    if not value:
        return []
    # Drive URLs roughly
    return re.findall(r"https?://[^\s,]+", value)


def parse_score(value: str) -> int | None:
    if not value:
        return None
    value = value.strip()
    if not value:
        return None
    try:
        n = int(float(value))
        if 1 <= n <= 5:
            return n
    except ValueError:
        pass
    return None


def collect_csvs(results_root: Path) -> list[tuple[Path, str]]:
    """Return list of (csv_path, designer_folder_name)."""
    out = []
    for folder in sorted(results_root.iterdir()):
        if not folder.is_dir():
            continue
        for csv_path in sorted(folder.glob("*.csv")):
            out.append((csv_path, folder.name))
    return out


def aggregate(results_root: Path) -> dict[str, Any]:
    csv_files = collect_csvs(results_root)
    if not csv_files:
        print(f"No CSVs found under {results_root}", file=sys.stderr)
        return {}

    # per_test[test_id] = {meta + list of responses}
    per_test: dict[str, dict[str, Any]] = {}
    designers: set[str] = set()
    folders: set[str] = set()
    screenshots: list[dict[str, str]] = []

    for csv_path, folder_name in csv_files:
        folders.add(folder_name)
        with csv_path.open(newline="", encoding="utf-8") as fh:
            reader = csv.DictReader(fh)
            for row in reader:
                test_id = (row.get("test_id") or "").strip()
                if not test_id:
                    continue
                level = detect_level(csv_path.name, test_id)
                command = (row.get("command") or "").strip()
                test_type = (row.get("type") or "").strip()
                parent_anchor = (row.get("parent_anchor") or "").strip() or None
                behaviours = split_behaviours(row.get("expected_behaviours") or "")
                pass_fail_raw = (row.get("pass_fail") or "").strip()
                score = parse_score(row.get("score_overall") or "")
                designer = (row.get("designer") or folder_name).strip()
                if designer:
                    designers.add(designer)
                surprised = (row.get("surprised_by") or "").strip()
                links = []
                for col in ("screenshot_link_1", "screenshot_link_2"):
                    for link in extract_links(row.get(col) or ""):
                        links.append(link)
                        screenshots.append(
                            {"test_id": test_id, "designer": designer, "link": link}
                        )
                # Establish the per_test entry first so we can use its canonical
                # behaviour list for length alignment. This protects against
                # designer CSVs that drift in bullet count from the first-seen.
                if test_id not in per_test:
                    per_test[test_id] = {
                        "command": command,
                        "level": level,
                        "type": test_type,
                        "parent_anchor": parent_anchor,
                        "behaviours": behaviours,
                        "responses": [],
                    }

                canonical_behaviours = per_test[test_id]["behaviours"]
                response = {
                    "designer": designer,
                    "score": score,
                    "pass_fail_raw": pass_fail_raw,
                    "pass_fail_per_behaviour": parse_pass_fail(
                        pass_fail_raw, len(canonical_behaviours)
                    ),
                    "surprised_by": surprised,
                    "screenshot_links": links,
                    "agent_version": (row.get("agent_version") or "").strip(),
                    "run_date": (row.get("run_date") or "").strip(),
                    "notes": (row.get("notes") or "").strip(),
                    "specialization": (row.get("specialization") or "").strip()
                    or None,
                    "ds_context_used": (row.get("ds_context_used") or "").strip()
                    or None,
                }
                per_test[test_id]["responses"].append(response)

    # Compute aggregates
    per_command: dict[str, dict[str, Any]] = defaultdict(
        lambda: {"n_tests": 0, "scores": [], "weak_tests": []}
    )
    per_level: dict[str, dict[str, Any]] = defaultdict(
        lambda: {"n_tests": 0, "scores": [], "weak_tests": []}
    )
    hot_fixes: list[dict[str, Any]] = []

    for tid, t in per_test.items():
        scores = [r["score"] for r in t["responses"] if r["score"] is not None]
        t["n_responses"] = len(t["responses"])
        t["avg_score"] = round(statistics.mean(scores), 2) if scores else None
        t["score_variance"] = (
            round(statistics.pvariance(scores), 2) if len(scores) > 1 else None
        )

        # Pass rate per behaviour
        n_b = len(t["behaviours"])
        pass_rate_per_b: dict[str, float | None] = {}
        for i in range(n_b):
            vals = [
                r["pass_fail_per_behaviour"][i]
                for r in t["responses"]
                if r["pass_fail_per_behaviour"][i] is not None
            ]
            pass_rate_per_b[t["behaviours"][i]] = (
                round(sum(vals) / len(vals), 2) if vals else None
            )
        t["pass_rate_per_behaviour"] = pass_rate_per_b

        # Roll up to per-command and per-level
        if t["avg_score"] is not None:
            per_command[t["command"]]["scores"].append(t["avg_score"])
            per_level[t["level"]]["scores"].append(t["avg_score"])
        per_command[t["command"]]["n_tests"] += 1
        per_level[t["level"]]["n_tests"] += 1

        if t["avg_score"] is not None and t["avg_score"] < 3:
            per_command[t["command"]]["weak_tests"].append(tid)
            per_level[t["level"]]["weak_tests"].append(tid)

        # Hot fixes: probes with any behaviour < 0.5 pass rate
        if t["type"] == "probe":
            for behaviour, pr in pass_rate_per_b.items():
                if pr is not None and pr < 0.5:
                    hot_fixes.append(
                        {
                            "test_id": tid,
                            "parent_anchor": t["parent_anchor"],
                            "pass_rate": pr,
                            "behaviour": behaviour,
                            "command": t["command"],
                            "level": t["level"],
                        }
                    )

    # Finalize per_command / per_level
    for bucket in (per_command, per_level):
        for key, val in bucket.items():
            scores = val.pop("scores")
            val["avg_score"] = (
                round(statistics.mean(scores), 2) if scores else None
            )

    hot_fixes.sort(key=lambda h: h["pass_rate"])

    return {
        "meta": {
            "generated_at": datetime.now(timezone.utc).isoformat().replace("+00:00", "Z"),
            "designers": sorted(designers),
            "result_folders": sorted(folders),
            "total_tests_filled": len(per_test),
        },
        "per_test": per_test,
        "per_command": dict(per_command),
        "per_level": dict(per_level),
        "hot_fixes": hot_fixes,
        "screenshots": screenshots,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    parser.add_argument(
        "results_dir",
        type=Path,
        help="Path to docs/superpowers/evals/results/ (or any folder of date-designer/*.csv)",
    )
    parser.add_argument(
        "--out",
        type=Path,
        default=None,
        help="Write JSON to this path instead of stdout",
    )
    args = parser.parse_args()

    if not args.results_dir.exists() or not args.results_dir.is_dir():
        print(f"Not a directory: {args.results_dir}", file=sys.stderr)
        return 1

    summary = aggregate(args.results_dir)
    payload = json.dumps(summary, indent=2, ensure_ascii=False)
    if args.out:
        args.out.write_text(payload, encoding="utf-8")
        print(f"Wrote {args.out}", file=sys.stderr)
    else:
        print(payload)
    return 0


if __name__ == "__main__":
    sys.exit(main())
