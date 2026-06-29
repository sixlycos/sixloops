#!/usr/bin/env python3
"""Compatibility entrypoint for artifact rendering."""

from __future__ import annotations

import sys

from sixloops.pipeline.render_artifacts import main


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except Exception as exc:
        print(f"render_artifacts.py: {exc}", file=sys.stderr)
        raise SystemExit(1)
