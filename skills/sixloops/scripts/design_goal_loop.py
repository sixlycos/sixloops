#!/usr/bin/env python3
"""Compatibility entrypoint for direct goal-loop design."""

from __future__ import annotations

import sys

from sixloops.goals.design_goal_loop import main


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except Exception as exc:
        print(f"design_goal_loop.py: {exc}", file=sys.stderr)
        raise SystemExit(1)
