"""Review assignment policy regressions."""
import argparse
import copy
import os
import tempfile
from types import SimpleNamespace
import runpy
import unittest
from pathlib import Path
from unittest import mock

SCRIPT = Path(__file__).resolve().parents[1] / "scripts" / "autoreview"


class SharedModelPolicyTests(unittest.TestCase):
    def setUp(self):
        self.helper = runpy.run_path(str(SCRIPT))
        self.config = copy.deepcopy(self.helper["BUILTIN_REVIEW_CONFIG"])
        self.args = argparse.Namespace(review_policy={"anthropic_max_effort": "max"}, fable_explicit=True)

    def reviewer(self, model, *, effort="high", fallback=None, engine="claude"):
        return argparse.Namespace(engine=engine, model=model, thinking=effort, fallback_model=fallback)

    def test_explicit_approval_cannot_authorize_reserved_or_dominated_reviewers(self):
        for model in ("claude-fable-5-1", "anthropic/fable", "gpt-6-astra", "claude-haiku-4-5", "gpt-5.6-terra"):
            with self.subTest(model=model), self.assertRaises(SystemExit):
                self.helper["enforce_reviewer_policy"]([self.reviewer(model)], self.args)

    def test_every_fallback_requires_an_allowed_review_assignment(self):
        for fallback in ("claude-opus-5-5,claude-fable-5-1", "gpt-6-astra", "claude-haiku-4-5", "gpt-5.6-terra", "claude-opus-5-5,", "claude-opus-5-5,default"):
            with self.subTest(fallback=fallback), self.assertRaises(SystemExit):
                self.helper["enforce_reviewer_policy"]([self.reviewer("claude-opus-5-5", fallback=fallback)], self.args)

    def test_legacy_value_profile_migrates_to_sol_high(self):
        self.assertEqual(self.config["profiles"]["value"]["candidates"], ["sol"])
        self.assertNotIn("terra", self.config["candidates"])
        self.assertNotIn("fable5", self.config["candidates"])

    def test_scored_selection_filters_invalid_assignment_before_ranking(self):
        for model in ("claude-fable-5-1", "gpt-6-astra", "claude-haiku-4-5", "gpt-5.6-terra"):
            candidate = dict(self.config["candidates"]["opus5"], model=model, intelligence=10, taste=10, cost=0, deepswe_pass_rate=100, manual_approval_required=False)
            self.config["candidates"]["legacy"] = candidate
            function = self.helper["scored_candidates"]
            with mock.patch.dict(function.__globals__, {"engine_binary": lambda *_: "/trusted/cli", "detected_host_engine": lambda: None}):
                selected = function(self.config, self.args, include_same_host=True, manual_approval_granted=True)
            self.assertNotIn("legacy", [item[0] for item in selected], model)

    def test_exact_profile_cannot_restore_legacy_fable(self):
        self.config["candidates"]["legacy"] = dict(self.config["candidates"]["opus5"], model="claude-fable-5-1", manual_approval_required=True)
        self.config["profiles"]["legacy"] = {"candidates": ["legacy"]}
        function = self.helper["select_profile_candidates"]
        with mock.patch.dict(function.__globals__, {"engine_binary": lambda *_: "/trusted/cli"}):
            with self.assertRaises(SystemExit):
                function(self.config, self.args, "legacy", profile_explicit=True)

    def test_missing_policy_fails_closed_with_install_recovery(self):
        function = self.helper["shared_model_policy"]
        function.cache_clear()
        with mock.patch("importlib.util.spec_from_file_location", side_effect=FileNotFoundError("missing")):
            with self.assertRaisesRegex(SystemExit, "install model-selection beside autoreview"):
                function()

    def test_no_config_and_cli_or_environment_cannot_bypass_role_policy(self):
        parse = self.helper["parse_args"]
        for arguments, environment in (
            (["--engine", "claude", "--model", "claude-fable-5-1"], {}),
            (["--reviewers", "claude:claude-fable-5-1:high"], {}),
            (["--engine", "claude"], {"AUTOREVIEW_CLAUDE_MODEL": "claude-fable-5-1"}),
            (["--engine", "claude", "--fallback-model", "claude-fable-5-1"], {}),
        ):
            with self.subTest(arguments=arguments, environment=environment), tempfile.TemporaryDirectory() as temp:
                with mock.patch("sys.argv", ["autoreview", "--no-config", *arguments]), mock.patch.dict(os.environ, environment, clear=True):
                    args = parse()
                    function = self.helper["configure_reviewers"]
                    with mock.patch.dict(function.__globals__, {"engine_binary": lambda *_: "/trusted/cli"}):
                        function(args, Path(temp))
                    reviewers = self.helper["reviewer_args"](args)
                    with self.assertRaises(SystemExit):
                        self.helper["enforce_reviewer_policy"](reviewers, args)

    def test_scored_installer_does_not_install_for_prohibited_candidates(self):
        self.config["candidates"] = {"legacy": dict(self.config["candidates"]["opus5"], model="claude-fable-5-1", manual_approval_required=False)}
        function = self.helper["missing_scored_candidate_engines"]
        with mock.patch.dict(function.__globals__, {"engine_binary": lambda *_: None, "detected_host_engine": lambda: None}):
            self.assertEqual(function(self.config, self.args), [])

    def test_layered_legacy_schema_keeps_auto_usable_but_rejects_exact_fable(self):
        with tempfile.TemporaryDirectory() as temp:
            repo = Path(temp)
            path = repo / ".agents" / "autoreview" / "config.toml"
            path.parent.mkdir(parents=True)
            path.write_text('version = 1\n[candidates.old]\nengine = "claude"\nmodel = "claude-fable-5-1"\neffort = "high"\nmanual_approval_required = true\ncost = 0\nintelligence = 10\ntaste = 10\ndeepswe_pass_rate = 100\n[profiles.old]\ncandidates = ["old"]\n')
            args = argparse.Namespace(no_config=False, config=[])
            function = self.helper["load_review_config"]
            with mock.patch.dict(os.environ, {"AUTOREVIEW_CONFIG": str(repo / "missing.toml")}):
                config, loaded = function(args, repo)
            self.assertEqual(loaded, [path.resolve()])
            function = self.helper["select_profile_candidates"]
            with mock.patch.dict(function.__globals__, {"engine_binary": lambda *_: "/trusted/cli", "detected_host_engine": lambda: "codex"}):
                self.assertEqual(function(config, args, "auto", profile_explicit=False)[0][0], "opus5")
                with self.assertRaises(SystemExit):
                    function(config, args, "old", profile_explicit=True)

    def test_external_adapters_keep_concrete_third_provider_models(self):
        for engine, model, effort in (("cursor", "grok-4.5", None), ("opencode", "opencode/kimi-k3", "max"), ("pi", "third-provider/model", "high")):
            with self.subTest(engine=engine):
                self.helper["enforce_reviewer_policy"]([self.reviewer(model, effort=effort, engine=engine)], self.args)

    def test_external_adapter_cannot_hide_reserved_models_or_use_opaque_defaults(self):
        for model in (None, "auto", "default", "vendor/fable", "vendor/astra", "vendor/haiku"):
            with self.subTest(model=model), self.assertRaises(SystemExit):
                self.helper["enforce_reviewer_policy"]([self.reviewer(model, engine="cursor", effort=None)], self.args)

    def test_known_primary_and_fallback_aliases_dispatch_canonical_runtime_models(self):
        for alias in ("sol", "gpt-6-1-sol"):
            reviewer = self.reviewer(alias, engine="codex")
            self.helper["enforce_reviewer_policy"]([reviewer], self.args)
            self.assertEqual(reviewer.model, "gpt-6.1-sol")
        reviewer = self.reviewer("opus", fallback="opus,anthropic/claude-opus-5-5")
        self.helper["enforce_reviewer_policy"]([reviewer], self.args)
        self.assertEqual(reviewer.model, "claude-opus-5-5")
        self.assertEqual(reviewer.fallback_model, "claude-opus-5-5,claude-opus-5-5")
        external = self.reviewer("openrouter/kimi-k3", engine="opencode")
        self.helper["enforce_reviewer_policy"]([external], self.args)
        self.assertEqual(external.model, "openrouter/kimi-k3")

    def test_known_model_normalization_preserves_adapter_provider_namespaces(self):
        for engine in ("opencode", "pi"):
            with self.subTest(engine=engine):
                reviewer = self.reviewer("anthropic/opus", engine=engine)
                self.helper["enforce_reviewer_policy"]([reviewer], self.args)
                self.assertEqual(reviewer.model, "anthropic/claude-opus-5-5")
        reviewer = self.reviewer("opus", engine="opencode")
        with self.assertRaisesRegex(SystemExit, "provider/model"):
            self.helper["enforce_reviewer_policy"]([reviewer], self.args)
        candidate = dict(self.config["candidates"]["opus5"], engine="opencode", model="opus")
        self.assertIn("provider/model", self.helper["candidate_assignment_error"](candidate, self.config, allow_unknown=True))

    def test_anthropic_aliases_receive_effort_caps_before_profile_installation(self):
        candidate = dict(self.config["candidates"]["opus5"], engine="pi", model="opus", effort="xhigh")
        self.assertIsNotNone(self.helper["candidate_assignment_error"](candidate, self.config, allow_unknown=True))

    def test_known_external_catalog_pairs_need_runtime_effort_evidence(self):
        for engine, effort in (("pi", None), ("opencode", None), ("cursor", None), ("cursor", "high")):
            with self.subTest(engine=engine, effort=effort), self.assertRaisesRegex(SystemExit, "effort"):
                self.helper["enforce_reviewer_policy"]([self.reviewer("claude-opus-5-5", engine=engine, effort=effort)], self.args)
        self.helper["enforce_reviewer_policy"]([self.reviewer("anthropic/claude-opus-5-5", engine="pi", effort="high")], self.args)

    def test_partial_legacy_score_overlays_load_but_do_not_restore_eligibility(self):
        function = self.helper["merge_legacy_review_config"]
        config = function(self.config, {"candidates": {"fable5": {"cost": 0}, "terra": {"taste": 10}}})
        self.helper["validate_review_config"](config)
        config = function(config, {"candidates": {"terra": {"taste": 9}}})
        self.assertEqual(config["candidates"]["fable5"]["cost"], 0)
        self.assertEqual(config["candidates"]["terra"]["taste"], 9)
        select = self.helper["scored_candidates"]
        with mock.patch.dict(select.__globals__, {"engine_binary": lambda *_: "/trusted/cli", "detected_host_engine": lambda: None}):
            selected = select(config, self.args, include_same_host=True, manual_approval_granted=True)
        self.assertTrue({"fable5", "terra"}.isdisjoint(item[0] for item in selected))

    def test_attestation_changes_when_shared_policy_or_catalog_changes(self):
        function = self.helper["review_attestation_key"]
        args = argparse.Namespace(max_priority="P0", web_search=False, allow_partial_panel=False)
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            for relative in ("scripts/model_policy.py", "data/catalog.json", "data/policy.json"):
                path = root / relative
                path.parent.mkdir(exist_ok=True)
                path.write_text("original")
            module = SimpleNamespace(__file__=str(root / "scripts" / "model_policy.py"))
            with mock.patch.dict(function.__globals__, {"shared_model_policy": lambda: module, "substantive_branch_diff_digest": lambda *_: ("base", "diff")}):
                def key():
                    return function(args, [], root, "main", {"app.py"}, "", "")
                before = key()
                for relative in ("scripts/model_policy.py", "data/catalog.json", "data/policy.json"):
                    with self.subTest(relative=relative):
                        (root / relative).write_text("changed")
                        self.assertNotEqual(before, key())
                        (root / relative).write_text("original")


if __name__ == "__main__":
    unittest.main()
