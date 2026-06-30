---
name: sixloops-design
description: Use when the user gives a current development goal and asks to design a bounded agent loop, team loop, or subagent workflow, or to decide whether it should shrink to a skill or checklist.
---

# SixLoops Design

Turn a current objective into the smallest useful reusable mechanism. Recommend
a managed loop only when the agent can observe, decide, act, verify, preserve
state, and stop without repeated user prompting.

## Workflow

1. Read `../sixloops/references/design-managed-loop.md`.
2. Test whether the goal is actually loop-shaped: recurring work, observable
   inputs, objective rejection signal, bounded actions, hard stop, and human
   gate for high-impact actions.
3. Run `../sixloops/scripts/design_goal_loop.py --goal "<goal>" --domain auto --team-mode auto --level auto --out-dir .sixloops/goal-design`
   only when an artifact packet is useful.
4. Present the start plan before internals: why the user would start it, first
   cycle, verifier, stop/review boundary, selected mode, and artifact paths.

## Downgrade When

- The goal is one-shot.
- The verifier cannot reject bad output.
- The work is mostly product judgment.
- A rule, skill, checklist, or approval gate is the safer first step.
