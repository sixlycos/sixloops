#!/usr/bin/env python3
"""Compatibility entrypoint for transcript redaction."""

from __future__ import annotations

import sys

from sixloops.pipeline.redact_transcripts import main


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except Exception as exc:
        print(f"redact_transcripts.py: {exc}", file=sys.stderr)
        raise SystemExit(1)
