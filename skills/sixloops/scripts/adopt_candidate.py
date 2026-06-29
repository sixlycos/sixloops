#!/usr/bin/env python3
"""Compatibility entrypoint for candidate adoption packet generation."""

from __future__ import annotations

import sys

from sixloops.goals.adopt_candidate import main


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except Exception as exc:
        print(f"adopt_candidate.py: {exc}", file=sys.stderr)
        raise SystemExit(1)
