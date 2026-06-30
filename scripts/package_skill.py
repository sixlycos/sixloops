#!/usr/bin/env python3
"""Package the SixLoops skill collection as a release zip."""

from __future__ import annotations

import argparse
import shutil
import zipfile
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
DEFAULT_SOURCE_ROOT = REPO_ROOT / "skills"
DEFAULT_OUT = REPO_ROOT / "dist" / "sixloops-skill.zip"
SKILL_NAMES = ("sixloops", "sixloops-mine", "sixloops-design", "sixloops-adopt")


def should_skip(path: Path) -> bool:
    parts = set(path.parts)
    return "__pycache__" in parts or path.suffix in {".pyc", ".pyo"}


def package_skill_collection(source_root: Path, out: Path) -> None:
    missing = [name for name in SKILL_NAMES if not (source_root / name).exists()]
    if missing:
        raise FileNotFoundError(f"Skill source(s) not found: {', '.join(missing)}")
    if out.exists():
        out.unlink()
    out.parent.mkdir(parents=True, exist_ok=True)

    with zipfile.ZipFile(out, "w", compression=zipfile.ZIP_DEFLATED) as archive:
        for name in SKILL_NAMES:
            source = source_root / name
            for path in sorted(source.rglob("*")):
                if path.is_dir() or should_skip(path):
                    continue
                archive.write(path, Path(name) / path.relative_to(source))


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Package the SixLoops skill collection as a release zip.")
    parser.add_argument("--source-root", default=str(DEFAULT_SOURCE_ROOT), help=f"Skills folder. Default: {DEFAULT_SOURCE_ROOT}")
    parser.add_argument("--out", default=str(DEFAULT_OUT), help=f"Output zip. Default: {DEFAULT_OUT}")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    source = Path(args.source_root)
    out = Path(args.out)
    package_skill_collection(source, out)
    size = out.stat().st_size
    print(f"Packaged {source} -> {out} ({size} bytes)")
    if shutil.which("python"):
        print("Install by unzipping this archive into ~/.agents/skills or ~/.claude/skills.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
