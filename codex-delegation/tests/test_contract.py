"""Check durable delegation constraints without starting an agent job."""

from __future__ import annotations

import json
import re
import shlex
import unittest
from pathlib import Path


SKILL = Path(__file__).resolve().parents[1]


def read(relative: str) -> str:
    return (SKILL / relative).read_text(encoding="utf-8")


class DelegationContractTests(unittest.TestCase):
    def test_document_reference_links_resolve(self) -> None:
        for document in SKILL.rglob('*.md'):
            for target in re.findall(r'\]\(([^)]+)\)', document.read_text()):
                if '://' in target or target.startswith('#'):
                    continue
                with self.subTest(document=document, target=target):
                    self.assertTrue((document.parent/target.split('#')[0]).is_file())

    def test_companion_examples_obey_transport_contract(self) -> None:
        companion = read("references/companion.md")
        examples = re.findall(r"```bash\n(.*?)\n```", companion, re.DOTALL)
        self.assertEqual(len(examples), 3)
        operations = set()
        for command in examples:
            with self.subTest(command=command):
                self.assertLess(len(command), 10_000)
                self.assertNotIn("\n", command)
                for forbidden in ("|", "&&", "$(", "`", ";"):
                    self.assertNotIn(forbidden, command)
                arguments = shlex.split(command)
                self.assertEqual(arguments[0], "node")
                self.assertTrue(arguments[1].endswith("/scripts/codex-companion.mjs"))
                operations.add(arguments[2])
                self.assertEqual(arguments[arguments.index("--cwd") + 1], "/absolute/repository")
                if arguments[2] == "task":
                    self.assertEqual(arguments[arguments.index("--model") + 1], "gpt-6.1-sol")
                    self.assertEqual(arguments[arguments.index("--effort") + 1], "high")
                    self.assertIn("Read /absolute/task.txt first", arguments[-1])
        self.assertEqual(operations, {"task", "status", "result"})

    def test_trigger_fixture_schema_and_both_boundaries(self) -> None:
        fixtures = json.loads(read('evals/evals.json'))
        self.assertEqual(fixtures['skill_name'], SKILL.name)
        cases = fixtures['evals']
        self.assertEqual(len({case['id'] for case in cases}), len(cases))
        self.assertEqual(len({case['prompt'] for case in cases}), len(cases))
        self.assertEqual({case['should_trigger'] for case in cases}, {True, False})
        for case in cases:
            with self.subTest(case=case['id']):
                self.assertIsInstance(case['should_trigger'], bool)
                for field in ['prompt', 'expected_output']:
                    self.assertIsInstance(case[field], str)
                    self.assertTrue(case[field].strip())
                self.assertTrue(case['assertions'])
                for assertion in case['assertions']:
                    self.assertIsInstance(assertion, str)
                    self.assertTrue(assertion.strip())


if __name__ == '__main__':
    unittest.main()
