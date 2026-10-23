"""Select models under the shared AgentStation role and benchmark policy."""
from __future__ import annotations

import functools
import json
import math
import re
from pathlib import Path
from typing import Any

DATA = Path(__file__).resolve().parents[1] / 'data'
POLICY_VERSION = 2
ROLES = {'worker', 'reviewer', 'coordinator', 'specialist'}
OPAQUE_MODELS = {'', 'auto', 'default', 'latest', 'inherit', 'automatic', 'claude', 'openai', 'anthropic'}


class PolicyError(ValueError):
    """An assignment violates the shared policy or its input contract."""


def _read_json(path: Path) -> dict[str, Any]:
    try:
        value = json.loads(path.read_text(encoding='utf-8'))
    except (OSError, ValueError) as exc:
        raise PolicyError(f'Cannot read model policy data {path}: {exc}') from exc
    if not isinstance(value, dict):
        raise PolicyError(f'Model policy data must be an object: {path}')
    return value


def validate_catalog(value: dict[str, Any]) -> None:
    if type(value.get('schema_version')) is not int or value['schema_version'] != 1 or type(value.get('policy_version')) is not int or value['policy_version'] != POLICY_VERSION:
        raise PolicyError('Unsupported model catalog or policy version')
    if not isinstance(value.get('verified_on'), str) or not re.fullmatch(r'\d{4}-\d{2}-\d{2}', value['verified_on']):
        raise PolicyError('The model catalog requires a verification date')
    rows = value.get('models')
    if not isinstance(rows, list) or not rows:
        raise PolicyError('The model catalog requires measured pairs')
    seen = set()
    for row in rows:
        if not isinstance(row, dict):
            raise PolicyError('Each model pair must be an object')
        for key in ['id', 'family', 'name', 'effort', 'source']:
            if not isinstance(row.get(key), str) or not row[key]:
                raise PolicyError(f'The model pair requires {key}')
        key = row['family'], row['effort']
        if key in seen:
            raise PolicyError(f'Duplicate catalog pair: {key}')
        seen.add(key)
        for field in ['cost', 'intelligence']:
            number = row.get(field)
            if isinstance(number, bool) or not isinstance(number, (float, int)) or not math.isfinite(number) or number < 0:
                raise PolicyError(f'Invalid measured {field} for {row["id"]}')
        if row.get('estimated') is not False:
            raise PolicyError(f'Estimated data cannot define the frontier: {row["id"]}')


@functools.lru_cache(maxsize=1)
def _catalog() -> dict[str, Any]:
    value = _read_json(DATA / 'catalog.json')
    validate_catalog(value)
    return value


def load_catalog() -> dict[str, Any]:
    return json.loads(json.dumps(_catalog()))


@functools.lru_cache(maxsize=1)
def _policy() -> dict[str, Any]:
    value = _read_json(DATA / 'policy.json')
    if type(value.get('schema_version')) is not int or value['schema_version'] != 1 or type(value.get('policy_version')) is not int or value['policy_version'] != POLICY_VERSION:
        raise PolicyError('Unsupported role policy version')
    required_limits = {'blocked_families': ['haiku'], 'coordinator_only': ['fable'],
                       'focused_specialist_only': ['astra'],
                       'ultracode_for_coordination_or_high_complexity': ['opus']}
    if any(value.get(key) != expected for key, expected in required_limits.items()):
        raise PolicyError('Role policy version 2 requires all owner role restrictions')
    for key in ['aliases', 'default_efforts', 'runtime_models', 'taste']:
        if not isinstance(value.get(key), dict):
            raise PolicyError(f'Role policy requires {key}')
    return value


def model_leaf(model: str) -> str:
    if not isinstance(model, str):
        raise PolicyError('The model identity must be a string')
    if model != model.strip() or re.search(r'\s|[\x00-\x1f]', model):
        raise PolicyError('A concrete model identity cannot contain whitespace or control characters')
    return re.split(r'[/ :]', model.casefold().replace('_', '-'))[-1]


def canonical_model(model: str) -> str:
    leaf = model_leaf(model)
    opaque_routes = {'auto', 'default', 'latest', 'inherit', 'automatic'}
    if leaf in OPAQUE_MODELS or any(part in opaque_routes for part in re.split(r'[/ :]', model.casefold())):
        raise PolicyError('Resolve the concrete host model before policy validation')
    return _policy()['aliases'].get(leaf, leaf)


def _role_limits(model: str, role: str, complexity: str, focused: bool, ultracode: bool) -> None:
    if role not in ROLES or complexity not in {'routine', 'high'}:
        raise PolicyError('Unsupported role or complexity')
    if type(focused) is not bool or type(ultracode) is not bool:
        raise PolicyError('Focus and Ultracode evidence must be boolean')
    model_leaf(model)
    leaf = model.casefold().replace('_', '-')
    if any(name in leaf for name in _policy()['blocked_families']):
        raise PolicyError('Haiku is excluded at every effort')
    if any(name in leaf for name in _policy()['coordinator_only']) and role != 'coordinator':
        raise PolicyError('Fable is coordinator-only; workers, reviewers and fallback cannot use it')
    if any(name in leaf for name in _policy()['focused_specialist_only']):
        if role != 'specialist' or complexity != 'high' or not focused:
            raise PolicyError('Astra requires a narrow, highly complex focused specialist assignment')
    if any(name in leaf for name in _policy()['ultracode_for_coordination_or_high_complexity']):
        if (role == 'coordinator' or complexity == 'high') and not ultracode:
            raise PolicyError('Opus coordination or high-complexity work requires multi-agent Ultracode')


def frontier() -> list[dict[str, Any]]:
    rows = [r for r in _catalog()['models']
            if not any(name in r['family'] for name in _policy()['blocked_families'])]
    return [dict(row) for row in sorted(rows, key=lambda r: (r['cost'], r['id']))
            if not any(other['cost'] <= row['cost'] and other['intelligence'] >= row['intelligence']
                       and (other['cost'] < row['cost'] or other['intelligence'] > row['intelligence'])
                       for other in rows)]


def validate_assignment(model: str, effort: str | None, *, role: str = 'worker',
                        complexity: str = 'routine', focused: bool = False,
                        ultracode: bool = False, require_frontier: bool = True,
                        allow_unknown: bool = False) -> dict[str, Any]:
    _role_limits(model, role, complexity, focused, ultracode)
    canonical = canonical_model(model)
    if canonical != model_leaf(model):
        _role_limits(canonical, role, complexity, focused, ultracode)
    if effort is not None and (not isinstance(effort, str) or not effort):
        raise PolicyError('Effort must be a non-empty token or absent')
    if type(require_frontier) is not bool or type(allow_unknown) is not bool:
        raise PolicyError('Policy options must be boolean')
    effort = _policy()['default_efforts'].get(canonical) if effort is None else effort
    rows = [r for r in _catalog()['models'] if r['family'] == canonical]
    if not rows:
        identity = model.casefold().replace('_', '-')
        known_provider = bool(re.search(r'(?:^|[./:-])(?:gpt|claude|openai|anthropic)(?:[./:-]|$)', identity))
        known_provider = known_provider or canonical in _policy()['aliases']
        if not allow_unknown or known_provider:
            raise PolicyError(f'Model is absent from the approved catalog: {model}')
        if effort is not None and (not isinstance(effort, str) or not re.fullmatch(r'[a-z][a-z0-9-]*', effort)):
            raise PolicyError('An external adapter effort must be a supported token or absent')
        return {'model': model, 'effort': effort, 'role': role, 'policy_version': POLICY_VERSION,
                'catalog_verified_on': None, 'external_catalog': True}
    row = next((r for r in rows if r['effort'] == effort), None)
    if row is None:
        raise PolicyError(f'Unsupported catalog pair: {model} at {effort}')
    exception = ('fable' in canonical and role == 'coordinator') or ('astra' in canonical and role == 'specialist')
    if require_frontier and not exception and not any(r['id'] == row['id'] for r in frontier()):
        raise PolicyError(f'Model/effort is outside the routine-worker Pareto frontier: {model} at {effort}')
    return {'model': _policy().get('runtime_models', {}).get(canonical, canonical), 'catalog_model': canonical, 'effort': effort, 'role': role,
            'intelligence': row['intelligence'], 'cost_per_task_usd': row['cost'],
            'taste': _policy()['taste'].get(canonical), 'policy_version': POLICY_VERSION,
            'catalog_verified_on': _catalog()['verified_on'], 'role_exception': exception}


TASK_DEFAULTS = {
    'mechanical': ('gpt-6-luna', 'high', 0),
    'simple': ('gpt-6-1-sol', 'medium', 7),
    'implementation': ('gpt-6-1-sol', 'high', 7),
    'design': ('claude-opus-5-5', 'high', 9),
    'browser': ('gpt-6-1-sol', 'high', 7),
}


def select_assignment(*, task: str = 'implementation', role: str = 'worker',
                      complexity: str = 'routine', focused: bool = False,
                      ultracode: bool = False, available: dict[str, list[str]] | None = None,
                      min_intelligence: float | None = None, min_taste: float | None = None) -> dict[str, Any]:
    if task not in TASK_DEFAULTS:
        raise PolicyError(f'Unknown task class: {task}')
    for number in [min_intelligence, min_taste]:
        if number is not None and (isinstance(number, bool) or not isinstance(number, (int, float))
                                   or not math.isfinite(number) or number < 0):
            raise PolicyError('Quality thresholds must be finite non-negative numbers')
    if available is not None:
        if not isinstance(available, dict) or not all(isinstance(m, str) and isinstance(e, list)
                and all(isinstance(v, str) for v in e) for m, e in available.items()):
            raise PolicyError('Availability must map concrete model identities to effort lists')
        canonical_available = {}
        for model, efforts in available.items():
            canonical = canonical_model(model)
            if canonical in canonical_available:
                raise PolicyError(f'Duplicate availability identities for {canonical}')
            canonical_available[canonical] = efforts
        available = canonical_available
    if role in {'coordinator', 'specialist'}:
        model = 'claude-fable-5-1' if role == 'coordinator' else 'gpt-6-astra'
        result = validate_assignment(model, 'high', role=role, complexity=complexity,
                                     focused=focused, ultracode=ultracode)
        if available is not None and 'high' not in available.get(model, []):
            raise PolicyError(f'Required role model is unavailable: {model} high')
        if result['intelligence'] < (min_intelligence or 0) or result['taste'] < (min_taste or 0):
            raise PolicyError('Required role model does not meet the quality requirements')
        return result
    model, effort, taste_floor = TASK_DEFAULTS[task]
    default = validate_assignment(model, effort)
    score_floor = default['intelligence']
    score_floor = max(score_floor, min_intelligence or 0)
    taste_floor = max(taste_floor, min_taste or 0)
    choices = []
    for row in frontier():
        if row['intelligence'] < score_floor or _policy()['taste'].get(row['family'], 0) < taste_floor:
            continue
        if available is not None and row['effort'] not in available.get(row['family'], []):
            continue
        try:
            choices.append(validate_assignment(row['family'], row['effort'], role=role,
                                               complexity=complexity, focused=focused, ultracode=ultracode))
        except PolicyError:
            continue
    if not choices:
        raise PolicyError('No supported frontier pair meets the role and quality requirements')
    return min(choices, key=lambda r: (r['cost_per_task_usd'], r['model'], r['effort']))


def render_table() -> str:
    labels = {'gpt-6-luna':'GPT-6 Luna', 'gpt-6-1-sol':'GPT-6.1 Sol',
              'claude-opus-5-5':'Claude Opus 5.5', 'claude-sonnet-5-5':'Claude Sonnet 5.5'}
    lines = ['| model | effort | AA intelligence | AA cost/task, USD |',
             '| --- | --- | ---: | ---: |']
    for row in frontier():
        lines.append(f'| {labels.get(row["family"], row["name"])} | {row["effort"]} | '
                     f'{row["intelligence"]:.1f} | {row["cost"]:.4f} |')
    return '\n'.join(lines) + '\n'


def check_global_instructions(path: Path) -> None:
    source = path.read_text(encoding='utf-8')
    if len(source.splitlines()) >= 200:
        raise PolicyError('Global AGENTS.md must remain below 200 lines')
    if render_table() not in source:
        raise PolicyError('Global frontier table differs from the canonical catalog')
    required = [
        'Exclude Haiku at every',
        'Reserve Fable exclusively for the orchestrator, manager, or coordinator role.',
        'Do not assign Fable implementation tasks or isolated code-review jobs.',
        'Apply this role limit to manual profiles, automatic selection, and fallback.',
        'Reserve Astra for a narrow, highly complex problem that needs sustained deep',
        'Require multi-agent',
        'Ultracode for Opus orchestration or highly complex work.',
    ]
    text = re.sub(r'\s+', ' ', source)
    if any(re.sub(r'\s+', ' ', rule) not in text for rule in required):
        raise PolicyError('Global model role restrictions are incomplete')
