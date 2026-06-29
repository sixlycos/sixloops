#!/usr/bin/env python3
"""Compatibility entrypoint for transcript discovery."""

from __future__ import annotations

import sys

from sixloops.pipeline.discover_claude_sessions import main


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except Exception as exc:
        print(f"discover_claude_sessions.py: {exc}", file=sys.stderr)
        raise SystemExit(1)
