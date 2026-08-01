# Architecture repair in plans

Plans repair the architecture problems that execution reveals, not only
the feature scope they started with. This reference defines how to find a
pocket of complexity, how to repair it at a seam, and how seam quality
becomes the verification.

## Pockets of complexity

A pocket of complexity is a region where one concept has no single owner.
Common forms: duplicated policy, a file that mixes transport with domain
rules, two modules that own the same invariant, or a recurring defect
cluster.

Signals during execution:

- One conceptual fix touches many files.
- A test needs deep mocks to reach the behavior.
- The same area produces repeated findings.
- A new feature cannot state verifiable acceptance criteria, because no
  boundary exposes the behavior.

Record each pocket as a finding with evidence, and route it to an owning
task. The plan absorbs the repair when it is in scope. Otherwise the
finding becomes a follow-up ticket with a named owner.

## Repair at the owning seam

A seam is a language-native boundary that owns one domain concept and its
contract. Repair method:

1. Name the concept and its contract.
2. Move the invariants, state transitions, errors, and side effects behind
   the seam.
3. Separate policy from transport, storage, framework, and vendor detail.
4. Adapt the callers to the contract.
5. Delete the duplicate ownership.

State the target as goals, not as implementations. Name the means that are
not goals, so the next agent does not reify a backend detail into the
design. The seams are the architecture. The backends are details that
serve it.

## Seam quality bar

A seam is real when it has a named contract and at least two real
consumers, or one consumer plus a named near-term second. One hypothetical
adapter is not a seam. A high-quality seam:

- Owns its invariant completely. No caller re-checks it.
- Exposes behavior that a test can assert as data or state outcomes.
- Keeps a stable contract while implementations change behind it.

## Seam quality as verification

Prioritize the seam repairs that verification depends on. When a plan
cannot state
verifiable acceptance for a task, repair the owning seam first, then write
the acceptance as seam-contract tests.

Behavior tests at the seam assert data and state outcomes, not hit
counters. Do not mock the contract the test must prove. A cross-boundary
test writes a sentinel on one side of the boundary and proves the other
side cannot observe it.

## Before and after diagrams

A plan that changes structure shows the same components before and after:

- Keep component names identical across both diagrams, so the delta is
  scannable.
- Show ownership and dependency direction, not deployment detail.
- Mark the seams the plan creates or repairs.

Use inline SVG or styled boxes in an HTML plan, and fenced text sketches
in a Markdown plan. Keep each diagram small enough to read without
scrolling.

## Decisions and refusals

Ratify each structural decision as a dated entry with a stable ID,
evidence, and consequence. Record each rejected design with the reason and
a re-open condition. A rejection backed by a measurement stays closed
until a named substrate assumption changes.
