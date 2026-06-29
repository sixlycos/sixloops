# Draft AGENTS.md Snippet: CI Babysitter Loop

This is a draft rule. Do not install it automatically; review it before copying into project instructions.

When `ci-babysitter` is triggered:

- Run level: `goal-loop`.
- Goal: Keep CI failures moving toward a verified fix without guessing.
- Read and update the loop state before stopping.
- Handle at most 3 item(s) per cycle.
- Stop after 8 iteration(s), repeated failure, no progress, or a human gate.
- Verify with: Run the focused project checks listed in verification..
- Ask before: push, merge.
