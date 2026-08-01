"""Tests for the technical-writing CLI."""

from __future__ import annotations

import json
import os
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


SCRIPT = Path(__file__).resolve().parents[1] / "scripts" / "technical-writing"
HEADER = """# Glossary

| Term | Definition | Avoid | Status | Evidence |
|---|---|---|---|---|
"""


class TechnicalWritingCliTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temporary = tempfile.TemporaryDirectory()
        self.addCleanup(self.temporary.cleanup)
        self.root = Path(self.temporary.name)
        self.home = self.root / "home"
        self.home.mkdir()
        self.project = self.root / "project"
        self.project.mkdir()

    def run_cli(
        self,
        *arguments: str,
        input_text: str | None = None,
        cwd: Path | None = None,
    ) -> subprocess.CompletedProcess[str]:
        environment = os.environ.copy()
        environment["HOME"] = str(self.home)
        environment.pop("AGENTSTATION_TECHNICAL_WRITING_CONFIG", None)
        return subprocess.run(
            [sys.executable, str(SCRIPT), *arguments],
            cwd=cwd or self.project,
            env=environment,
            input=input_text,
            text=True,
            capture_output=True,
            check=False,
        )

    def write_project_config(self, body: str) -> Path:
        path = self.project / ".agents" / "technical-writing.toml"
        path.parent.mkdir()
        path.write_text(body, encoding="utf-8")
        return path

    def write_glossary(self, rows: str = "") -> Path:
        path = self.project / "GLOSSARY.md"
        path.write_text(HEADER + rows, encoding="utf-8")
        return path

    def test_lint_reads_stdin_and_returns_json(self) -> None:
        result = self.run_cli(
            "lint",
            "-",
            "--format",
            "json",
            input_text="The parser reads the file.",
        )
        self.assertEqual(result.returncode, 0, result.stderr)
        payload = json.loads(result.stdout)
        self.assertTrue(payload["passed"])
        self.assertEqual(payload["mode"], "developer")
        self.assertEqual(payload["documents"][0]["path"], "<stdin>")
        self.assertEqual(payload["summary"]["files"], 1)

    def test_lint_strips_fenced_and_inline_code(self) -> None:
        text = """Use the command below.

```text
robust; leverage; it is being changed
```

Run `leverage;` now.
"""
        result = self.run_cli("lint", "-", "--format", "json", input_text=text)
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        payload = json.loads(result.stdout)
        self.assertEqual(payload["summary"]["diagnostics"], 0)

    def test_contraction_rule_does_not_report_possessives(self) -> None:
        result = self.run_cli(
            "lint",
            "-",
            "--format",
            "json",
            input_text=(
                "AgentStation's linter checks the project's glossary. "
                "The skill provides one command."
            ),
        )
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertEqual(json.loads(result.stdout)["summary"]["diagnostics"], 0)

    def test_contraction_rule_reports_a_typographic_apostrophe(self) -> None:
        result = self.run_cli(
            "lint",
            "-",
            "--format",
            "json",
            input_text="We can’t continue.",
        )
        diagnostics = json.loads(result.stdout)["documents"][0]["diagnostics"]
        self.assertEqual([item["rule"] for item in diagnostics], ["contraction"])

    def test_lint_reports_each_required_surface_rule(self) -> None:
        self.write_project_config(
            """
[limits]
descriptive_words = 8
paragraph_sentences = 2
max_warnings_per_100_words = 1000
"""
        )
        text = (
            "We can't leverage a robust tool; it is being improved — reach out "
            "because this sentence contains more than eight words. "
            "It is important to note that we perform an analysis of logs. "
            "The result was written. We have completed the work."
        )
        result = self.run_cli("lint", "-", "--format", "json", input_text=text)
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        rules = {
            item["rule"]
            for item in json.loads(result.stdout)["documents"][0]["diagnostics"]
        }
        self.assertEqual(
            rules,
            {
                "banned_word",
                "contraction",
                "complex_verb",
                "em_dash",
                "ing_main_verb",
                "long_paragraph",
                "long_sentence",
                "marketing_adjective",
                "modal_hedge",
                "nominalization",
                "passive_voice",
                "phrasal_verb",
                "semicolon",
            },
        )

    def test_complex_verb_reports_perfect_tenses(self) -> None:
        result = self.run_cli(
            "lint",
            "-",
            "--format",
            "json",
            "--mode",
            "strict",
            input_text=("We have received the report. The agent had written the file."),
        )
        diagnostics = json.loads(result.stdout)["documents"][0]["diagnostics"]
        self.assertEqual(
            [item["rule"] for item in diagnostics],
            ["complex_verb", "complex_verb"],
        )

    def test_complex_verb_allows_have_as_a_simple_verb(self) -> None:
        result = self.run_cli(
            "lint",
            "-",
            "--format",
            "json",
            "--mode",
            "strict",
            input_text="We have three files. The agent has a lock.",
        )
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertEqual(json.loads(result.stdout)["summary"]["diagnostics"], 0)

    def test_complex_verb_allows_adjectives_after_have(self) -> None:
        result = self.run_cli(
            "lint",
            "-",
            "--format",
            "json",
            "--mode",
            "strict",
            input_text="We have green status lights. The project has open issues.",
        )
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertEqual(json.loads(result.stdout)["summary"]["diagnostics"], 0)

    def test_developer_allows_configured_warning_rate_but_strict_promotes(self) -> None:
        self.write_project_config(
            """
[limits]
max_warnings_per_100_words = 100
"""
        )
        developer = self.run_cli(
            "lint", "-", "--format", "json", input_text="Read this; then stop."
        )
        strict = self.run_cli(
            "lint",
            "-",
            "--format",
            "json",
            "--mode",
            "strict",
            input_text="Read this; then stop.",
        )
        self.assertEqual(developer.returncode, 0, developer.stdout)
        self.assertEqual(
            json.loads(developer.stdout)["documents"][0]["diagnostics"][0]["severity"],
            "warning",
        )
        self.assertEqual(strict.returncode, 1, strict.stdout)
        self.assertEqual(
            json.loads(strict.stdout)["documents"][0]["diagnostics"][0]["severity"],
            "error",
        )

    def test_short_developer_reply_uses_a_100_word_warning_floor(self) -> None:
        result = self.run_cli(
            "lint",
            "-",
            "--format",
            "json",
            input_text="The tests are running.",
        )
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        payload = json.loads(result.stdout)
        self.assertEqual(payload["summary"]["warnings"], 1)
        self.assertEqual(payload["summary"]["warning_rate_per_100_words"], 1)

    def test_passive_heuristic_does_not_treat_red_as_a_participle(self) -> None:
        result = self.run_cli(
            "lint",
            "-",
            "--format",
            "json",
            "--mode",
            "strict",
            input_text="If the status light is red, disconnect power.",
        )
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertEqual(json.loads(result.stdout)["summary"]["diagnostics"], 0)

    def test_ing_heuristic_ignores_indefinite_pronouns(self) -> None:
        result = self.run_cli(
            "lint",
            "-",
            "--format",
            "json",
            "--mode",
            "strict",
            input_text=(
                "There is nothing left. This is something the caller supplies. "
                "The result is anything other than 200."
            ),
        )
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertEqual(json.loads(result.stdout)["summary"]["diagnostics"], 0)

    def test_modal_phrase_produces_one_diagnostic(self) -> None:
        result = self.run_cli(
            "lint",
            "-",
            "--format",
            "json",
            input_text="It is important to note the result.",
        )
        diagnostics = json.loads(result.stdout)["documents"][0]["diagnostics"]
        self.assertEqual([item["rule"] for item in diagnostics], ["modal_hedge"])

    def test_configurable_instruction_and_descriptive_limits(self) -> None:
        self.write_project_config(
            """
[limits]
instruction_words = 3
descriptive_words = 10
max_warnings_per_100_words = 100

[rules]
long_sentence = "error"
"""
        )
        result = self.run_cli(
            "lint",
            "-",
            "--format",
            "json",
            input_text="1. Read the complete configuration file.",
        )
        self.assertEqual(result.returncode, 1)
        diagnostics = json.loads(result.stdout)["documents"][0]["diagnostics"]
        self.assertEqual([item["rule"] for item in diagnostics], ["long_sentence"])
        self.assertIn("sentence has 5 words", diagnostics[0]["message"])
        self.assertIn("limit is 3", diagnostics[0]["message"])

    def test_numbered_list_marker_does_not_consume_instruction_budget(self) -> None:
        self.write_project_config(
            """
[limits]
instruction_words = 5
descriptive_words = 50
max_warnings_per_100_words = 100

[rules]
long_sentence = "error"
"""
        )
        result = self.run_cli(
            "lint",
            "-",
            "--format",
            "json",
            input_text="1. Read the complete configuration file.",
        )
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertEqual(json.loads(result.stdout)["summary"]["diagnostics"], 0)

    def test_each_sentence_in_list_item_uses_instruction_limit(self) -> None:
        self.write_project_config(
            """
[limits]
instruction_words = 5
descriptive_words = 50
max_warnings_per_100_words = 100

[rules]
long_sentence = "error"
"""
        )
        result = self.run_cli(
            "lint",
            "-",
            "--format",
            "json",
            input_text=(
                "1. Read the file. Verify the complete configuration before continuing."
            ),
        )
        self.assertEqual(result.returncode, 1, result.stdout + result.stderr)
        diagnostics = json.loads(result.stdout)["documents"][0]["diagnostics"]
        self.assertEqual([item["rule"] for item in diagnostics], ["long_sentence"])
        self.assertIn("sentence has 6 words", diagnostics[0]["message"])
        self.assertIn("limit is 5", diagnostics[0]["message"])

    def test_wrapped_list_item_uses_the_instruction_limit(self) -> None:
        self.write_project_config(
            """
[limits]
instruction_words = 5
descriptive_words = 50
max_warnings_per_100_words = 100

[rules]
long_sentence = "error"
"""
        )
        result = self.run_cli(
            "lint",
            "-",
            "--format",
            "json",
            input_text=(
                "1. Read the complete configuration\n   before you run the command.\n"
            ),
        )
        self.assertEqual(result.returncode, 1)
        diagnostic = json.loads(result.stdout)["documents"][0]["diagnostics"][0]
        self.assertEqual(diagnostic["rule"], "long_sentence")
        self.assertIn("limit is 5", diagnostic["message"])

    def test_explicit_config_replaces_project_discovery(self) -> None:
        user_config = self.home / ".config" / "agentstation" / "technical-writing.toml"
        user_config.parent.mkdir(parents=True)
        user_config.write_text('[rules]\nsemicolon = "off"\n', encoding="utf-8")
        self.write_project_config('[terms]\nadditional_banned = ["widget"]\n')
        explicit = self.root / "override.toml"
        explicit.write_text(
            '[rules]\nbanned_word = "error"\n[terms]\nadditional_banned = ["gadget"]\n',
            encoding="utf-8",
        )

        result = self.run_cli(
            "lint",
            "-",
            "--format",
            "json",
            "--config",
            str(explicit),
            input_text="Use the widget and gadget;",
        )
        self.assertEqual(result.returncode, 1, result.stdout + result.stderr)
        payload = json.loads(result.stdout)
        self.assertEqual(len(payload["config_sources"]), 2)
        diagnostics = payload["documents"][0]["diagnostics"]
        self.assertEqual([item["rule"] for item in diagnostics], ["banned_word"])
        self.assertEqual(diagnostics[0]["severity"], "error")
        self.assertIn("gadget", diagnostics[0]["message"])

    def test_external_config_keeps_glossary_resolution_in_the_project(self) -> None:
        self.write_glossary(
            "| worker | A process. | daemon | Approved | src/worker.py |\n"
        )
        explicit = self.root / "override.toml"
        explicit.write_text('[rules]\nsemicolon = "off"\n', encoding="utf-8")
        result = self.run_cli(
            "lint",
            "-",
            "--format",
            "json",
            "--config",
            str(explicit),
            input_text="Start the daemon.",
        )
        self.assertEqual(result.returncode, 1, result.stdout + result.stderr)
        payload = json.loads(result.stdout)
        self.assertEqual(payload["config_sources"], [str(explicit.resolve())])
        self.assertEqual(
            payload["documents"][0]["diagnostics"][0]["rule"],
            "glossary_term",
        )

    def test_repository_root_resolves_the_glossary_from_a_subdirectory(self) -> None:
        (self.project / ".git").mkdir()
        self.write_glossary(
            "| worker | A process. | daemon | Approved | src/worker.py |\n"
        )
        docs = self.project / "docs"
        docs.mkdir()
        result = self.run_cli(
            "lint",
            "-",
            "--format",
            "json",
            cwd=docs,
            input_text="Start the daemon.",
        )
        self.assertEqual(result.returncode, 1, result.stdout + result.stderr)
        diagnostic = json.loads(result.stdout)["documents"][0]["diagnostics"][0]
        self.assertEqual(diagnostic["rule"], "glossary_term")

    def test_configured_glossary_cannot_escape_the_project_root(self) -> None:
        self.write_project_config('[glossary]\npath = "../outside.md"\n')
        result = self.run_cli("glossary", "check")
        self.assertEqual(result.returncode, 2)
        self.assertIn("must stay inside the project root", result.stderr)

    def test_missing_explicit_glossary_is_an_input_error(self) -> None:
        missing = self.project / "missing-glossary.md"
        result = self.run_cli(
            "lint",
            "-",
            "--glossary",
            str(missing),
            input_text="The parser reads the file.",
        )
        self.assertEqual(result.returncode, 2)
        self.assertIn("explicit glossary does not exist", result.stderr)

    def test_missing_required_glossary_is_an_input_error(self) -> None:
        self.write_project_config(
            """
[glossary]
path = "missing-glossary.md"
required = true
"""
        )
        result = self.run_cli(
            "lint",
            "-",
            input_text="The parser reads the file.",
        )
        self.assertEqual(result.returncode, 2)
        self.assertIn("required glossary does not exist", result.stderr)

    def test_multiple_paths_and_glob_are_deduplicated(self) -> None:
        docs = self.project / "docs"
        docs.mkdir()
        (docs / "one.md").write_text("The parser reads one file.\n", encoding="utf-8")
        (docs / "two.md").write_text("The parser reads two files.\n", encoding="utf-8")
        result = self.run_cli(
            "lint",
            "docs/*.md",
            "docs/one.md",
            "--format",
            "json",
        )
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(json.loads(result.stdout)["summary"]["files"], 2)

    def test_multi_file_lint_fails_when_one_document_fails(self) -> None:
        docs = self.project / "docs"
        docs.mkdir()
        (docs / "short.md").write_text(
            "The tests are running. The builds are running.\n",
            encoding="utf-8",
        )
        (docs / "long.md").write_text(
            "\n\n".join("The parser reads the file." for _ in range(100)) + "\n",
            encoding="utf-8",
        )
        result = self.run_cli("lint", "docs", "--format", "json")
        self.assertEqual(result.returncode, 1, result.stdout + result.stderr)
        payload = json.loads(result.stdout)
        by_name = {
            Path(document["path"]).name: document for document in payload["documents"]
        }
        self.assertFalse(payload["passed"])
        self.assertTrue(by_name["long.md"]["passed"])
        self.assertFalse(by_name["short.md"]["passed"])

    def test_directory_lint_uses_markdown_structure_and_skips_executables(
        self,
    ) -> None:
        docs = self.project / "docs"
        docs.mkdir()
        (docs / "guide.md").write_text(
            """# Procedure

1. Read the configuration.
2. Run the test.

- The command reads one file.
- The result includes one record.
""",
            encoding="utf-8",
        )
        executable = docs / "helper"
        executable.write_text(
            "robust; leverage; this is not a prose artifact\n", encoding="utf-8"
        )
        (docs / "worker.py").write_text(
            'VALUE = "robust; leverage; intricate"\n# The parser reads one file.\n',
            encoding="utf-8",
        )
        result = self.run_cli("lint", "docs", "--format", "json")
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        payload = json.loads(result.stdout)
        self.assertEqual(payload["summary"]["files"], 2)
        self.assertEqual(payload["summary"]["diagnostics"], 0)

    def test_python_lint_extracts_comments_and_docstrings_only(self) -> None:
        self.write_project_config("[limits]\nmax_warnings_per_100_words = 100\n")
        source = self.project / "worker.py"
        source.write_text(
            '"""This module showcases the parser."""\n'
            'VALUE = "The vibrant tapestry delves into a realm."\n'
            "# The intricate parser reads input.\n"
            "def parse():\n"
            '    """The helper is transformative."""\n'
            '    return "showcase"\n',
            encoding="utf-8",
        )
        result = self.run_cli("lint", str(source), "--format", "json")
        diagnostics = json.loads(result.stdout)["documents"][0]["diagnostics"]
        self.assertEqual(
            [item["rule"] for item in diagnostics],
            ["restricted_vocabulary"] * 3,
        )
        self.assertEqual([item["line"] for item in diagnostics], [1, 3, 5])

    def test_c_like_lint_extracts_line_and_block_comments_only(self) -> None:
        self.write_project_config("[limits]\nmax_warnings_per_100_words = 100\n")
        source = self.project / "worker.ts"
        source.write_text(
            'const value = "The vibrant tapestry.";\n'
            "// The intricate parser reads input.\n"
            "/**\n"
            " * The module showcases results.\n"
            " */\n"
            'const url = "https://example.com/path";\n',
            encoding="utf-8",
        )
        result = self.run_cli("lint", str(source), "--format", "json")
        diagnostics = json.loads(result.stdout)["documents"][0]["diagnostics"]
        self.assertEqual(
            [item["rule"] for item in diagnostics],
            ["restricted_vocabulary", "restricted_vocabulary"],
        )
        self.assertEqual([item["line"] for item in diagnostics], [2, 4])

    def test_rust_lifetimes_and_php_hash_comments_use_comment_parsers(self) -> None:
        self.write_project_config("[limits]\nmax_warnings_per_100_words = 100\n")
        rust = self.project / "worker.rs"
        rust.write_text(
            "fn borrow<'a>(value: &'a str) -> &'a str {\n"
            "    // The intricate helper returns the input.\n"
            "    value\n"
            "}\n",
            encoding="utf-8",
        )
        php = self.project / "worker.php"
        php.write_text(
            '<?php $value = "intricate";\n# The helper showcases the result.\n',
            encoding="utf-8",
        )
        rust_result = self.run_cli("lint", str(rust), "--format", "json")
        php_result = self.run_cli("lint", str(php), "--format", "json")
        rust_diagnostics = json.loads(rust_result.stdout)["documents"][0]["diagnostics"]
        php_diagnostics = json.loads(php_result.stdout)["documents"][0]["diagnostics"]
        self.assertEqual(
            [item["rule"] for item in rust_diagnostics],
            ["restricted_vocabulary"],
        )
        self.assertEqual(
            [item["rule"] for item in php_diagnostics],
            ["restricted_vocabulary"],
        )

    def test_structured_source_lints_comments_not_values(self) -> None:
        self.write_project_config("[limits]\nmax_warnings_per_100_words = 100\n")
        source = self.project / "settings.toml"
        source.write_text(
            'description = "A vibrant tapestry"\n'
            "# The intricate option controls retries.\n",
            encoding="utf-8",
        )
        result = self.run_cli("lint", str(source), "--format", "json")
        diagnostics = json.loads(result.stdout)["documents"][0]["diagnostics"]
        self.assertEqual(
            [item["rule"] for item in diagnostics], ["restricted_vocabulary"]
        )
        self.assertEqual(diagnostics[0]["line"], 2)

    def test_html_lint_extracts_visible_text_and_comments(self) -> None:
        self.write_project_config("[limits]\nmax_warnings_per_100_words = 100\n")
        source = self.project / "guide.html"
        source.write_text(
            '<p class="intricate">The intricate guide reads input.</p>\n'
            "<code>The vibrant tapestry</code>\n"
            '<script>const value = "transformative";</script>\n'
            "<!-- The note showcases the result. -->\n",
            encoding="utf-8",
        )
        result = self.run_cli("lint", str(source), "--format", "json")
        diagnostics = json.loads(result.stdout)["documents"][0]["diagnostics"]
        self.assertEqual(
            [item["rule"] for item in diagnostics],
            ["restricted_vocabulary", "restricted_vocabulary"],
        )
        self.assertEqual([item["line"] for item in diagnostics], [1, 4])

    def test_unsupported_source_is_not_linted_as_plain_prose(self) -> None:
        source = self.project / "data.json"
        source.write_text('{"description":"intricate"}\n', encoding="utf-8")
        result = self.run_cli("lint", str(source), "--format", "json")
        self.assertEqual(result.returncode, 2)
        self.assertIn("no comment-aware prose parser", result.stderr)

    def test_markdown_structured_data_logs_and_identifiers_are_protected(self) -> None:
        self.write_project_config("[limits]\nmax_warnings_per_100_words = 100\n")
        text = """---
description: intricate tapestry
---

| Field | Value |
|---|---|
| mode | transformative |

2026-07-31T12:00:00Z INFO delve into the request

$ delve --intricate

Read tapestry.value. The intricate prose remains.
"""
        result = self.run_cli("lint", "-", "--format", "json", input_text=text)
        diagnostics = json.loads(result.stdout)["documents"][0]["diagnostics"]
        self.assertEqual(
            [item["rule"] for item in diagnostics], ["restricted_vocabulary"]
        )
        self.assertIn("intricate", diagnostics[0]["message"])

    def test_missing_input_and_invalid_config_exit_two(self) -> None:
        missing = self.run_cli("lint", "missing.md")
        self.assertEqual(missing.returncode, 2)
        self.assertIn("input does not exist", missing.stderr)

        config = self.root / "bad.toml"
        config.write_text("version = 2\n", encoding="utf-8")
        invalid = self.run_cli("lint", "-", "--config", str(config), input_text="Text.")
        self.assertEqual(invalid.returncode, 2)
        self.assertIn("version must be 1", invalid.stderr)

    def test_glossary_check_accepts_valid_rows(self) -> None:
        self.write_glossary(
            "| worker | A process that handles a request. | daemon | Approved | src/worker.py |\n"
        )
        result = self.run_cli("glossary", "check")
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertIn("PASS", result.stdout)

    def test_glossary_check_detects_alias_conflicts(self) -> None:
        self.write_glossary(
            "| worker | A process. | daemon | Approved | src/a.py |\n"
            "| daemon | A background process. | service | Approved | src/b.py |\n"
        )
        result = self.run_cli("glossary", "check", "--format", "json")
        self.assertEqual(result.returncode, 1)
        payload = json.loads(result.stdout)
        self.assertFalse(payload["passed"])
        self.assertTrue(
            any("conflicts" in message for message in payload["errors"]),
            payload["errors"],
        )

    def test_case_only_alias_enforces_the_approved_capitalization(self) -> None:
        self.write_glossary(
            "| JavaScript | The programming language. | Javascript | Approved | src/app.js |\n"
        )
        check = self.run_cli("glossary", "check")
        self.assertEqual(check.returncode, 0, check.stdout + check.stderr)

        approved = self.run_cli(
            "lint", "-", "--format", "json", input_text="Use JavaScript."
        )
        avoided = self.run_cli(
            "lint", "-", "--format", "json", input_text="Use Javascript."
        )
        self.assertEqual(approved.returncode, 0, approved.stdout + approved.stderr)
        self.assertEqual(avoided.returncode, 1, avoided.stdout + avoided.stderr)
        diagnostic = json.loads(avoided.stdout)["documents"][0]["diagnostics"][0]
        self.assertEqual(diagnostic["rule"], "glossary_term")

    def test_glossary_alias_does_not_match_inside_hyphenated_compound(self) -> None:
        self.write_glossary(
            "| repository | A version-controlled tree. | repo | "
            "Approved | README.md |\n"
        )
        result = self.run_cli(
            "lint",
            "-",
            "--format",
            "json",
            input_text="The mono-repo contains the package.",
        )
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertEqual(json.loads(result.stdout)["summary"]["diagnostics"], 0)

    def test_glossary_check_rejects_unknown_status(self) -> None:
        self.write_glossary("| worker | A process. | | Maybe | src/worker.py |\n")
        result = self.run_cli("glossary", "check", "--format", "json")
        self.assertEqual(result.returncode, 1)
        self.assertTrue(
            any(
                "status must be" in message
                for message in json.loads(result.stdout)["errors"]
            )
        )

    def test_approved_definition_requirement_is_configurable(self) -> None:
        self.write_glossary(
            "| worker | TODO: Define worker. | daemon | Approved | src/a.py |\n"
        )
        failed = self.run_cli("glossary", "check")
        self.assertEqual(failed.returncode, 1)
        self.write_project_config("[glossary]\nrequire_approved_definitions = false\n")
        passed = self.run_cli("glossary", "check")
        self.assertEqual(passed.returncode, 0, passed.stdout + passed.stderr)

    def test_approved_avoid_term_is_a_lint_error(self) -> None:
        self.write_glossary(
            "| worker | A process that handles a request. | daemon | Approved | src/a.py |\n"
        )
        result = self.run_cli(
            "lint", "-", "--format", "json", input_text="Start the daemon."
        )
        self.assertEqual(result.returncode, 1)
        diagnostics = json.loads(result.stdout)["documents"][0]["diagnostics"]
        self.assertEqual(diagnostics[0]["rule"], "glossary_term")
        self.assertIn("'worker'", diagnostics[0]["message"])

    def test_deprecated_glossary_term_is_a_lint_error(self) -> None:
        self.write_glossary(
            "| daemon | A deprecated name for worker. | | Deprecated | src/a.py |\n"
        )
        result = self.run_cli(
            "lint", "-", "--format", "json", input_text="Start the daemon."
        )
        self.assertEqual(result.returncode, 1)
        diagnostic = json.loads(result.stdout)["documents"][0]["diagnostics"][0]
        self.assertEqual(diagnostic["rule"], "glossary_term")
        self.assertIn("deprecated", diagnostic["message"])

    def test_lint_does_not_enforce_aliases_inside_the_glossary(self) -> None:
        glossary = self.write_glossary(
            "| worker | A process. | daemon | Approved | src/a.py |\n"
        )
        result = self.run_cli("lint", str(glossary), "--format", "json")
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        diagnostics = json.loads(result.stdout)["documents"][0]["diagnostics"]
        self.assertFalse(any(item["rule"] == "glossary_term" for item in diagnostics))

    def test_glossary_init_creates_drafts_and_never_overwrites(self) -> None:
        (self.project / "README.md").write_text(
            "NimbusClient creates a NimbusClient.\n", encoding="utf-8"
        )
        created = self.run_cli("glossary", "init")
        self.assertEqual(created.returncode, 0, created.stdout + created.stderr)
        glossary = self.project / "GLOSSARY.md"
        content = glossary.read_text(encoding="utf-8")
        self.assertIn("| NimbusClient |", content)
        self.assertIn("| Draft |", content)

        second = self.run_cli("glossary", "init")
        self.assertEqual(second.returncode, 2)
        self.assertEqual(glossary.read_text(encoding="utf-8"), content)

    def test_glossary_update_check_write_and_idempotence(self) -> None:
        glossary = self.write_glossary(
            "| API | An application programming interface. | | Approved | README.md |\n"
        )
        with glossary.open("a", encoding="utf-8") as handle:
            handle.write("\n## Review notes\n\nKeep this section unchanged.\n")
        (self.project / "README.md").write_text(
            "NimbusClient calls NimbusClient through the API.\n", encoding="utf-8"
        )
        check = self.run_cli("glossary", "update", "--check")
        self.assertEqual(check.returncode, 1)
        self.assertIn("missing: NimbusClient", check.stdout)

        before = (self.project / "GLOSSARY.md").read_text(encoding="utf-8")
        write = self.run_cli("glossary", "update", "--write")
        self.assertEqual(write.returncode, 0, write.stdout + write.stderr)
        after = (self.project / "GLOSSARY.md").read_text(encoding="utf-8")
        self.assertIn(
            "| API | An application programming interface. | | Approved | README.md |",
            after,
        )
        self.assertIn("## Review notes", before)
        self.assertEqual(after.count("| NimbusClient |"), 1)
        self.assertTrue(after.endswith("Keep this section unchanged.\n"))
        self.assertLess(after.index("| NimbusClient |"), after.index("## Review notes"))

        again = self.run_cli("glossary", "update", "--write")
        self.assertEqual(again.returncode, 0, again.stdout + again.stderr)
        self.assertEqual(
            (self.project / "GLOSSARY.md").read_text(encoding="utf-8"), after
        )
        final_check = self.run_cli("glossary", "update", "--check")
        self.assertEqual(final_check.returncode, 0, final_check.stdout)

    def test_candidate_scan_honors_minimum_occurrences_and_excludes(self) -> None:
        self.write_project_config(
            """
[glossary]
candidate_min_occurrences = 3
scan = ["docs"]
exclude = ["ignored.md"]
"""
        )
        docs = self.project / "docs"
        docs.mkdir()
        (docs / "terms.md").write_text(
            "AlphaClient AlphaClient. BetaClient.\n", encoding="utf-8"
        )
        (docs / "ignored.md").write_text(
            "HiddenClient HiddenClient HiddenClient.\n", encoding="utf-8"
        )
        result = self.run_cli("glossary", "init")
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        content = (self.project / "GLOSSARY.md").read_text(encoding="utf-8")
        self.assertNotIn("AlphaClient", content)
        self.assertNotIn("BetaClient", content)
        self.assertNotIn("HiddenClient", content)

    def test_candidate_scan_excludes_nested_vendor_directories(self) -> None:
        self.write_project_config(
            """
[glossary]
candidate_min_occurrences = 2
scan = ["packages"]
exclude = ["node_modules"]
"""
        )
        source = self.project / "packages" / "app"
        vendor = source / "node_modules" / "dependency"
        vendor.mkdir(parents=True)
        (source / "README.md").write_text(
            "VisibleClient VisibleClient.\n", encoding="utf-8"
        )
        (vendor / "README.md").write_text(
            "HiddenClient HiddenClient.\n", encoding="utf-8"
        )
        result = self.run_cli("glossary", "init")
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        content = (self.project / "GLOSSARY.md").read_text(encoding="utf-8")
        self.assertIn("VisibleClient", content)
        self.assertNotIn("HiddenClient", content)

    def test_candidate_scan_extracts_supported_term_shapes_and_package_names(
        self,
    ) -> None:
        self.write_project_config(
            """
[glossary]
candidate_min_occurrences = 2
scan = ["README.md", "package.json"]
"""
        )
        (self.project / "package.json").write_text(
            '{"name":"nimbus-kit","dependencies":{"@scope/cloud-sdk":"1.0.0"}}\n',
            encoding="utf-8",
        )
        (self.project / "README.md").write_text(
            "NimbusClient NimbusClient SDK SDK `cache_key` `cache_key` "
            "`cloud-worker` `cloud-worker` nimbus-kit @scope/cloud-sdk\n",
            encoding="utf-8",
        )
        result = self.run_cli("glossary", "init")
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        content = (self.project / "GLOSSARY.md").read_text(encoding="utf-8")
        for term in (
            "NimbusClient",
            "SDK",
            "cache_key",
            "cloud-worker",
            "nimbus-kit",
            "@scope/cloud-sdk",
        ):
            self.assertIn(f"| {term} |", content)

    def test_candidate_scan_skips_internal_source_identifiers(self) -> None:
        self.write_project_config(
            """
[glossary]
candidate_min_occurrences = 2
scan = ["src"]
"""
        )
        source = self.project / "src"
        source.mkdir()
        (source / "worker.py").write_text(
            """
class PublicClient:
    pass

internal_value = 1
internal_value = 2
""",
            encoding="utf-8",
        )
        result = self.run_cli("glossary", "init")
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        content = (self.project / "GLOSSARY.md").read_text(encoding="utf-8")
        self.assertNotIn("internal_value", content)

    def test_candidate_scan_honors_ignored_candidates(self) -> None:
        self.write_project_config(
            """
[glossary]
candidate_min_occurrences = 2
scan = ["README.md"]
ignored_candidates = ["HiddenClient"]
"""
        )
        (self.project / "README.md").write_text(
            "HiddenClient HiddenClient. VisibleClient VisibleClient.\n",
            encoding="utf-8",
        )
        result = self.run_cli("glossary", "init")
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        content = (self.project / "GLOSSARY.md").read_text(encoding="utf-8")
        self.assertNotIn("HiddenClient", content)
        self.assertIn("VisibleClient", content)

    def test_candidate_scan_does_not_count_terms_inside_hyphenated_compounds(
        self,
    ) -> None:
        self.write_project_config(
            """
[glossary]
candidate_min_occurrences = 2
scan = ["README.md"]
"""
        )
        (self.project / "README.md").write_text(
            "NimbusClient-alpha NimbusClient-beta.\n",
            encoding="utf-8",
        )
        result = self.run_cli("glossary", "init")
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        content = (self.project / "GLOSSARY.md").read_text(encoding="utf-8")
        self.assertNotIn("| NimbusClient |", content)

    def test_rule_can_be_disabled_and_allowed_term_suppresses_word_rule(self) -> None:
        self.write_project_config(
            """
[rules]
semicolon = "off"

[terms]
allowed = ["robust"]
"""
        )
        result = self.run_cli(
            "lint", "-", "--format", "json", input_text="A robust parser; reads text."
        )
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertEqual(json.loads(result.stdout)["summary"]["diagnostics"], 0)

    def test_allowed_term_does_not_suppress_unlisted_inflections(self) -> None:
        self.write_project_config(
            """
[terms]
allowed = ["ensure"]
"""
        )
        result = self.run_cli(
            "lint",
            "-",
            "--format",
            "json",
            input_text="The parser ensures consistent output.",
        )
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        diagnostics = json.loads(result.stdout)["documents"][0]["diagnostics"]
        self.assertEqual([item["rule"] for item in diagnostics], ["banned_word"])
        self.assertIn("'ensures'", diagnostics[0]["message"])

    def test_formulaic_phrase_reports_stock_framing(self) -> None:
        result = self.run_cli(
            "lint",
            "-",
            "--format",
            "json",
            input_text="The change marks a significant step forward for the parser.",
        )
        diagnostics = json.loads(result.stdout)["documents"][0]["diagnostics"]
        self.assertEqual([item["rule"] for item in diagnostics], ["formulaic_phrase"])
        self.assertIn("specific fact", diagnostics[0]["message"])

    def test_allowed_phrase_suppresses_an_exact_formulaic_exception(self) -> None:
        self.write_project_config('[terms]\nallowed = ["a significant step forward"]\n')
        result = self.run_cli(
            "lint",
            "-",
            "--format",
            "json",
            input_text="The change marks a significant step forward for the parser.",
        )
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertEqual(json.loads(result.stdout)["summary"]["diagnostics"], 0)

    def test_formulaic_phrase_reports_each_occurrence_without_word_duplication(
        self,
    ) -> None:
        self.write_project_config("[limits]\nmax_warnings_per_100_words = 100\n")
        result = self.run_cli(
            "lint",
            "-",
            "--format",
            "json",
            input_text="We delve into logs. We delve into traces.",
        )
        diagnostics = json.loads(result.stdout)["documents"][0]["diagnostics"]
        self.assertEqual(
            [item["rule"] for item in diagnostics],
            ["formulaic_phrase", "formulaic_phrase"],
        )

    def test_assistant_scaffold_reports_preamble_and_closing(self) -> None:
        self.write_project_config("[limits]\nmax_warnings_per_100_words = 100\n")
        result = self.run_cli(
            "lint",
            "-",
            "--format",
            "json",
            input_text="Certainly, here is the result. Hope this helps.",
        )
        diagnostics = json.loads(result.stdout)["documents"][0]["diagnostics"]
        self.assertEqual(
            [item["rule"] for item in diagnostics],
            ["assistant_scaffold", "assistant_scaffold"],
        )

    def test_negative_parallelism_reports_selected_rhetorical_forms(self) -> None:
        self.write_project_config("[limits]\nmax_warnings_per_100_words = 100\n")
        result = self.run_cli(
            "lint",
            "-",
            "--format",
            "json",
            input_text=(
                "The patch is not just smaller, but also clearer. "
                "It is not a cache. It is a lookup table. "
                "No setup, no waiting, just results."
            ),
        )
        diagnostics = json.loads(result.stdout)["documents"][0]["diagnostics"]
        self.assertEqual(
            [item["rule"] for item in diagnostics],
            [
                "negative_parallelism",
                "negative_parallelism",
                "negative_parallelism",
            ],
        )

    def test_negative_parallelism_allows_direct_technical_comparison(self) -> None:
        result = self.run_cli(
            "lint",
            "-",
            "--format",
            "json",
            input_text="Use TLS rather than HTTP.",
        )
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertEqual(json.loads(result.stdout)["summary"]["diagnostics"], 0)

    def test_allowed_phrase_suppresses_an_exact_rhetorical_exception(self) -> None:
        self.write_project_config(
            '[terms]\nallowed = ["not only smaller, but also faster"]\n'
        )
        result = self.run_cli(
            "lint",
            "-",
            "--format",
            "json",
            input_text="The build is not only smaller, but also faster.",
        )
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertEqual(json.loads(result.stdout)["summary"]["diagnostics"], 0)

    def test_restricted_vocabulary_reports_each_occurrence(self) -> None:
        result = self.run_cli(
            "lint",
            "-",
            "--format",
            "json",
            input_text=(
                "The intricate guide showcases a vibrant design. "
                "The guide remains intricate."
            ),
        )
        contextual = self.run_cli(
            "lint",
            "-",
            "--format",
            "json",
            input_text="The roadmap aligns memory on a page boundary.",
        )
        diagnostics = json.loads(result.stdout)["documents"][0]["diagnostics"]
        self.assertEqual(
            [item["rule"] for item in diagnostics],
            ["restricted_vocabulary"] * 4,
        )
        self.assertEqual(json.loads(contextual.stdout)["summary"]["diagnostics"], 0)

    def test_modes_change_restricted_vocabulary_severity(self) -> None:
        developer = self.run_cli(
            "lint",
            "-",
            "--format",
            "json",
            input_text="The intricate parser reads input.",
        )
        strict = self.run_cli(
            "lint",
            "-",
            "--mode",
            "strict",
            "--format",
            "json",
            input_text="The intricate parser reads input.",
        )
        developer_diagnostic = json.loads(developer.stdout)["documents"][0][
            "diagnostics"
        ][0]
        strict_diagnostic = json.loads(strict.stdout)["documents"][0]["diagnostics"][0]
        self.assertEqual(developer_diagnostic["severity"], "warning")
        self.assertEqual(strict_diagnostic["severity"], "error")

    def test_restricted_vocabulary_settings_are_layered_and_configurable(self) -> None:
        self.write_project_config(
            """
[restricted_vocabulary]
additional = ["polished arc"]
exceptions = ["intricate"]
"""
        )
        result = self.run_cli(
            "lint",
            "-",
            "--format",
            "json",
            input_text="The intricate guide defines a polished arc.",
        )
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        diagnostics = json.loads(result.stdout)["documents"][0]["diagnostics"]
        self.assertEqual(
            [item["rule"] for item in diagnostics],
            ["restricted_vocabulary"],
        )
        self.assertIn("polished arc", diagnostics[0]["message"])

    def test_restricted_vocabulary_exception_is_an_exact_form(self) -> None:
        self.write_project_config(
            '[restricted_vocabulary]\nexceptions = ["intricate"]\n'
        )
        result = self.run_cli(
            "lint",
            "-",
            "--format",
            "json",
            input_text="The intricate guide describes several intricacies.",
        )
        diagnostics = json.loads(result.stdout)["documents"][0]["diagnostics"]
        self.assertEqual(
            [item["rule"] for item in diagnostics], ["restricted_vocabulary"]
        )
        self.assertIn("intricacies", diagnostics[0]["message"])

    def test_quotations_and_approved_terms_are_protected(self) -> None:
        self.write_glossary(
            "| robust | A project-specific parser mode. | | Approved | README.md |\n"
        )
        result = self.run_cli(
            "lint",
            "-",
            "--format",
            "json",
            input_text=(
                'The parser is robust. "The module plays a crucial role."\n\n'
                "> The guide presents a vibrant tapestry that showcases a journey.\n"
            ),
        )
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertEqual(json.loads(result.stdout)["summary"]["diagnostics"], 0)

    def test_approved_term_does_not_hide_a_larger_formulaic_phrase(self) -> None:
        self.write_glossary(
            "| pivotal | A project-specific release class. | | Approved | README.md |\n"
        )
        result = self.run_cli(
            "lint",
            "-",
            "--format",
            "json",
            input_text="The module plays a pivotal role in parsing.",
        )
        diagnostics = json.loads(result.stdout)["documents"][0]["diagnostics"]
        self.assertEqual([item["rule"] for item in diagnostics], ["formulaic_phrase"])

    def test_invalid_restricted_vocabulary_config_exits_two(self) -> None:
        config = self.root / "bad-style.toml"
        config.write_text(
            '[restricted_vocabulary]\nexceptions = "intricate"\n',
            encoding="utf-8",
        )
        result = self.run_cli(
            "lint",
            "-",
            "--config",
            str(config),
            input_text="Text.",
        )
        self.assertEqual(result.returncode, 2)
        self.assertIn("must be an array of non-empty strings", result.stderr)

    def write_discovery_tree(self) -> None:
        (self.project / "README.md").write_text(
            "The parser reads the file.\n", encoding="utf-8"
        )
        (self.project / "LICENSE").write_text(
            "Permission is hereby granted, free of charge, to any person "
            "obtaining a copy of this software and associated documentation "
            "files, to deal in the Software without restriction.\n",
            encoding="utf-8",
        )
        (self.project / "CHANGELOG.md").write_text(
            "The release was shipped by the robust release tooling.\n",
            encoding="utf-8",
        )
        (self.project / "notes.md").write_text(
            "The command writes the report.\n", encoding="utf-8"
        )
        vendored = self.project / "node_modules" / "package"
        vendored.mkdir(parents=True)
        (vendored / "readme.md").write_text(
            "This robust library is being leveraged by many teams.\n",
            encoding="utf-8",
        )
        (vendored / "vendored.md").write_text(
            "The adapter maps the record.\n", encoding="utf-8"
        )
        generated = self.project / "docs"
        generated.mkdir()
        (generated / "api.md").write_text(
            "<!-- @generated -->\nThe endpoint was called by the client.\n",
            encoding="utf-8",
        )

    def discovered_paths(self, *arguments: str) -> list[str]:
        result = self.run_cli("lint", *arguments, "--format", "json")
        payload = json.loads(result.stdout)
        return sorted(Path(item["path"]).name for item in payload["documents"])

    def test_directory_scan_skips_boilerplate_and_generated_paths(self) -> None:
        self.write_discovery_tree()
        self.assertEqual(self.discovered_paths("."), ["README.md", "notes.md"])

    def test_explicit_path_lints_an_excluded_file(self) -> None:
        self.write_discovery_tree()
        result = self.run_cli("lint", "LICENSE", "--format", "json")
        payload = json.loads(result.stdout)
        self.assertEqual(payload["summary"]["files"], 1)
        self.assertTrue(payload["documents"][0]["diagnostics"])

    def test_files_exclude_adds_a_project_pattern(self) -> None:
        self.write_discovery_tree()
        self.write_project_config('version = 1\n[files]\nexclude = ["notes.md"]\n')
        self.assertEqual(
            self.discovered_paths("."), ["README.md", "technical-writing.toml"]
        )

    def test_files_exceptions_restore_a_default_exclusion(self) -> None:
        self.write_discovery_tree()
        self.write_project_config(
            'version = 1\n[files]\nexceptions = ["CHANGELOG.md", "node_modules"]\n'
        )
        self.assertEqual(
            self.discovered_paths("."),
            [
                "CHANGELOG.md",
                "README.md",
                "notes.md",
                "readme.md",
                "technical-writing.toml",
                "vendored.md",
            ],
        )

    def test_files_exceptions_restore_a_file_inside_an_excluded_directory(
        self,
    ) -> None:
        self.write_discovery_tree()
        self.write_project_config(
            "version = 1\n"
            "[files]\n"
            'exceptions = ["node_modules/package/vendored.md"]\n'
        )
        self.assertEqual(
            self.discovered_paths("."),
            ["README.md", "notes.md", "technical-writing.toml", "vendored.md"],
        )

    def test_files_exceptions_restore_a_generated_file(self) -> None:
        self.write_discovery_tree()
        self.write_project_config(
            'version = 1\n[files]\nexceptions = ["docs/api.md"]\n'
        )
        self.assertEqual(
            self.discovered_paths("."),
            ["README.md", "api.md", "notes.md", "technical-writing.toml"],
        )

    def test_invalid_files_config_exits_two(self) -> None:
        config = self.root / "bad-files.toml"
        config.write_text('[files]\nexclude = "LICENSE"\n', encoding="utf-8")
        result = self.run_cli("lint", "-", "--config", str(config), input_text="Text.")
        self.assertEqual(result.returncode, 2)
        self.assertIn("files.exclude must be an array", result.stderr)


if __name__ == "__main__":
    unittest.main()
