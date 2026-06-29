#!/usr/bin/env bash
set -euo pipefail

target="${1:-both}"
scope="${2:-user}"
project_path="${3:-$PWD}"

repo_root="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
source_dir="$repo_root/skills/session-to-loop"

if [[ ! -d "$source_dir" ]]; then
  echo "Skill source not found: $source_dir" >&2
  exit 1
fi

copy_skill() {
  local destination_root="$1"
  local destination="$destination_root/session-to-loop"
  mkdir -p "$destination"
  cp -R "$source_dir"/. "$destination"/
  echo "Installed session-to-loop -> $destination"
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
