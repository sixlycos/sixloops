#!/usr/bin/env python3
"""Compatibility entrypoint for analysis scope preparation."""

from __future__ import annotations

import sys

from sixloops.pipeline.prepare_analysis_scope import main


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except Exception as exc:
        print(f"prepare_analysis_scope.py: {exc}", file=sys.stderr)
        raise SystemExit(1)
