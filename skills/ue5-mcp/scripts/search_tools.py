#!/usr/bin/env python3
"""Search the bundled UE5 MCP catalog without loading it into model context."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any, Iterable


DEFAULT_CATALOG = Path(__file__).resolve().parent.parent / "references" / "toolsets"


def load_json(path: Path) -> dict[str, Any]:
    with path.open("r", encoding="utf-8-sig") as handle:
        value = json.load(handle)
    if not isinstance(value, dict):
        raise ValueError(f"Expected a JSON object in {path}")
    return value


def iter_records(catalog: Path) -> Iterable[dict[str, str]]:
    for path in sorted(catalog.glob("*.json")):
        if path.name.startswith("_"):
            continue
        data = load_json(path)
        plugin = path.stem
        for toolset in data.get("toolsets", []):
            toolset_id = str(toolset.get("id", ""))
            yield {
                "kind": "toolset",
                "id": toolset_id,
                "toolset": toolset_id,
                "plugin": plugin,
                "description": str(toolset.get("desc", "")),
                "signature": "",
                "details": "",
            }
            for tool in toolset.get("tools", []):
                tool_id = str(tool.get("id", ""))
                yield {
                    "kind": "tool",
                    "id": f"{toolset_id}.{tool_id}",
                    "toolset": toolset_id,
                    "plugin": plugin,
                    "description": str(tool.get("desc", "")),
                    "signature": str(tool.get("signature", "")),
                    "details": "",
                }
        for skill in data.get("skills", []):
            yield {
                "kind": "skill",
                "id": str(skill.get("id", "")),
                "toolset": "",
                "plugin": plugin,
                "description": str(skill.get("desc", "")),
                "signature": "",
                "details": str(skill.get("instructions", "")),
            }


def score_record(record: dict[str, str], query: str) -> int:
    phrase = query.casefold().strip()
    tokens = [token for token in phrase.split() if token]
    if not tokens:
        return 1

    record_id = record["id"].casefold()
    signature = record["signature"].casefold()
    description = record["description"].casefold()
    details = record["details"].casefold()
    combined = " ".join((record_id, signature, description, details))
    if any(token not in combined for token in tokens):
        return 0

    score = 0
    if phrase == record_id:
        score += 300
    elif phrase in record_id:
        score += 140
    if phrase and phrase in signature:
        score += 60
    if phrase and phrase in description:
        score += 40
    for token in tokens:
        if record_id.startswith(token):
            score += 45
        elif token in record_id:
            score += 30
        if token in signature:
            score += 12
        if token in description:
            score += 8
        if token in details:
            score += 3
    return score


def shorten(value: str, limit: int) -> str:
    compact = " ".join(value.split())
    if len(compact) <= limit:
        return compact
    return compact[: max(0, limit - 3)].rstrip() + "..."


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("query", nargs="*", help="Words that must all match")
    parser.add_argument("--catalog", type=Path, default=DEFAULT_CATALOG)
    parser.add_argument("--kind", choices=("all", "tool", "toolset", "skill"), default="all")
    parser.add_argument("--toolset", help="Exact toolset ID filter")
    parser.add_argument("--plugin", help="Plugin JSON stem filter")
    parser.add_argument("--limit", type=int, default=12)
    parser.add_argument("--min-score", type=int, default=10)
    parser.add_argument("--max-chars", type=int, default=500)
    parser.add_argument(
        "--format",
        choices=("full", "minimal"),
        default="full",
        dest="output_format",
        help="Text output detail; --json always returns complete records",
    )
    parser.add_argument("--json", action="store_true", dest="as_json")
    parser.add_argument("--stats", action="store_true")
    return parser.parse_args(argv)


def format_minimal(record: dict[str, str]) -> str:
    if record["kind"] == "tool":
        return record["signature"] or record["id"]
    return f"{record['kind']} {record['id']}"


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv)
    if not args.catalog.is_dir():
        print(f"Catalog directory not found: {args.catalog}", file=sys.stderr)
        return 2

    try:
        records = list(iter_records(args.catalog))
    except (OSError, ValueError, json.JSONDecodeError) as exc:
        print(f"Catalog read failed: {exc}", file=sys.stderr)
        return 2

    if args.stats:
        counts = {kind: sum(record["kind"] == kind for record in records) for kind in ("toolset", "tool", "skill")}
        counts["plugins"] = len({record["plugin"] for record in records})
        print(json.dumps(counts, ensure_ascii=False, sort_keys=True))
        return 0

    query = " ".join(args.query).strip()
    if not query and not args.toolset and not args.plugin:
        print("Provide a query, --toolset, --plugin, or --stats.", file=sys.stderr)
        return 2

    matches: list[tuple[int, dict[str, str]]] = []
    for record in records:
        if args.kind != "all" and record["kind"] != args.kind:
            continue
        if args.toolset and record["toolset"].casefold() != args.toolset.casefold():
            continue
        if args.plugin and record["plugin"].casefold() != args.plugin.casefold():
            continue
        score = score_record(record, query)
        if score and (not query or score >= args.min_score):
            matches.append((score, record))

    matches.sort(key=lambda item: (-item[0], item[1]["kind"], item[1]["id"].casefold()))
    selected = matches[: max(0, args.limit)]
    if args.as_json:
        payload = [{"score": score, **record} for score, record in selected]
        print(json.dumps(payload, ensure_ascii=False, indent=2))
        return 0

    if args.output_format == "minimal":
        for _, record in selected:
            print(format_minimal(record))
        if not selected:
            print("No matches.")
        return 0

    for score, record in selected:
        print(f"{record['kind']} {record['id']} [{record['plugin']}] score={score}")
        if record["signature"]:
            print(f"  signature: {record['signature']}")
        if record["description"]:
            print(f"  description: {shorten(record['description'], args.max_chars)}")
        if record["details"]:
            print(f"  details: {shorten(record['details'], args.max_chars)}")
    if not selected:
        print("No matches.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
