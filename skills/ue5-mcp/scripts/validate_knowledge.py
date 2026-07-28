#!/usr/bin/env python3
"""Validate the bundled UE5 MCP catalog snapshot."""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path
from typing import Any


CATALOG = Path(__file__).resolve().parent.parent / "references" / "toolsets"
TEST_NAME = re.compile(r"(^|[^a-z])(fake|mock|demo|errorprone)([^a-z]|$)", re.IGNORECASE)


def read(path: Path) -> dict[str, Any]:
    with path.open("r", encoding="utf-8-sig") as handle:
        value = json.load(handle)
    if not isinstance(value, dict):
        raise ValueError(f"Expected object in {path.name}")
    return value


def main() -> int:
    issues: list[str] = []
    index_path = CATALOG / "_index.json"
    if not index_path.is_file():
        print("Missing _index.json", file=sys.stderr)
        return 2

    try:
        index = read(index_path)
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
                    if not tool_id or not str(tool.get("signature", "")).strip() or not str(tool.get("desc", "")).strip():
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

    result = {"ok": not issues, "stats": actual, "issues": issues}
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0 if not issues else 1


if __name__ == "__main__":
    raise SystemExit(main())
