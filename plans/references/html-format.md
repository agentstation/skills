# HTML plan format

The default plan artifact is one self-contained HTML file. The overview
answers three questions at a glance: how close the plan is to done, what
happens next, and what the plan delivers. The file stays plain text, so an
agent edits it like any source file.

Markdown is the fallback when the repository requires it. A Markdown plan
uses the same section names, statuses, and rules, except the Progress
section, which only the HTML format renders. It uses tables for the
ledgers and fenced text sketches for diagrams.

## File rules

- One file, no external resources: no CDN scripts, stylesheets, fonts, or
  images.
- Start from [`../assets/plan-template.html`](../assets/plan-template.html).
- Name the file `<slug>-plan.html`. The proof root is `proof/<slug>/`.
- Keep the file valid HTML. Escape `<` and `&` in prose and code samples.
- Run `scripts/plans check` on the plan after each edit. It reports broken
  links, missing anchors, section order, and unknown statuses.

## Skill-owned blocks

The skill owns three parts of every plan: the `<style data-plans="N">`
block, the `<script data-plans="N">` block, and the `#progress` section. A
plan never edits them and has no other `<style>` or `<script>` element.

To bring a plan to the current template, run `scripts/plans upgrade` on it.
The tool replaces the three parts whole, puts `#progress` directly before
`#current-resume-state`, and leaves all plan content unchanged. It refuses
a `#progress` section that holds authored content, such as a table or a
link. Move that content to its own section first.

The script works from a `file:` URL and over HTTP, with no build step. The
page is complete without JavaScript: the ledger shows all rows and the full
evidence text. Print hides the controls and shows all text.

## Overview header

The `header#overview` element holds, in this order:

1. The `<h1>` title and the status line, as defined in
   [`structure.md`](structure.md).
2. Progress: the percentage, the counts, and a stacked bar, computed from
   the ledger.
3. Current resume state, defined in [`structure.md`](structure.md).
4. Outcome: the one-paragraph invariant.
5. Architecture: the before and after diagrams, side by side.

A sticky plan bar shows the title, the status, the percentage, the age of
the last update, and links to each main section. A cold agent or a human
reads only the overview to know where the plan stands.

The status line carries the plan status as `<code data-plan-status>`, an
`Owner:` field, and for a superseded plan a `Successor:` link. A plan that
is not `active` gets a banner that names its status. A terminal plan
(`complete`, `superseded`, or `abandoned`) shows a grey bar, frozen at its
last percentage.

In the Current resume state table, the row whose first cell is
`Next action` holds the next action. The page marks that row. The record
contains the text `Updated: <ISO time>`, and the page shows its age.

## Ledger markup

The status ledger is a semantic table with four cells per row: ID, Task,
Status, and Evidence.

- One `<tr>` per task, on one line, so rebases cannot lose rows silently.
- The row `id` attribute is the task ID, which makes every task linkable.
- The row `data-status` attribute holds the status name. It may carry a
  parameter, such as `blocked(missing fixture)`. The page reads the bare
  name before the parenthesis.
- The status cell holds the same token in a `<code>` element.
- The evidence cell leads with the current result and links into the proof
  root.
- The task block carries `id="task-<ID>"` on its heading or wrapper.

Example rows:

```html
<tr id="AB1" data-status="todo"><td>AB1</td><td>Route writes through the
commit seam</td><td><code>todo</code></td><td></td></tr>
<tr id="AB2" data-status="rejected"><td>AB2</td><td>Cache the commit
witness</td><td><code>rejected(U7 gate)</code></td><td></td></tr>
```

To change a task status, edit `data-status` and the visible token in one
edit. The states match the task statuses in
[`structure.md`](structure.md). A status outside that list counts as `todo`
and shows a dashed mark, and `plans check` reports it.

The page adds these controls to the ledger:

- Status filter buttons with counts, a search field (`/` focuses it), and
  a phase filter. The URL query string keeps the view, so a link opens the
  same view.
- A clamp on long evidence cells, with a button to show all, and one
  toggle to expand all evidence.
- Links between rows and the rest of the page. Each ID cell links to its
  task block. Each task heading and each log item links to its row.

## Progress computation

The script derives progress from the ledger rows at load time. The bar
reads left to right, and each segment width is a row count:

1. `done`, green.
2. `in_progress`, yellow, the leading edge.
3. `blocked`, red with a hatch.
4. `todo`, the empty track. Unknown statuses count here.
5. `deferred`, `no-action`, and `rejected`, grey, at the right end.

The Progress title holds the percentage of terminal rows (`done`,
`no-action`, and `rejected`). The line beside it gives the terminal and
total row counts. The legend gives the count of each segment, so no
status depends on color alone. The percentage rounds down, so 100% means
every row is terminal. Each legend item filters the ledger. The line under
the bar links each `in_progress`, `blocked`, and unknown row.

When at least two phases exist, a small bar shows each phase. The phase of
an ID is its letters and first number (`NM2.4` is in `NM2`). A dotted ID
without a number before the dot uses the text before the dot (`NPC.5` is
in `NPC`). Other IDs go to `Other`. A plan whose IDs have no dot has no
phases.

The colors are tokens on `:root`, with dark-mode and print values. The
ledger stays the single source of truth.

## Plan summary message

When a page frames the plan, the plan script posts one message to the
parent window after it computes progress. The plans index reads this
message. The message is the contract between a plan and the index:

```text
{ type: "plan-summary", version: 2, summary: {
    title, status, statusToken, updated, modified, owner, outcome,
    nextAction, total, terminal, percent, counts, inProgress, blocked,
    unknown, phases } }
```

- `title` is the `<h1>` text. `status` is the bare `data-plan-status`
  name, and `statusToken` is its visible token.
- `updated` is the full time after `Updated:` in Current resume state,
  with its fraction and time zone. `modified` is `document.lastModified`.
- `owner` is the `Owner:` field of the status line, or an empty string.
- `outcome` is the Outcome blockquote text.
- `nextAction` is the `Next action` row of the Current resume state table.
  Without that row, it is the text after `Next action:` in the status line.
- `counts` holds the five segment counts. `inProgress`, `blocked`, and
  `unknown` list rows as `{ id, task, status }`.
- `phases` lists `{ key, total, terminal, counts }` in ledger order, or is
  empty.

The plan posts to `*` only from a `file:` URL, where no other origin can
frame it. Over HTTP it posts only to its own origin. Change the message
shape only with a new `version`, and update the index template in the same
change. The index accepts versions 1 and 2.

## Plans index page

A repository with a plans directory keeps `index.html` beside the plans.
Copy [`../assets/plans-index.html`](../assets/plans-index.html). The index
is the only routing document. Keep no README table beside it.

The page has three sections:

1. Active plans: totals as tiles, then one card per active plan. A card
   holds the title, the owner, the update age, and the progress with its
   phases. It also holds the next action and the in-progress, blocked, and
   unknown task IDs. Links open the plan, its resume state, and its ledger.
2. Work with no owner: one `<tr id="unowned-<slug>">` row per item, on one
   line, with the columns Item, Why it matters, and Trigger. Mark a trigger
   date as `<time datetime="YYYY-MM-DD">`, one per Trigger cell. The page
   marks a date that is due or near. A date in plain text gets no mark.
   With no rows, the page hides the table and says that no open work is
   without an owner.
3. Routing: the rules, then `<ol id="plan-list">` under Execution order.
   This list is the manifest.

Sort and filter the cards with the toolbar. The default sort puts the plan
nearest to done first: the highest percentage, then the fewest open rows,
then manifest order. Other sorts are most blocked, most in progress,
recently updated, stalest first, and execution order. The filters are a
text search and the toggles Has blocked, Has in progress, and Stale. The
URL query string keeps the view. A card shows its age after 3 days and a
Stale badge after 7 days.

- List each plan that is not terminal in the manifest, in execution order,
  one link per plan. Edit the list in the same change as a plan lifecycle
  transition.
- The page loads each listed plan in a hidden frame and reads its summary
  message. It shows only plans whose live status is `active`. A plan that
  becomes terminal leaves the board before an agent removes its manifest
  item.
- A listed plan that sends no summary in 15 seconds shows as a card with a
  link. Use this to find a broken link or a plan without the current
  script.
- The page reads every plan again each minute while it is visible, when
  the tab becomes visible, and on Refresh. It works from a `file:` URL,
  where the browser blocks `fetch`, and from a local HTTP server.
- Without JavaScript, the manifest list is the index.

An index differs from the template only in its manifest items, its
unowned rows, and the lede of the unowned section.

## Editing rules

- Edit the file as text with normal file tools.
- Keep the section order and the section `id` attributes from the
  template. The recovery loop and the plan summary message depend on them.
- Never edit the skill-owned blocks. Run `scripts/plans upgrade` instead.
- Append a log row before the log table's closing `</tbody>`. The
  template keeps the script in `<head>`. The execution log is therefore
  the last content in the file, and only closing tags follow it.
- Write the Item cell of a log row as plain task IDs, so the page links
  them.
- Rotate older log rows through the [compaction procedure](context-budget.md).
  Keep the history link above the recent log table.
- Keep task IDs and row order stable.
- Update diagrams when a task changes the target structure, and keep
  component names identical across the before and after views.
- Keep the plan prose conformant with the technical-writing skill.
