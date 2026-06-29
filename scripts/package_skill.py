#!/usr/bin/env python3
"""Package the SixLoops skill folder as a release zip."""

from __future__ import annotations

import argparse
import shutil
import zipfile
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
DEFAULT_SOURCE = REPO_ROOT / "skills" / "session-to-loop"
DEFAULT_OUT = REPO_ROOT / "dist" / "sixloops-skill.zip"


def should_skip(path: Path) -> bool:
    parts = set(path.parts)
    return "__pycache__" in parts or path.suffix in {".pyc", ".pyo"}


def package_skill(source: Path, out: Path) -> None:
    if not source.exists():
        raise FileNotFoundError(f"Skill source not found: {source}")
    if out.exists():
        out.unlink()
    out.parent.mkdir(parents=True, exist_ok=True)

    with zipfile.ZipFile(out, "w", compression=zipfile.ZIP_DEFLATED) as archive:
        for path in sorted(source.rglob("*")):
            if path.is_dir() or should_skip(path):
                continue
            archive.write(path, Path("session-to-loop") / path.relative_to(source))


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Package the SixLoops skill folder as a release zip.")
    parser.add_argument("--source", default=str(DEFAULT_SOURCE), help=f"Skill folder. Default: {DEFAULT_SOURCE}")
    parser.add_argument("--out", default=str(DEFAULT_OUT), help=f"Output zip. Default: {DEFAULT_OUT}")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    source = Path(args.source)
    out = Path(args.out)
    package_skill(source, out)
    size = out.stat().st_size
    print(f"Packaged {source} -> {out} ({size} bytes)")
    if shutil.which("python"):
        print("Install by unzipping this archive into ~/.agents/skills or ~/.claude/skills.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
