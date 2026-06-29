#!/usr/bin/env python3
"""Public entrypoint for the SixLoops local pipeline."""

from __future__ import annotations

import subprocess

from sixloops.pipeline.sixloops import main


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except subprocess.CalledProcessError as exc:
        raise SystemExit(exc.returncode)
