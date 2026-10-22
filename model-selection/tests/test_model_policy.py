from __future__ import annotations

import importlib.util
import json
import subprocess
import sys
import unittest
import tempfile
from unittest.mock import patch
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location('model_policy', ROOT / 'scripts/model_policy.py')
assert SPEC and SPEC.loader
POLICY = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(POLICY)


class PolicyTests(unittest.TestCase):
    def test_frontier_matches_owner_pairs(self):
        rows = POLICY.frontier()
        self.assertEqual(len(rows), 14)
        self.assertEqual([(r['family'], r['effort']) for r in rows],
            [('gpt-6-luna', e) for e in ['low','medium','high','xhigh','max']]
            + [('gpt-6-1-sol', e) for e in ['low','medium','high','xhigh','max']]
            + [('claude-opus-5-5','high'), ('claude-opus-5-5','xhigh'),
               ('claude-sonnet-5-5','max'), ('claude-opus-5-5','max')])

    def test_role_limits_precede_unknown_model_and_frontier_options(self):
        for name in ['fable', 'anthropic/claude-fable-5-1', 'anthropic:claude-fable-5',
                     'Haiku', 'bedrock/CLAUDE_HAIKU_5_5', 'gpt-6-astra', 'openai/astra']:
            with self.subTest(model=name), self.assertRaises(POLICY.PolicyError):
                POLICY.validate_assignment(name, 'high', role='reviewer', allow_unknown=True,
                                           require_frontier=False)

    def test_fable_only_coordinates(self):
        result = POLICY.validate_assignment('fable','high',role='coordinator')
        self.assertEqual(result['model'], 'claude-fable-5-1')
        with self.assertRaises(POLICY.PolicyError):
            POLICY.validate_assignment('fable','high',role='worker')

    def test_astra_requires_narrow_complex_focus(self):
        for kwargs in [{}, {'role':'specialist'}, {'role':'specialist','focused':True},
                       {'role':'specialist','complexity':'high'}]:
            with self.subTest(kwargs=kwargs), self.assertRaises(POLICY.PolicyError):
                POLICY.validate_assignment('astra','high',**kwargs)
        result = POLICY.validate_assignment('astra','high',role='specialist',
                                            complexity='high', focused=True)
        self.assertEqual(result['model'],'gpt-6-astra')

    def test_opus_complex_work_requires_ultracode(self):
        for role,complexity in [('coordinator','routine'),('worker','high')]:
            with self.subTest(role=role), self.assertRaises(POLICY.PolicyError):
                POLICY.validate_assignment('opus','high',role=role,complexity=complexity)
            POLICY.validate_assignment('opus','high',role=role,complexity=complexity,ultracode=True)

    def test_dominated_and_retired_pairs_are_not_routine_workers(self):
        for model,effort in [('opus','medium'),('sonnet','high'),('gpt-5.6-terra','max'),
                             ('gpt-6-sol','high')]:
            with self.subTest(model=model), self.assertRaises(POLICY.PolicyError):
                POLICY.validate_assignment(model,effort)

    def test_opaque_defaults_do_not_escape_policy(self):
        for model in ['', 'auto', 'default', 'latest', 'anthropic/auto', 'openrouter/auto:free', 'provider/latest:0']:
            with self.subTest(model=model), self.assertRaises(POLICY.PolicyError):
                POLICY.validate_assignment(model,'high',allow_unknown=True)

    def test_explicit_external_adapter_model_can_remain_available(self):
        POLICY.validate_assignment('z-ai/glm-5.3','max',role='reviewer',allow_unknown=True)
        POLICY.validate_assignment('grok-4.5',None,role='reviewer',allow_unknown=True)
        with self.assertRaises(POLICY.PolicyError):
            POLICY.validate_assignment('z-ai/glm-5.3','max',role='reviewer')

    def test_availability_is_checked_without_silent_fallback(self):
        availability = {'gpt-6-1-sol':['medium','high']}
        with self.assertRaises(POLICY.PolicyError):
            POLICY.select_assignment(task='design', available=availability)
        result = POLICY.select_assignment(task='simple', available=availability)
        self.assertEqual((result['model'],result['effort']),('gpt-6.1-sol','medium'))

    def test_default_routes_respect_capability_and_taste(self):
        for task,pair in [('mechanical',('gpt-6-luna','high')),
                          ('simple',('gpt-6.1-sol','medium')),
                          ('implementation',('gpt-6.1-sol','high')),
                          ('design',('claude-opus-5-5','high'))]:
            result = POLICY.select_assignment(task=task)
            self.assertEqual((result['model'],result['effort']),pair)

    def test_exact_sonnet_edge_survives_display_rounding(self):
        rows=POLICY.frontier()
        opus=next(r for r in rows if r['family']=='claude-opus-5-5' and r['effort']=='xhigh')
        sonnet=next(r for r in rows if r['family']=='claude-sonnet-5-5')
        self.assertGreater(sonnet['intelligence'],opus['intelligence'])
        self.assertLess(sonnet['intelligence']-opus['intelligence'],0.013)
        self.assertEqual(round(sonnet['intelligence'],1),round(opus['intelligence'],1))

    def test_catalog_and_policy_reject_invalid_versions_and_nonfinite_data(self):
        data=POLICY.load_catalog()
        for value in [float('nan'),float('inf'),True,-1]:
            changed=json.loads(json.dumps(data))
            changed['models'][0]['cost']=value
            with self.subTest(value=value),self.assertRaises(POLICY.PolicyError):
                POLICY.validate_catalog(changed)
        data['schema_version']=999
        with self.assertRaises(POLICY.PolicyError):POLICY.validate_catalog(data)

    def test_cli_failure_is_structured_and_nonzero(self):
        result=subprocess.run([sys.executable,str(ROOT/'scripts/model-selection'),
                               'check','--model','fable','--effort','high','--role','reviewer'],
                              text=True,capture_output=True)
        self.assertEqual(result.returncode,2)
        self.assertEqual(json.loads(result.stderr)['error'],'model_policy_violation')

    def test_runtime_aliases_and_invalid_identity(self):
        for name in ['gpt-6.1-sol', 'openai/gpt-6.1-sol', 'openai:gpt-6.1-sol']:
            self.assertEqual(POLICY.validate_assignment(name, 'high')['model'], 'gpt-6.1-sol')
        for name in [' fable', 'fable\n', 'anthropic/fable unknown', 'anthropic/']:
            with self.subTest(name=name), self.assertRaises(POLICY.PolicyError):
                POLICY.validate_assignment(name, 'high', role='reviewer', allow_unknown=True)
        for effort in ['', False, 1]:
            with self.subTest(effort=effort), self.assertRaises(POLICY.PolicyError):
                POLICY.validate_assignment('sol', effort)

    def test_invalid_availability_and_thresholds_fail_closed(self):
        for availability in [[], {'sol':'high'}, {'sol':[True]}]:
            with self.subTest(availability=availability), self.assertRaises(POLICY.PolicyError):
                POLICY.select_assignment(available=availability)
        for threshold in ['high', True, -1, float('nan')]:
            with self.subTest(threshold=threshold), self.assertRaises(POLICY.PolicyError):
                POLICY.select_assignment(min_intelligence=threshold)
        with self.assertRaises(POLICY.PolicyError):
            POLICY.select_assignment(role='coordinator', min_intelligence=60)
        with self.assertRaises(POLICY.PolicyError):
            POLICY.select_assignment(role='specialist', complexity='high', focused=True,
                                     available={'gpt-6.1-sol':['high']})

    def test_alias_targets_receive_the_same_role_limits(self):
        policy = dict(POLICY._policy())
        policy['aliases'] = policy['aliases'] | {'manager':'claude-fable-5-1'}
        with patch.object(POLICY, '_policy', return_value=policy):
            with self.assertRaises(POLICY.PolicyError):
                POLICY.validate_assignment('manager','high',role='reviewer')

    def test_provider_revision_suffixes_cannot_hide_reserved_families(self):
        for name, role in [('us.anthropic.claude-haiku-4-5-20251001-v1:0','reviewer'),
                           ('bedrock/claude-fable-5-1-v1:0','worker'),
                           ('bedrock/claude-opus-5-5-v1:0','coordinator'),
                           ('azure/gpt-6-astra:2026-10-22','worker'),
                           ('bedrock/claude-opus-5-5-v1:0','reviewer')]:
            with self.subTest(name=name), self.assertRaises(POLICY.PolicyError):
                POLICY.validate_assignment(name,'high',role=role,allow_unknown=True)

    def test_duplicate_availability_aliases_fail_in_both_orders(self):
        entries = [('sol',['high']),('gpt-6.1-sol',['medium'])]
        for availability in [dict(entries),dict(reversed(entries))]:
            with self.assertRaises(POLICY.PolicyError):
                POLICY.select_assignment(available=availability)

    def test_policy_data_cannot_omit_owner_restrictions(self):
        with tempfile.TemporaryDirectory() as directory:
            data_path = Path(directory)
            source = json.loads((ROOT/'data/policy.json').read_text())
            for change in [{'schema_version':True}, {'coordinator_only':[]},
                           {'focused_specialist_only':[]}, {'blocked_families':[]}]:
                (data_path/'policy.json').write_text(json.dumps(source | change))
                POLICY._policy.cache_clear()
                try:
                    with patch.object(POLICY, 'DATA', data_path), self.assertRaises(POLICY.PolicyError):
                        POLICY.validate_assignment('fable','high',role='reviewer')
                finally:
                    POLICY._policy.cache_clear()

    def test_global_instruction_tampering_and_line_limit(self):
        clauses = [
            'Exclude Haiku at every effort.',
            'Reserve Fable exclusively for the orchestrator, manager, or coordinator role.',
            'Do not assign Fable implementation tasks or isolated code-review jobs.',
            'Apply this role limit to manual profiles, automatic selection, and fallback.',
            'Reserve Astra for a narrow, highly complex problem that needs sustained deep focus.',
            'Require multi-agent Ultracode for Opus orchestration or highly complex work.',
        ]
        source = POLICY.render_table() + '\n'.join(clauses) + '\n'
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory)/'AGENTS.md'
            path.write_text(source)
            POLICY.check_global_instructions(path)
            for changed in [source.replace(clauses[1], ''), source.replace('5.4609','5.4608'),
                            source + '\n'*200]:
                path.write_text(changed)
                with self.assertRaises(POLICY.PolicyError):
                    POLICY.check_global_instructions(path)

    def test_global_table_snapshot_contract(self):
        table=POLICY.render_table()
        self.assertEqual(len([line for line in table.splitlines() if line.startswith('| ')]),16)
        self.assertIn('| Claude Sonnet 5.5 | max | 56.0 | 5.4609 |',table)
        self.assertNotIn('Haiku',table)


if __name__ == '__main__':
    unittest.main()
