from __future__ import annotations

import importlib.util
import io
import json
import tempfile
import unittest
from contextlib import redirect_stdout
from pathlib import Path


SCRIPT = (
    Path(__file__).resolve().parents[1]
    / "skills"
    / "ue5-mcp"
    / "scripts"
    / "search_tools.py"
)
SPEC = importlib.util.spec_from_file_location("search_tools", SCRIPT)
if SPEC is None or SPEC.loader is None:
    raise RuntimeError(f"Unable to load {SCRIPT}")
search_tools = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(search_tools)


class SearchToolsOutputTests(unittest.TestCase):
    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory()
        self.catalog = Path(self.temp_dir.name)
        payload = {
            "toolsets": [
                {
                    "id": "BlueprintTools",
                    "desc": "Blueprint editor tools.",
                    "tools": [
                        {
                            "id": "compile_blueprint",
                            "desc": "Compiles the given Blueprint.",
                            "signature": (
                                "BlueprintTools.compile_blueprint"
                                "(unreal.Blueprint, bool) -> None"
                            ),
                        },
                        {
                            "id": "inspect_blueprint",
                            "desc": "Inspects a Blueprint without a signature.",
                            "signature": "",
                        },
                    ],
                }
            ],
            "skills": [
                {
                    "id": "BlueprintWorkflow",
                    "desc": "Blueprint workflow guidance.",
                    "instructions": "Inspect before changing assets.",
                }
            ],
        }
        (self.catalog / "EditorToolset.json").write_text(
            json.dumps(payload), encoding="utf-8"
        )

    def tearDown(self):
        self.temp_dir.cleanup()

    def run_cli(self, *args: str) -> tuple[int, str]:
        output = io.StringIO()
        with redirect_stdout(output):
            result = search_tools.main([*args, "--catalog", str(self.catalog)])
        return result, output.getvalue()

    def test_minimal_tool_output_contains_only_signature(self):
        result, output = self.run_cli(
            "compile", "--kind", "tool", "--format", "minimal"
        )

        self.assertEqual(0, result)
        self.assertEqual(
            "BlueprintTools.compile_blueprint(unreal.Blueprint, bool) -> None\n",
            output,
        )
        self.assertNotIn("description", output)
        self.assertNotIn("score=", output)
        self.assertNotIn("EditorToolset", output)

    def test_minimal_tool_without_signature_falls_back_to_id(self):
        result, output = self.run_cli(
            "inspect", "--kind", "tool", "--format", "minimal"
        )

        self.assertEqual(0, result)
        self.assertEqual("BlueprintTools.inspect_blueprint\n", output)

    def test_minimal_non_tool_output_keeps_kind(self):
        result, output = self.run_cli(
            "workflow", "--kind", "skill", "--format", "minimal"
        )

        self.assertEqual(0, result)
        self.assertEqual("skill BlueprintWorkflow\n", output)

    def test_default_output_remains_full(self):
        result, output = self.run_cli("compile", "--kind", "tool")

        self.assertEqual(0, result)
        self.assertIn("tool BlueprintTools.compile_blueprint", output)
        self.assertIn("[EditorToolset] score=", output)
        self.assertIn("signature:", output)
        self.assertIn("description: Compiles the given Blueprint.", output)

    def test_json_ignores_text_format_and_returns_complete_record(self):
        result, output = self.run_cli(
            "compile", "--kind", "tool", "--format", "minimal", "--json"
        )

        self.assertEqual(0, result)
        record = json.loads(output)[0]
        self.assertEqual("Compiles the given Blueprint.", record["description"])
        self.assertIn("score", record)

    def test_parser_accepts_minimal_format(self):
        args = search_tools.parse_args(["compile", "--format", "minimal"])

        self.assertEqual("minimal", args.output_format)


if __name__ == "__main__":
    unittest.main()
