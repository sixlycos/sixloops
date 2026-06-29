#!/usr/bin/env python3
"""Compatibility entrypoint for analysis packet building."""

from __future__ import annotations

import sys

from sixloops.pipeline.build_analysis_packets import main


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except Exception as exc:
        print(f"build_analysis_packets.py: {exc}", file=sys.stderr)
        raise SystemExit(1)
