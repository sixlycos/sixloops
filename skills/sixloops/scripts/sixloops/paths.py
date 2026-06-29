"""Stable paths for the installed SixLoops skill package."""

from __future__ import annotations

from pathlib import Path


PACKAGE_DIR = Path(__file__).resolve().parent
SCRIPT_DIR = PACKAGE_DIR.parent
SKILL_DIR = SCRIPT_DIR.parent
REFERENCES_DIR = SKILL_DIR / "references"
SCHEMAS_DIR = SKILL_DIR / "schemas"
TEMPLATE_DIR = SKILL_DIR / "assets" / "templates"
