# Design Managed Loop

Use this workflow when the user gives a current objective and asks to design a
loop, team loop, or subagent workflow.

## Goal

Turn the user's current objective into a bounded loop plan that can run after
one explicit approval, or downgrade it to a skill/checklist when delegation is
not justified.

## Workflow

1. Read `goal-loop-designer.md`.
2. Decide whether the goal is loop-shaped:
   - continued or recurring work,
   - observable inputs,
   - objective rejection signal,
   - bounded actions,
   - hard iteration cap,
   - human gate for high-impact work.
3. Run the direct goal script when an artifact packet is useful:

   ```bash
   python skills/sixloops/scripts/design_goal_loop.py \
     --goal "<user goal>" \
     --domain auto \
     --team-mode auto \
     --level auto \
     --out-dir .sixloops/goal-design
   ```

4. Read generated `GOAL.md`, `STATE.json`, `RUN.md`, `VERIFY.md`, `TEAM.md`,
   `HANDOFF.md`, and `goal-loop-design.json`.
5. Present the start plan first:
   - why the user would start it,
   - first cycle,
   - verifier,
   - stop/review boundary,
   - selected mode,
   - generated artifact paths.

## Team Policy

Use team roles only when separation improves planning, implementation, review,
or verification. Spawn maker roles only inside explicit edit scope. If subagent
tools are unavailable, run the same roles sequentially and keep `TEAM.md` as a
handoff prompt.

## Downgrade When

- The goal is one-shot and not worth state.
- The verifier cannot reject bad output.
- The work is mostly product judgment.
- The safe next step is a rule, skill, checklist, or approval gate.
