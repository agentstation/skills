# Native plugin procedure

Read this procedure before the first Claude Code delegation.

Use the installed `openai/codex-plugin-cc` interface. Check its current commands
and help before use. The upstream interface can change independently of this
skill.

1. Check readiness with `/codex:setup`.
2. Select an eligible model and effort through `model-selection`.
3. Check that the installed plugin accepts that model and effort.
4. Use `codex:codex-rescue` or `/codex:rescue` for a scoped assignment.

For example, after both checks accept this pair:

```text
/codex:rescue --fresh --model gpt-6.1-sol --effort high Investigate the failing parser tests. Make no edits. Report evidence and unknowns.
```

Pass the model through the native model parameter. Pass effort through the
plugin's `--effort` flag. A Claude Agent model parameter does not set Codex
reasoning effort. A prompt that names a model does not select it.

The plugin uses Codex configuration, including `~/.codex/config.toml` and
trusted project overrides. Inspect those defaults when explicit flags are absent.
Do not change global defaults as a side effect of a task assignment.

Use `/codex:review` for a normal read-only review. Use
`/codex:adversarial-review` for a focused challenge. These plugin reviews do not
replace the repository's required structured autoreview gate.

Use `/codex:status`, `/codex:result`, and `/codex:cancel` for explicit background
jobs. Preserve the job identifier. A foreground call returns its result directly.
Use the supported resume option to continue an existing job within its authority.

## Browser tasks

Use the owner's existing browser permissions for any site the task requires.
Do not require a per-task site list or a separate saved entry for each origin.
The browser runtime enforces the owner's permissions and host policy.

In `~/.codex/browser/config.toml`, `approval_mode = "never_ask"` permits global
origin access when host policy allows it. The `[origins].allowed` list does not
limit that mode to its listed sites. Upload and download permissions are separate.
Do not change browser settings as a side effect of delegation.

A plugin job cannot answer interactive Codex prompts. If access fails, report
the URL and runtime error. Stop only the dependent work until access is available.
Site access does not authorize account changes or other external writes.

See [upstream plugin documentation](https://github.com/openai/codex-plugin-cc)
for setup, authentication, command syntax, and supported runtime options.
