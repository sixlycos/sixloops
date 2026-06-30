# Adopt Loop Runbook

Use this workflow when the user replies with `start ...`, `continue ...`,
`run ...`, or asks to execute an existing SixLoops candidate.

## Goal

Run one controlled cycle inside the approved mode, update state, and return one
clear status: `DONE`, `CONTINUE`, review-needed, `BLOCKED`, or
`BUDGET_STOPPED`.

## Workflow

1. Identify the selected candidate and mode.
   - Use the exact reply string when present.
   - Prefer the weakest useful mode.
   - Do not infer approval for merge, deploy, production, credentials, data,
     payment, deletion, or schema changes.

2. Read the latest card or adoption packet.
   - Candidate card: `cards/<candidate-id>.md`.
   - Agent handoff: `claude-loops/<candidate-id>.md`.
   - Adoption packet: `GOAL.md`, `STATE.json`, `HANDOFF.md`, and optional
     `AGENTS-snippet.md`.

3. Create an adoption packet when stateful reuse is needed and none exists:

   ```bash
   python skills/sixloops/scripts/adopt_candidate.py \
     --candidates <candidates.json> \
     --candidate-id <candidate-id> \
     --mode "<mode>" \
     --out-dir <adoption-dir>
   ```

4. Run one bounded cycle.
   - Read state first.
   - Select at most 1-3 active items.
   - Act only inside the approved mode.
   - Verify with the listed verifier.
   - Update state before stopping.

5. Return status.
   - `DONE`: acceptance checks passed with evidence.
   - `CONTINUE`: another cycle can improve verified certainty and budget
     remains.
   - review-needed: human judgment or explicit approval is required.
   - `BLOCKED`: reliable progress is not possible with current evidence.
   - `BUDGET_STOPPED`: item, iteration, time, token, or cost cap was reached.

## Never Do Silently

- Install `AGENTS-snippet.md` into project instructions.
- Push, merge, deploy, migrate, delete data, change credentials, alter billing,
  or call production APIs.
- Expand scope beyond the selected candidate and approved mode.
