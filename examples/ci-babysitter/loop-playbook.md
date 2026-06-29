# Loop Engineering Playbook

Project: `session-to-loop`

Analysis window: `explicit local inputs`

Input sources: `1 file(s), 5 record(s)`

Redaction: `enabled`

## Loop Proposals

Prepared 1 user-confirmable loop engineering proposal(s) from local evidence.

### 1. CI Babysitter Loop

Decision: `draft` | Mechanism: `loop, skill` | Confidence: `high`

Can use now: `limited` | Can confirm: `yes` | Can delegate: `yes`

Next action: `adopt`

Confirm with one:

- `adopt ci-babysitter as read-only`
- `adopt ci-babysitter as goal-loop`
- `shrink ci-babysitter to skill`
- `reject ci-babysitter`

Goal: Keep CI failures moving toward a verified fix without guessing.

Work shape: `goal-driven` | Archetype: `engineering-maintenance`

Heartbeat: `goal` | Recommended starting level: `goal-loop`

First run:

- Observe: read the state file, current inputs, and latest verifier evidence
- Decide: choose at most 3 item(s), the next action, and any human gate
- Act: pick at most 3 directly evidenced item(s)
- Verify: Run the focused project checks listed in verification.
- State: .session-to-loop/state/ci-babysitter.json
- Stop after: 8 iterations, repeated failure, no progress across two iterations, or a human gate

Trigger:

- When CI is pending or failed on the current branch.

Loop cycle:

- Read the previous state file if it exists.
- Inspect CI status, failed logs, and current git diff.
- Pick at most 1-3 actionable failures by impact and confidence.
- Attempt only low-risk local fixes with direct evidence.
- Run focused verification and record the result.

Verification:

- Relevant local test passes.
- CI becomes green or is clearly blocked.

Stop conditions:

- CI is green.
- Same failure repeats twice.
- Push or merge is required.

Iteration cap: 8 run iteration(s)

Approval boundary: push; merge

Acceptance contract:

- Relevant local test passes.
- CI becomes green or is clearly blocked.

Exit contract:

Continue only if:

- Objective is unchanged.
- Next action stays inside approved scope.
- A verifier can reject bad output.
- New evidence changed or is likely from the next verifier.
- Fewer than 3 item(s) are active in this cycle.
- Fewer than 8 iteration(s) have run.

Return `DONE` when:

- Relevant local test passes.
- CI becomes green or is clearly blocked.

Return `NEEDS_HUMAN` when:

- push is required.
- merge is required.

Return `BLOCKED` when:

- Same failure repeats twice.
- Verifier is unavailable or ambiguous.

Return `BUDGET_STOPPED` when:

- More than 3 item(s) would be required in one cycle.
- 8 iteration(s) are reached.

Why this mechanism: This needs repeated observe-decide-act-verify behavior with state, verification, stop conditions, and resume behavior. Repeated user requests to inspect CI logs before patching and to avoid pushing before verification. Basis: repeated user-language evidence.

## Choose Next Action

Confirm which proposal(s) to adopt from `CI Babysitter Loop`. After confirmation, generate the concrete loop card, draft skill or hook/checklist, and the state-file convention for the selected loop.

- `adopt ci-babysitter as read-only`
- `adopt ci-babysitter as goal-loop`
- `shrink ci-babysitter to skill`
- `reject ci-babysitter`

## Recommended Artifacts

| Candidate | Mechanism | Decision | Confidence |
| --- | --- | --- | --- |
| CI Babysitter Loop | loop, skill | draft | high |

## Rules and Memory Candidates

None.

## Skill Candidates

- `ci-babysitter`: Repeated user requests to inspect CI logs before patching and to avoid pushing before verification.

## Hook Candidates

None.

## Loop Candidates

- `ci-babysitter`: Repeated user requests to inspect CI logs before patching and to avoid pushing before verification.

## Checklist or Approval Gates

None.

## Rejected Candidates

None.

## Source Notes

Files: 1; records: 5; providers: generic=4; source types: generic-jsonl=4

## Private Data

Private candidates and evidence packets are omitted from this public example.

## Shareable Outputs

- cards/ci-babysitter.md
- ci-babysitter-loop.md
- ci-babysitter-skill.md
- summary.json


## Analysis Scope

Approved: `True`

Allowed roles: `user, tool`

Redacted snippets: `enabled`

Output visibility: `private`
