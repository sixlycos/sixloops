#!/usr/bin/env python3
"""Run minimal SixLoops skill-collection structure checks."""

from __future__ import annotations

import re
import subprocess
import sys
import zipfile
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
SKILLS = {
    "sixloops": ("router",),
    "sixloops-mine": ("mine", "log", "session"),
    "sixloops-design": ("design", "goal"),
    "sixloops-adopt": ("adopt", "start", "continue"),
}


def description(text: str) -> str:
    match = re.search(r"^description:\s*(.+)$", text, re.MULTILINE)
    return match.group(1).strip() if match else ""


def main() -> int:
    failures: list[str] = []
    for name, terms in SKILLS.items():
        path = REPO_ROOT / "skills" / name / "SKILL.md"
        if not path.exists():
            failures.append(f"missing {path.relative_to(REPO_ROOT)}")
            continue
        desc = description(path.read_text(encoding="utf-8"))
        lowered = desc.lower()
        if not desc:
            failures.append(f"{name} missing description")
        if not any(term in lowered for term in terms):
            failures.append(f"{name} description missing route term from {terms}")

    for script in ("scripts/install.sh", "scripts/install.ps1", "scripts/package_skill.py"):
        text = (REPO_ROOT / script).read_text(encoding="utf-8")
        for name in SKILLS:
            if name not in text:
                failures.append(f"{script} does not mention {name}")

    out = REPO_ROOT / ".sixloops" / "tmp" / "skill-collection-eval.zip"
    result = subprocess.run(
        [sys.executable, "scripts/package_skill.py", "--out", str(out)],
        cwd=str(REPO_ROOT),
        capture_output=True,
        text=True,
    )
    if result.returncode:
        failures.append(result.stderr.strip() or result.stdout.strip() or "package_skill.py failed")
    elif out.exists():
        with zipfile.ZipFile(out) as archive:
            roots = {Path(name).parts[0] for name in archive.namelist() if Path(name).parts}
        missing = sorted(set(SKILLS) - roots)
        if missing:
            failures.append(f"package zip missing skills: {missing}")
    else:
        failures.append("package zip was not created")

    for failure in failures:
        print(f"FAIL {failure}")
    if failures:
        return 1
    print("PASS skill collection")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
