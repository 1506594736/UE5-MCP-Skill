from __future__ import annotations

import importlib.util
import io
import unittest
from contextlib import redirect_stderr
from datetime import datetime, timezone
from pathlib import Path


SCRIPT = (
    Path(__file__).resolve().parents[1]
    / "skills"
    / "ue5-mcp"
    / "scripts"
    / "validate_knowledge.py"
)
SPEC = importlib.util.spec_from_file_location("validate_knowledge", SCRIPT)
if SPEC is None or SPEC.loader is None:
    raise RuntimeError(f"Unable to load {SCRIPT}")
validate_knowledge = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(validate_knowledge)


class MetadataValidationTests(unittest.TestCase):
    NOW = datetime(2026, 7, 29, tzinfo=timezone.utc)

    def validate(self, index, **kwargs):
        return validate_knowledge.validate_metadata(index, now=self.NOW, **kwargs)

    def test_valid_metadata(self):
        metadata, warnings, issues = self.validate(
            {"engine": "5.8.0", "generated": "2026-07-28T18:42:59Z"},
            max_age=90,
            editor_version="5.8.0",
        )

        self.assertEqual([], warnings)
        self.assertEqual([], issues)
        self.assertEqual("5.8.0", metadata["engine"])
        self.assertGreater(metadata["age_days"], 0)

    def test_missing_metadata_is_rejected(self):
        _, _, issues = self.validate({})

        self.assertIn("invalid engine version: '<empty>'", issues)
        self.assertIn("missing generated timestamp", issues)

    def test_timestamp_requires_timezone(self):
        _, _, issues = self.validate(
            {"engine": "5.8.0", "generated": "2026-07-28T18:42:59"}
        )

        self.assertIn("generated timestamp must include a timezone", issues)

    def test_future_timestamp_is_rejected(self):
        _, _, issues = self.validate(
            {"engine": "5.8.0", "generated": "2026-07-30T00:00:00Z"}
        )

        self.assertTrue(any("in the future" in issue for issue in issues))

    def test_stale_snapshot_is_rejected(self):
        _, _, issues = self.validate(
            {"engine": "5.8.0", "generated": "2026-01-01T00:00:00Z"},
            max_age=90,
        )

        self.assertIn("catalog snapshot is older than 90 days", issues)

    def test_minor_version_mismatch_is_rejected(self):
        _, _, issues = self.validate(
            {"engine": "5.8.0", "generated": "2026-07-28T18:42:59Z"},
            editor_version="5.9.0",
        )

        self.assertIn("engine version mismatch: snapshot 5.8.0, editor 5.9.0", issues)

    def test_patch_version_mismatch_is_a_warning(self):
        _, warnings, issues = self.validate(
            {"engine": "5.8.0", "generated": "2026-07-28T18:42:59Z"},
            editor_version="5.8.1",
        )

        self.assertEqual([], issues)
        self.assertIn("engine patch version differs: snapshot 5.8.0, editor 5.8.1", warnings)

    def test_negative_max_age_is_rejected_by_cli(self):
        with redirect_stderr(io.StringIO()), self.assertRaises(SystemExit):
            validate_knowledge.parse_args(["--max-age", "-1"])

    def test_invalid_editor_version_is_rejected_by_cli(self):
        with redirect_stderr(io.StringIO()), self.assertRaises(SystemExit):
            validate_knowledge.parse_args(["--editor-version", "5.8-preview"])

    def test_truncated_toolset_descriptions_are_detected(self):
        descriptions = (
            "Tools for tracks, sections, and",
            "Tools for bindings. Use",
            "Provides tools, including",
            "Provides the properties of",
        )

        for description in descriptions:
            with self.subTest(description=description):
                self.assertTrue(validate_knowledge.description_looks_truncated(description))

    def test_complete_toolset_descriptions_are_allowed(self):
        descriptions = (
            "Tools for tracks, sections, and bindings.",
            "Tools designed for ease of use.",
            "Provides tools, including actor discovery and placement.",
        )

        for description in descriptions:
            with self.subTest(description=description):
                self.assertFalse(validate_knowledge.description_looks_truncated(description))

    def test_index_toolset_descriptions_are_keyed_by_file_and_id(self):
        descriptions = validate_knowledge.index_toolset_descriptions(
            {
                "plugins": [
                    {
                        "file": "Example.json",
                        "toolsets": [{"id": "ExampleTools", "desc": "Example tools."}],
                    }
                ]
            }
        )

        self.assertEqual(
            "Example tools.",
            descriptions[("Example.json", "ExampleTools")],
        )

    def test_skill_toolset_references_must_resolve_to_exact_ids(self):
        issues = validate_knowledge.validate_skill_toolset_references(
            [("Niagara.json", "NiagaraSkill", "NiagaraToolset_System")],
            {"UNiagaraToolset_System"},
        )

        self.assertEqual(
            [
                "Niagara.json: skill NiagaraSkill references unknown toolset: "
                "NiagaraToolset_System"
            ],
            issues,
        )

    def test_exact_skill_toolset_references_are_allowed(self):
        issues = validate_knowledge.validate_skill_toolset_references(
            [("Niagara.json", "NiagaraSkill", "UNiagaraToolset_System")],
            {"UNiagaraToolset_System"},
        )

        self.assertEqual([], issues)


if __name__ == "__main__":
    unittest.main()
