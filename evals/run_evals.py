#!/usr/bin/env python3
"""Run deterministic SixLoops fixture evals."""

from __future__ import annotations

import argparse
import json
import shutil
import subprocess
import sys
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
DEFAULT_EVALS = REPO_ROOT / "evals" / "evals.json"
DEFAULT_OUT_ROOT = REPO_ROOT / ".session-to-loop" / "tmp" / "evals"
PIPELINE = REPO_ROOT / "skills" / "session-to-loop" / "scripts" / "session_to_loop.py"


def load_json(path: Path) -> object:
    return json.loads(path.read_text(encoding="utf-8"))


def read_packets(path: Path) -> list[dict]:
    packets = []
    if not path.exists():
        return packets
    with path.open("r", encoding="utf-8") as handle:
        for line in handle:
            stripped = line.strip()
            if stripped:
                packets.append(json.loads(stripped))
    return packets


def ensure_safe_child(path: Path, root: Path) -> None:
    resolved = path.resolve()
    resolved_root = root.resolve()
    if resolved != resolved_root and resolved_root not in resolved.parents:
        raise ValueError(f"Refusing to clean path outside eval root: {path}")


def clean_case_dir(path: Path, root: Path) -> None:
    ensure_safe_child(path, root)
    if path.exists():
        shutil.rmtree(path)
    path.mkdir(parents=True, exist_ok=True)


def all_public_text(public_dir: Path) -> str:
    if not public_dir.exists():
        return ""
    chunks = []
    for path in public_dir.rglob("*"):
        if path.is_file():
            try:
                chunks.append(path.read_text(encoding="utf-8", errors="ignore"))
            except OSError:
                continue
    return "\n".join(chunks)


def candidate_mechanisms(candidates: list[dict]) -> set[str]:
    mechanisms: set[str] = set()
    for candidate in candidates:
        mechanisms.update(str(item) for item in candidate.get("mechanisms", []))
    return mechanisms


def candidate_approvals(candidates: list[dict]) -> set[str]:
    approvals: set[str] = set()
    for candidate in candidates:
        safety = candidate.get("safety") if isinstance(candidate.get("safety"), dict) else {}
        approvals.update(str(item) for item in safety.get("requires_approval_for", []))
    return approvals


def assert_case(case: dict, case_dir: Path) -> list[str]:
    failures: list[str] = []
    expected = case.get("expected", {})
    private = case_dir / "private"
    public = case_dir / "public"
    candidates_path = private / "candidates.json"
    packet_index_path = private / "analysis-packets-index.json"
    packets_path = private / "analysis-packets.jsonl"

    if not candidates_path.exists():
        return [f"missing candidates output: {candidates_path}"]
    if not packet_index_path.exists():
        return [f"missing packet index output: {packet_index_path}"]

    candidates_data = load_json(candidates_path)
    packet_index = load_json(packet_index_path)
    packets = read_packets(packets_path)
    candidates = candidates_data.get("candidates", []) if isinstance(candidates_data, dict) else []
    ids = {str(item.get("id")) for item in candidates}
    mechanisms = candidate_mechanisms(candidates)
    decisions = {str(item.get("decision")) for item in candidates}
    approvals = candidate_approvals(candidates)
    roles = {str(packet.get("role")) for packet in packets}
    session_ids = {str(packet.get("session_id")) for packet in packets}
    provider_counts = packet_index.get("provider_counts", {}) or packet_index.get("source", {}).get("providers", {})
    source_types = packet_index.get("source", {}).get("source_types", {})

    for candidate_id in expected.get("include_candidates", []):
        if candidate_id not in ids:
            failures.append(f"expected candidate {candidate_id!r}, got {sorted(ids)}")

    for mechanism in expected.get("include_mechanisms", []):
        if mechanism not in mechanisms:
            failures.append(f"expected mechanism {mechanism!r}, got {sorted(mechanisms)}")

    for mechanism in expected.get("exclude_mechanisms", []):
        if mechanism in mechanisms:
            failures.append(f"excluded mechanism {mechanism!r} was present")

    decision = expected.get("include_decision")
    if decision and decision not in decisions:
        failures.append(f"expected decision {decision!r}, got {sorted(decisions)}")

    for excluded in expected.get("exclude_decisions", []):
        if excluded in decisions:
            failures.append(f"excluded decision {excluded!r} was present")

    provider = expected.get("require_packet_provider")
    if provider and int(provider_counts.get(provider, 0)) <= 0:
        failures.append(f"expected packet provider {provider!r}, got {provider_counts}")

    source_type = expected.get("require_source_type")
    if source_type and int(source_types.get(source_type, 0)) <= 0:
        failures.append(f"expected source type {source_type!r}, got {source_types}")

    for role in expected.get("require_packet_roles", []):
        if role not in roles:
            failures.append(f"expected packet role {role!r}, got {sorted(roles)}")

    for session_id in expected.get("require_session_ids", []):
        if session_id not in session_ids:
            failures.append(f"expected session id {session_id!r}, got {sorted(session_ids)}")

    for approval in expected.get("require_approval_for", []):
        if approval not in approvals:
            failures.append(f"expected approval boundary {approval!r}, got {sorted(approvals)}")

    if expected.get("redaction_required") and not packet_index.get("redaction", {}).get("enabled"):
        failures.append("expected redaction to be enabled")

    public_text = all_public_text(public)
    for forbidden in expected.get("must_not_include", []):
        if forbidden in public_text:
            failures.append(f"forbidden text leaked into public artifacts: {forbidden!r}")
    if "{{" in public_text or "}}" in public_text:
        failures.append("unrendered template placeholder found in public artifacts")

    return failures


def run_case(case: dict, out_root: Path, keep_going: bool) -> tuple[bool, list[str]]:
    case_dir = out_root / str(case["id"])
    clean_case_dir(case_dir, out_root)
    cmd = [
        sys.executable,
        str(PIPELINE),
        "--input",
        str(REPO_ROOT / case["fixture"]),
        "--out-root",
        str(case_dir),
        "--approve",
        "--rule-fallback",
    ]
    result = subprocess.run(cmd, cwd=str(REPO_ROOT), capture_output=True, text=True)
    if result.returncode != 0:
        details = [f"pipeline exited {result.returncode}"]
        if result.stdout.strip():
            details.append(result.stdout.strip())
        if result.stderr.strip():
            details.append(result.stderr.strip())
        if not keep_going:
            return False, details
        return False, details

    failures = assert_case(case, case_dir)
    return not failures, failures


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Run SixLoops synthetic eval fixtures.")
    parser.add_argument("--evals", default=str(DEFAULT_EVALS), help=f"Eval spec JSON. Default: {DEFAULT_EVALS}")
    parser.add_argument("--out-root", default=str(DEFAULT_OUT_ROOT), help=f"Output root. Default: {DEFAULT_OUT_ROOT}")
    parser.add_argument("--case", action="append", default=[], help="Run only this case id. Can be repeated.")
    parser.add_argument("--keep-going", action="store_true", help="Run all selected cases even after a failure.")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    evals = load_json(Path(args.evals))
    if not isinstance(evals, list):
        raise ValueError("evals spec must be a list.")
    selected = [case for case in evals if not args.case or case.get("id") in set(args.case)]
    if not selected:
        raise ValueError("No eval cases selected.")

    out_root = Path(args.out_root)
    out_root.mkdir(parents=True, exist_ok=True)

    failed = 0
    ran = 0
    for case in selected:
        ran += 1
        ok, details = run_case(case, out_root, args.keep_going)
        if ok:
            print(f"PASS {case['id']}")
            continue
        failed += 1
        print(f"FAIL {case['id']}")
        for detail in details:
            print(f"  - {detail}")
        if not args.keep_going:
            break

    passed = ran - failed
    print(f"{passed}/{ran} eval(s) passed.")
    return 1 if failed else 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except Exception as exc:
        print(f"run_evals.py: {exc}", file=sys.stderr)
        raise SystemExit(1)
