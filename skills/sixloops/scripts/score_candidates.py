#!/usr/bin/env python3
"""Compatibility entrypoint for fallback candidate scoring."""

from __future__ import annotations

import sys

from sixloops.pipeline.score_candidates import main


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except Exception as exc:
        print(f"score_candidates.py: {exc}", file=sys.stderr)
        raise SystemExit(1)
