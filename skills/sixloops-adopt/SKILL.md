---
name: sixloops-adopt
description: Use when the user replies start, continue, run, adopt, shrink, or reject for an existing SixLoops candidate, or asks to execute one controlled loop cycle.
---

# SixLoops Adopt

Run one controlled cycle of an existing SixLoops candidate, or shrink/reject it
without pretending the candidate is ready for automation.

## Workflow

1. Read `../sixloops/references/adopt-loop-runbook.md`.
2. Identify the selected candidate and mode from the user's exact reply string.
3. Read the latest card or adoption packet. Create one with
   `../sixloops/scripts/adopt_candidate.py` only when stateful reuse is needed.
4. Run at most one bounded cycle inside the approved mode.
5. Update state and return exactly one status: `DONE`, `CONTINUE`,
   review-needed, `BLOCKED`, or `BUDGET_STOPPED`.

## Never Do Silently

- Install generated project instructions.
- Push, merge, deploy, migrate, delete data, change credentials, alter billing,
  or call production APIs.
- Expand scope beyond the selected candidate and approved mode.
