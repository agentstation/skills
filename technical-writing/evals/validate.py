#!/usr/bin/env python3
"""Validate the AgentStation writing skill and its behavioral eval manifest."""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path


SKILL_DIR = Path(__file__).resolve().parent.parent
SKILL_FILE = SKILL_DIR / "SKILL.md"
EVAL_FILE = Path(__file__).resolve().parent / "evals.json"
REQUIRED_CATEGORIES = {
    "developer-communication",
    "exact-content",
    "factual-integrity",
    "mode-selection",
    "procedure",
    "restraint",
    "structure",
    "terminology",
}
TERM_CHARACTERS = "A-Za-z0-9_-"


def fail(message: str) -> None:
    raise ValueError(message)


def parse_frontmatter(text: str) -> tuple[dict[str, str], str]:
    lines = text.splitlines()
    if not lines or lines[0] != "---":
        fail("SKILL.md must start with YAML frontmatter")
    try:
        end = lines.index("---", 1)
    except ValueError as exc:
        raise ValueError("SKILL.md frontmatter is not terminated") from exc
    fields: dict[str, str] = {}
    for line in lines[1:end]:
        if ":" in line and not line.startswith(" "):
            key, _, value = line.partition(":")
            fields[key.strip()] = value.strip().strip("\"'")
    return fields, "\n".join(lines[end + 1 :])


def forbidden_literal_pattern(value: str) -> re.Pattern[str]:
    return re.compile(
        rf"(?<![{TERM_CHARACTERS}]){re.escape(value)}(?![{TERM_CHARACTERS}])",
        re.IGNORECASE,
    )


def literal_conflicts(
    protected: list[str],
    forbidden: list[str],
) -> list[tuple[str, str]]:
    return [
        (protected_value, forbidden_value)
        for protected_value in protected
        for forbidden_value in forbidden
        if forbidden_literal_pattern(forbidden_value).search(protected_value)
    ]


def validate_skill() -> None:
    text = SKILL_FILE.read_text(encoding="utf-8")
    frontmatter, body = parse_frontmatter(text)
    name = frontmatter.get("name")
    if name != SKILL_DIR.name:
        fail(f"frontmatter name {name!r} does not match {SKILL_DIR.name!r}")
    description = frontmatter.get("description", "")
    if not description:
        fail("frontmatter description is required")
    if len(description) > 1024:
        fail(f"description is {len(description)} characters; maximum is 1024")
    words = re.findall(r"\b[\w'-]+\b", body)
    if len(words) > 400:
        fail(f"SKILL.md body is {len(words)} words; always-on limit is 400")
    for target in re.findall(r"\]\(([^)]+\.md)\)", body):
        if not (SKILL_DIR / target).is_file():
            fail(f"linked reference does not exist: {target}")


def validate_evals() -> None:
    data = json.loads(EVAL_FILE.read_text(encoding="utf-8"))
    if data.get("skill_name") != SKILL_DIR.name:
        fail("eval skill_name must match the skill directory")
    cases = data.get("evals")
    if not isinstance(cases, list) or not cases:
        fail("evals must be a non-empty list")

    ids: set[str] = set()
    categories: set[str] = set()
    smoke_count = 0
    for index, case in enumerate(cases):
        if not isinstance(case, dict):
            fail(f"eval {index} must be an object")
        case_id = case.get("id")
        if not isinstance(case_id, str) or not case_id:
            fail(f"eval {index} needs a non-empty string id")
        if case_id in ids:
            fail(f"duplicate eval id: {case_id}")
        ids.add(case_id)

        category = case.get("category")
        if category not in REQUIRED_CATEGORIES:
            fail(f"{case_id}: unknown category {category!r}")
        categories.add(category)
        smoke_count += case.get("smoke") is True

        for field in ("prompt", "expected_output"):
            if not isinstance(case.get(field), str) or not case[field].strip():
                fail(f"{case_id}: {field} must be a non-empty string")
        assertions = case.get("assertions")
        if not isinstance(assertions, list) or not assertions:
            fail(f"{case_id}: assertions must be a non-empty list")
        for field in ("protected_literals", "forbidden_literals"):
            values = case.get(field)
            if not isinstance(values, list) or not all(
                isinstance(value, str) and value for value in values
            ):
                fail(f"{case_id}: {field} must be a list of non-empty strings")
        conflicts = literal_conflicts(
            case["protected_literals"],
            case["forbidden_literals"],
        )
        if conflicts:
            fail(f"{case_id}: protected and forbidden literals conflict: {conflicts}")

    missing = REQUIRED_CATEGORIES - categories
    if missing:
        fail(f"missing eval categories: {sorted(missing)}")
    if smoke_count < 8:
        fail(f"only {smoke_count} smoke cases; at least 8 are required")


def main() -> int:
    try:
        validate_skill()
        validate_evals()
    except (OSError, ValueError, json.JSONDecodeError) as exc:
        print(f"FAIL {exc}", file=sys.stderr)
        return 1
    print("ok: technical-writing skill and eval manifest valid")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
