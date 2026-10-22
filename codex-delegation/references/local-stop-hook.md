# Conditional local stop hook

Read this note only on a machine that already uses the wrapper below.
These paths describe one existing local arrangement. They are not installation
requirements for this skill.

The wrapper is `~/.claude/hooks/stop-review-triage.mjs`. Its registration is in
`~/.claude/settings.json`. The temporary disable marker is
`~/.claude/hooks-state/stop-triage/disabled`.

If this wrapper owns the stop gate, keep the plugin review gate off. Use the
plugin's supported disable command, `/codex:setup --disable-review-gate`, only
within the user's authorization. Two enabled gates can run duplicate reviews.

Do not install this wrapper, create its marker, or change hook settings merely
because this skill is present. Inspect the actual local configuration first.
