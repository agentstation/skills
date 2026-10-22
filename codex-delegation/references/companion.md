# Direct companion constraints

Read this reference only when the native plugin cannot express the task.

Use the installed plugin's `codex-companion.mjs`. Do not copy it or create a
custom launcher. Check its installed help before the call.

The companion blocks in the foreground unless you pass `--background`. Never
pipe its output. A closed pipe sends SIGPIPE and can detach the job silently.

Use one command line that starts with `node` and the script path. Keep the full
command under 10,000 characters. Do not add a `cd` prefix, `&&`, command
substitution, or newlines in arguments. Pass `--cwd <repository>` on `task`,
`status`, and `result`.

These examples assume `CLAUDE_PLUGIN_ROOT` resolves to the installed Codex plugin.
Replace each path and job identifier with the actual value before use.

```bash
node "${CLAUDE_PLUGIN_ROOT}/scripts/codex-companion.mjs" task --cwd /absolute/repository --model gpt-6.1-sol --effort high "Read /absolute/task.txt first. Investigate only."
```

```bash
node "${CLAUDE_PLUGIN_ROOT}/scripts/codex-companion.mjs" status --cwd /absolute/repository task-identifier
```

```bash
node "${CLAUDE_PLUGIN_ROOT}/scripts/codex-companion.mjs" result --cwd /absolute/repository task-identifier
```

Save long task text in a file. Ask Codex to read that file first. Keep the
assignment's allowed changes and evidence requirements in that file.

Check job state through the supported interface after an interrupted call.
Never treat a timeout or a stale log as proof that the job stopped. Do not
launch a duplicate job until the interface confirms the existing job's state.
