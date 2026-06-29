#!/usr/bin/env bash
set -euo pipefail

target="${1:-both}"
scope="${2:-user}"
project_path="${3:-$PWD}"

repo_root="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
source_dir="$repo_root/skills/sixloops"

if [[ ! -d "$source_dir" ]]; then
  echo "Skill source not found: $source_dir" >&2
  exit 1
fi

copy_skill() {
  local destination_root="$1"
  destination_root="${destination_root%/}"
  if [[ -z "$destination_root" ]]; then
    echo "Refusing to install into an empty destination root." >&2
    exit 1
  fi

  local destination="$destination_root/sixloops"
  local destination_parent
  destination_parent="$(dirname "$destination")"
  if [[ "$destination_parent" != "$destination_root" || "$(basename "$destination")" != "sixloops" ]]; then
    echo "Refusing to install outside destination root: $destination" >&2
    exit 1
  fi

  mkdir -p "$destination_root"
  rm -rf -- "$destination"
  mkdir -p "$destination"
  cp -R "$source_dir"/. "$destination"/
  find "$destination" -type d -name '__pycache__' -prune -exec rm -rf {} +
  find "$destination" -type f \( -name '*.pyc' -o -name '*.pyo' \) -delete
  echo "Installed sixloops -> $destination"
}

install_codex() {
  if [[ "$scope" == "project" ]]; then
    local root="$project_path/.agents/skills"
    copy_skill "$root"
    echo "Codex project install uses the Agent Skills project folder: $root"
    return
  fi

  copy_skill "$HOME/.agents/skills"
}

install_claude() {
  if [[ "$scope" == "project" ]]; then
    copy_skill "$project_path/.claude/skills"
    return
  fi

  copy_skill "$HOME/.claude/skills"
}

case "$target" in
  codex)
    install_codex
    ;;
  claude)
    install_claude
    ;;
  both)
    install_codex
    install_claude
    ;;
  *)
    echo "Usage: $0 [codex|claude|both] [user|project] [project_path]" >&2
    exit 1
    ;;
esac

echo "Done. Start a new Codex or Claude Code session so the skill index refreshes."
