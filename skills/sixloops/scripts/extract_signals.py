#!/usr/bin/env python3
"""Compatibility entrypoint for fallback signal extraction."""

from __future__ import annotations

import sys

from sixloops.pipeline.extract_signals import main


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except Exception as exc:
        print(f"extract_signals.py: {exc}", file=sys.stderr)
        raise SystemExit(1)
