# HTML plan format

The default plan artifact is one self-contained HTML file. The overview
answers three questions at a glance: what the plan delivers, how close it
is to done, and how the architecture changes. The file stays plain text,
so an agent edits it like any source file.

Markdown is the fallback when the repository requires it. A Markdown plan
uses the same section names, statuses, and rules, except the Progress
section, which only the HTML format renders. It uses tables for the
ledgers and fenced text sketches for diagrams.

## File rules

- One file, no external resources: no CDN scripts, stylesheets, fonts, or
  images. Inline the CSS and the one progress script.
- Start from [`../assets/plan-template.html`](../assets/plan-template.html).
- Name the file `<slug>-plan.html`. The proof root is `proof/<slug>/`.
- Keep the file valid HTML. Escape `<` and `&` in prose and code samples.
- The template prints to PDF through the browser print dialog.

## Overview header

The overview is the top of the page, in this order:

1. The status line, as defined in [`structure.md`](structure.md).
2. Outcome: the one-paragraph invariant.
3. Progress: a bar plus counts, computed from the ledger.
4. Architecture: the before and after diagrams, side by side.

The overview is the resume surface. A cold agent or a human reads only the
overview to know where the plan stands.

## Ledger markup

The status ledger is a semantic table:

- One `<tr>` per task, on one line, so rebases cannot lose rows silently.
- The row `id` attribute is the task ID, which makes every task linkable.
- The row `data-status` attribute holds the bare status name, without a
  parameter: one of `todo`, `in_progress`, `blocked`, `deferred`, `done`,
  `no-action`, or `rejected`.
- The visible token in the status cell carries the parameter when the
  status has one, such as `blocked(missing fixture)`.
- The evidence cell holds the proof text and links into the proof root.

Example rows:

```html
<tr id="AB1" data-status="todo"><td>AB1</td><td>Route writes through the
commit seam</td><td><code>todo</code></td><td></td></tr>
<tr id="AB2" data-status="rejected"><td>AB2</td><td>Cache the commit
witness</td><td><code>rejected(U7 gate)</code></td><td></td></tr>
```

To change a task status, edit `data-status` and the visible token in one
edit. The states match the task statuses in
[`structure.md`](structure.md). The template's script and styles also
accept a parameterized `data-status` value, such as `rejected(U7 gate)`,
by reading the bare name before the parameter.

## Progress computation

The template's inline script derives progress from the ledger at load
time. It counts rows and treats `done`, `no-action`, and `rejected` as
terminal. It fills the bar and names the current `in_progress` task. The
ledger stays the single source of truth. Without JavaScript the table
still reads correctly, and the bar stays empty.

## Editing rules

- Edit the file as text with normal file tools.
- Keep the section order and the section `id` attributes from the
  template. The recovery loop depends on them.
- Append a log row before the log table's closing `</tbody>`. The
  template keeps the script in `<head>`. The execution log is therefore
  the last content in the file, and only closing tags follow it.
- Keep task IDs and row order stable.
- Update diagrams when a task changes the target structure, and keep
  component names identical across the before and after views.
- Keep the plan prose conformant with the technical-writing skill.
