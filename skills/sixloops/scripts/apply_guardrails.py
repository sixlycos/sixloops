#!/usr/bin/env python3
"""Compatibility entrypoint for candidate guardrails."""

from __future__ import annotations

import sys

from sixloops.pipeline.apply_guardrails import main


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except Exception as exc:
        print(f"apply_guardrails.py: {exc}", file=sys.stderr)
        raise SystemExit(1)
