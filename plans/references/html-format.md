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
2. Current resume state, defined in [`structure.md`](structure.md).
3. Outcome: the one-paragraph invariant.
4. Progress: the percentage and the legend on the title row, then a
   stacked bar, computed from the ledger.
5. Architecture: the before and after diagrams, side by side.

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

The template's inline script derives progress from the ledger rows at load
time. The bar reads left to right, and each segment width is a row count:

1. `done`, green.
2. `in_progress`, yellow, the leading edge.
3. `blocked`, red with a hatch.
4. `todo`, the empty track.
5. `deferred`, `no-action`, and `rejected`, grey, at the right end.

The Progress title row holds the percentage of terminal rows (`done`,
`no-action`, and `rejected`), the terminal and total row counts, and the
legend. The percentage rounds down, so 100% means every row is terminal.
The legend gives the count of each segment, so no status depends on color
alone. The line under the bar links each `in_progress` and `blocked` row.
It also links each row with an unknown status, which counts as `todo`.

The ledger status cells use the same colors. The colors are tokens on
`:root`, with dark-mode and print values. The ledger stays the single
source of truth. Without JavaScript the table still reads correctly, and the
bar stays empty.

## Plan summary message

When a page frames the plan, the plan script posts one message to the
parent window after it computes progress. The plans index reads this
message. The message is the contract between a plan and the index:

```text
{ type: "plan-summary", version: 1, summary: {
    title, status, statusToken, updated, modified, outcome, nextAction,
    total, terminal, percent, counts, inProgress, blocked, unknown } }
```

- `title` is the `<h1>` text. `status` is the bare `data-plan-status`
  name, and `statusToken` is its visible token.
- `updated` is the first date after `Updated:` in Current resume state.
  `modified` is `document.lastModified`.
- `outcome` is the Outcome blockquote text.
- `nextAction` is the `Next action` row of the Current resume state table.
  Without that row, it is the text after `Next action:` in the status line.
- `counts` holds the five segment counts. `inProgress`, `blocked`, and
  `unknown` list rows as `{ id, task, status }`.

The plan posts to `*` only from a `file:` URL, where no other origin can
frame it. Over HTTP it posts only to its own origin. Change the message
shape only with a new `version`, and update the index template in the same
change.

## Plans index page

A repository with a plans directory keeps `index.html` beside the plans.
Copy [`../assets/plans-index.html`](../assets/plans-index.html). The page
shows each active plan as a card. A card holds the title, the percentage,
the bar, and the legend. It also holds the outcome, the next action, and
the in-progress and blocked task IDs. Totals across the active plans head
the page.

- The `<ol id="plan-list">` is the manifest. List each plan that is not
  terminal, in execution order, one link per plan. Edit the list in the
  same change as a plan lifecycle transition.
- The page loads each listed plan in a hidden frame and reads its summary
  message. It shows only plans whose live status is `active`. A plan that
  becomes terminal leaves the page before an agent removes its manifest
  row.
- The page reads every plan again each minute while it is visible, when
  the tab becomes visible, and on Refresh. It works from a `file:` URL,
  where the browser blocks `fetch`, and from a local HTTP server.
- A listed plan that sends no summary shows as a card with a link. Use
  this to find a broken link or a plan without the current script.
- Without JavaScript, the manifest list is the index.

## Editing rules

- Edit the file as text with normal file tools.
- Keep the section order and the section `id` attributes from the
  template. The recovery loop and the plan summary message depend on them.
- Keep the template's progress script unchanged. To upgrade an older plan,
  replace its progress script, its `#progress` section, and its progress
  styles with the template's versions.
- Append a log row before the log table's closing `</tbody>`. The
  template keeps the script in `<head>`. The execution log is therefore
  the last content in the file, and only closing tags follow it.
- Rotate older log rows through the [compaction procedure](context-budget.md).
  Keep the history link above the recent log table.
- Keep task IDs and row order stable.
- Update diagrams when a task changes the target structure, and keep
  component names identical across the before and after views.
- Keep the plan prose conformant with the technical-writing skill.
