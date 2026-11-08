"""Tests for the plans CLI."""

from __future__ import annotations

import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


SKILL = Path(__file__).resolve().parents[1]
SCRIPT = SKILL / "scripts" / "plans"
ASSETS = SKILL / "assets"

# An older plan: its progress section comes after the outcome, and its
# style and script blocks carry no version.
OLD_PLAN = """<!doctype html>
<html lang="en">
<head>
<title>Old plan</title>
<style>.old { color: red; }</style>
<script>var old = 1;</script>
</head>
<body>
<header id="overview">
  <h1>Old plan</h1>
  <p id="status-line">Status: <code data-plan-status="active">active</code>
    · Owner: a session · Next action: see
    <a href="#current-resume-state">Current resume state</a></p>
  <section id="current-resume-state"><h2>Current resume state</h2>
    <p>Updated: 2026-01-01 UTC.</p></section>
  <section id="outcome"><h2>Outcome</h2><blockquote>Done.</blockquote></section>
  <section id="progress">
    <h2>Progress</h2>
    <div class="bar"></div>
  </section>
  <section id="architecture"><h2>Architecture</h2></section>
</header>
<main>
  <section id="scope"><h2>Scope</h2></section>
  <section id="ledger"><h2>Status ledger</h2><table><tbody>
<tr id="AB1" data-status="done"><td>AB1</td><td>Kept task text</td><td><code>done</code></td><td></td></tr>
<tr id="AB2" data-status="STATUS"><td>AB2</td><td>Second</td><td><code>STATUS</code></td><td></td></tr>
  </tbody></table></section>
  <section id="tasks"><h2>Tasks</h2>
    <h3 id="task-AB1">AB1 Kept task text</h3>
    <h3 id="task-AB2">AB2 Second</h3>
    <p><a href="#AB1">LINK</a></p></section>
  <section id="goal"><h2>Goal</h2></section>
  <section id="execution-log"><h2>Execution log</h2></section>
</main>
</body>
</html>
"""


def plan(status="todo", link="AB1"):
    return OLD_PLAN.replace("STATUS", status).replace("LINK", link) \
        .replace('href="#AB1"', 'href="#%s"' % link)


class PlansCliTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temporary = tempfile.TemporaryDirectory()
        self.addCleanup(self.temporary.cleanup)
        self.root = Path(self.temporary.name)

    def run_cli(self, *arguments: str) -> subprocess.CompletedProcess[str]:
        return subprocess.run(
            [sys.executable, str(SCRIPT), *arguments],
            capture_output=True, text=True, cwd=self.root, check=False)

    def write(self, name: str, text: str) -> Path:
        path = self.root / name
        path.write_text(text, encoding="utf-8")
        return path

    def test_templates_pass_check(self) -> None:
        result = self.run_cli(
            "check", str(ASSETS / "plan-template.html"),
            str(ASSETS / "plans-index.html"))
        self.assertEqual(result.returncode, 0, result.stdout)
        self.assertIn("0 error(s)", result.stdout)

    def test_upgrade_replaces_blocks_and_moves_progress(self) -> None:
        path = self.write("old-plan.html", plan())
        result = self.run_cli("upgrade", path.name)
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn("upgraded old-plan.html", result.stdout)
        text = path.read_text(encoding="utf-8")
        self.assertNotIn(".old { color: red; }", text)
        self.assertNotIn("var old = 1;", text)
        self.assertEqual(text.count("<style"), 1)
        self.assertEqual(text.count("<script"), 1)
        self.assertIn('<style data-plans="', text)
        self.assertLess(text.index('<section id="progress">'),
                        text.index('<section id="current-resume-state">'))
        self.assertLess(text.index('<section id="current-resume-state">'),
                        text.index('<section id="outcome">'))
        self.assertIn("<td>Kept task text</td>", text)

        again = self.run_cli("upgrade", path.name)
        self.assertIn("current old-plan.html", again.stdout)
        self.assertEqual(path.read_text(encoding="utf-8"), text)

        check = self.run_cli("check", path.name)
        self.assertEqual(check.returncode, 0, check.stdout)
        self.assertNotIn("older than version", check.stdout)

    def test_dry_run_writes_nothing(self) -> None:
        path = self.write("old-plan.html", plan())
        result = self.run_cli("upgrade", "--dry-run", path.name)
        self.assertIn("would upgrade old-plan.html", result.stdout)
        self.assertEqual(path.read_text(encoding="utf-8"), plan())

    def test_upgrade_refuses_authored_progress(self) -> None:
        authored = plan().replace(
            '<div class="bar"></div>',
            '<div class="bar"></div><p><a href="proof/x.md">Cases</a></p>')
        path = self.write("old-plan.html", authored)
        result = self.run_cli("upgrade", path.name)
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("authored content", result.stderr)
        self.assertEqual(path.read_text(encoding="utf-8"), authored)

    def test_check_reports_old_order_and_blocks(self) -> None:
        path = self.write("old-plan.html", plan())
        result = self.run_cli("check", path.name)
        self.assertEqual(result.returncode, 1)
        self.assertIn("error: section order", result.stdout)
        self.assertIn("warning: skill blocks are older", result.stdout)

    def test_check_reports_missing_anchor_and_file(self) -> None:
        path = self.write("old-plan.html", plan(link="AB9"))
        self.run_cli("upgrade", path.name)
        text = path.read_text(encoding="utf-8").replace(
            "</main>", '<a href="gone.html">x</a></main>')
        path.write_text(text, encoding="utf-8")
        result = self.run_cli("check", path.name)
        self.assertEqual(result.returncode, 1)
        self.assertIn("missing anchor: #AB9", result.stdout)
        self.assertIn("missing file: gone.html", result.stdout)

    def test_check_warns_on_unknown_status(self) -> None:
        path = self.write("old-plan.html", plan(status="parked"))
        self.run_cli("upgrade", path.name)
        result = self.run_cli("check", path.name)
        self.assertEqual(result.returncode, 0, result.stdout)
        self.assertIn("AB2: unknown task status parked", result.stdout)

    def test_check_accepts_parameterized_status(self) -> None:
        path = self.write("old-plan.html", plan(status="blocked(FD3)"))
        self.run_cli("upgrade", path.name)
        result = self.run_cli("check", path.name)
        self.assertEqual(result.returncode, 0, result.stdout)
        self.assertNotIn("unknown task status", result.stdout)

    def test_check_reports_duplicate_ledger_id(self) -> None:
        text = plan().replace('<tr id="AB2"', '<tr id="AB1"')
        path = self.write("old-plan.html", text)
        self.run_cli("upgrade", path.name)
        result = self.run_cli("check", path.name)
        self.assertEqual(result.returncode, 1)
        self.assertIn("duplicate ledger id: AB1", result.stdout)


if __name__ == "__main__":
    unittest.main()
