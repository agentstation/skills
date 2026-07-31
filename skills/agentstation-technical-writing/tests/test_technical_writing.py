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
            "The result was written."
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
        self.assertIn("limit is 3", diagnostics[0]["message"])

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
                "1. Read the complete configuration\n"
                "   before you run the command.\n"
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
            '[rules]\nbanned_word = "error"\n'
            '[terms]\nadditional_banned = ["gadget"]\n',
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
        result = self.run_cli("lint", "docs", "--format", "json")
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        payload = json.loads(result.stdout)
        self.assertEqual(payload["summary"]["files"], 1)
        self.assertEqual(payload["summary"]["diagnostics"], 0)

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


if __name__ == "__main__":
    unittest.main()
