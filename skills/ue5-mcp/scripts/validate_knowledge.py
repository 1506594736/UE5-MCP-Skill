#!/usr/bin/env python3
"""Validate the bundled UE5 MCP catalog snapshot."""

from __future__ import annotations

import argparse
import json
import re
import sys
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import Any, Optional


CATALOG = Path(__file__).resolve().parent.parent / "references" / "toolsets"
TEST_NAME = re.compile(r"(^|[^a-z])(fake|mock|demo|errorprone)([^a-z]|$)", re.IGNORECASE)
ENGINE_VERSION = re.compile(r"^(0|[1-9]\d*)\.(0|[1-9]\d*)(?:\.(0|[1-9]\d*))?$")
FUTURE_TOLERANCE = timedelta(minutes=5)


def read(path: Path) -> dict[str, Any]:
    with path.open("r", encoding="utf-8-sig") as handle:
        value = json.load(handle)
    if not isinstance(value, dict):
        raise ValueError(f"Expected object in {path.name}")
    return value


def non_negative_int(value: str) -> int:
    parsed = int(value)
    if parsed < 0:
        raise argparse.ArgumentTypeError("must be zero or greater")
    return parsed


def engine_version_arg(value: str) -> str:
    try:
        parse_engine_version(value)
    except ValueError as exc:
        raise argparse.ArgumentTypeError(str(exc)) from exc
    return value


def parse_engine_version(value: Any) -> tuple[int, int, int]:
    text = str(value).strip()
    match = ENGINE_VERSION.fullmatch(text)
    if not match:
        raise ValueError(f"invalid engine version: {text or '<empty>'!r}")
    major, minor, patch = match.groups()
    return int(major), int(minor), int(patch or 0)


def parse_generated(value: Any) -> datetime:
    text = str(value).strip()
    if not text:
        raise ValueError("missing generated timestamp")
    try:
        parsed = datetime.fromisoformat(text[:-1] + "+00:00" if text.endswith("Z") else text)
    except ValueError as exc:
        raise ValueError(f"invalid generated timestamp: {text!r}") from exc
    if parsed.tzinfo is None or parsed.utcoffset() is None:
        raise ValueError("generated timestamp must include a timezone")
    return parsed.astimezone(timezone.utc)


def validate_metadata(
    index: dict[str, Any],
    *,
    max_age: Optional[int] = None,
    editor_version: Optional[str] = None,
    now: Optional[datetime] = None,
) -> tuple[dict[str, Any], list[str], list[str]]:
    metadata: dict[str, Any] = {
        "engine": index.get("engine"),
        "generated": index.get("generated"),
    }
    warnings: list[str] = []
    issues: list[str] = []

    try:
        snapshot_version = parse_engine_version(index.get("engine", ""))
    except ValueError as exc:
        issues.append(str(exc))
        snapshot_version = None

    try:
        generated = parse_generated(index.get("generated", ""))
    except ValueError as exc:
        issues.append(str(exc))
        generated = None

    current = now or datetime.now(timezone.utc)
    if current.tzinfo is None or current.utcoffset() is None:
        raise ValueError("current time must include a timezone")
    current = current.astimezone(timezone.utc)

    if generated is not None:
        age = current - generated
        metadata["age_days"] = max(0, age.total_seconds() / 86400)
        if age < -FUTURE_TOLERANCE:
            issues.append(f"generated timestamp is in the future: {index.get('generated')!r}")
        elif max_age is not None and age > timedelta(days=max_age):
            issues.append(f"catalog snapshot is older than {max_age} days")

    if editor_version is not None:
        requested_version = parse_engine_version(editor_version)
        metadata["editor_version"] = editor_version
        if snapshot_version is not None:
            if requested_version[:2] != snapshot_version[:2]:
                issues.append(
                    "engine version mismatch: "
                    f"snapshot {index.get('engine')}, editor {editor_version}"
                )
            elif requested_version[2] != snapshot_version[2]:
                warnings.append(
                    "engine patch version differs: "
                    f"snapshot {index.get('engine')}, editor {editor_version}"
                )

    return metadata, warnings, issues


def parse_args(argv: Optional[list[str]] = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--max-age", type=non_negative_int, metavar="DAYS")
    parser.add_argument("--editor-version", type=engine_version_arg)
    return parser.parse_args(argv)


def main(argv: Optional[list[str]] = None) -> int:
    args = parse_args(argv)
    issues: list[str] = []
    index_path = CATALOG / "_index.json"
    if not index_path.is_file():
        print("Missing _index.json", file=sys.stderr)
        return 2

    try:
        index = read(index_path)
        metadata, warnings, metadata_issues = validate_metadata(
            index,
            max_age=args.max_age,
            editor_version=args.editor_version,
        )
        issues.extend(metadata_issues)
        files = sorted(path for path in CATALOG.glob("*.json") if not path.name.startswith("_"))
        toolsets: set[str] = set()
        tools: set[str] = set()
        skills: set[str] = set()
        tool_count = 0
        skill_count = 0

        for path in files:
            data = read(path)
            for toolset in data.get("toolsets", []):
                toolset_id = str(toolset.get("id", "")).strip()
                if not toolset_id:
                    issues.append(f"{path.name}: empty toolset id")
                    continue
                if toolset_id in toolsets:
                    issues.append(f"duplicate toolset: {toolset_id}")
                toolsets.add(toolset_id)
                if TEST_NAME.search(toolset_id):
                    issues.append(f"test-like toolset remains: {toolset_id}")
                for tool in toolset.get("tools", []):
                    tool_id = str(tool.get("id", "")).strip()
                    key = f"{toolset_id}.{tool_id}"
                    tool_count += 1
                    if (
                        not tool_id
                        or not str(tool.get("signature", "")).strip()
                        or not str(tool.get("desc", "")).strip()
                    ):
                        issues.append(f"{path.name}: incomplete tool {key}")
                    if key in tools:
                        issues.append(f"duplicate tool: {key}")
                    tools.add(key)
            for skill in data.get("skills", []):
                skill_id = str(skill.get("id", "")).strip()
                skill_count += 1
                if not skill_id or not str(skill.get("instructions", "")).strip():
                    issues.append(f"{path.name}: incomplete skill {skill_id or '<empty>'}")
                if skill_id in skills:
                    issues.append(f"duplicate skill: {skill_id}")
                skills.add(skill_id)
    except (OSError, ValueError, json.JSONDecodeError) as exc:
        print(f"Validation failed to read catalog: {exc}", file=sys.stderr)
        return 2

    actual = {"plugins": len(files), "toolsets": len(toolsets), "tools": tool_count, "skills": skill_count}
    expected = index.get("stats", {})
    for key, value in actual.items():
        if expected.get(key) != value:
            issues.append(f"count mismatch for {key}: expected {expected.get(key)!r}, got {value}")

    result = {
        "ok": not issues,
        "metadata": metadata,
        "stats": actual,
        "warnings": warnings,
        "issues": issues,
    }
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0 if not issues else 1


if __name__ == "__main__":
    raise SystemExit(main())
