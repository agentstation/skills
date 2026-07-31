"""Tests for behavioral-evaluation literal semantics."""

from __future__ import annotations

import runpy
import unittest
from pathlib import Path


VALIDATOR = runpy.run_path(
    str(Path(__file__).resolve().parents[1] / "evals" / "validate.py"),
    run_name="technical_writing_eval_validator",
)


class EvalValidationTests(unittest.TestCase):
    def test_forbidden_literal_matches_a_standalone_term(self) -> None:
        pattern = VALIDATOR["forbidden_literal_pattern"]("repo")

        self.assertIsNotNone(pattern.search("Clone the repo."))
        self.assertIsNotNone(pattern.search("Clone the REPO."))

    def test_forbidden_literal_does_not_match_inside_compound(self) -> None:
        pattern = VALIDATOR["forbidden_literal_pattern"]("repo")

        for text in ("repository", "mono-repo", "repo-sync"):
            with self.subTest(text=text):
                self.assertIsNone(pattern.search(text))

    def test_literal_conflicts_use_forbidden_term_boundaries(self) -> None:
        conflicts = VALIDATOR["literal_conflicts"]

        self.assertEqual(conflicts(["repository"], ["repo"]), [])
        self.assertEqual(conflicts(["repo"], ["repo"]), [("repo", "repo")])


if __name__ == "__main__":
    unittest.main()
