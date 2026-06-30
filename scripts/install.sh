#!/usr/bin/env bash
set -euo pipefail

target="${1:-both}"
scope="${2:-user}"
project_path="${3:-$PWD}"

repo_root="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
skills_root="$repo_root/skills"
skill_names=(sixloops sixloops-mine sixloops-design sixloops-adopt)

for skill_name in "${skill_names[@]}"; do
  if [[ ! -d "$skills_root/$skill_name" ]]; then
    echo "Skill source not found: $skills_root/$skill_name" >&2
    exit 1
  fi
done

copy_skill() {
  local destination_root="$1"
  local skill_name="$2"
  local source_dir="$skills_root/$skill_name"
  destination_root="${destination_root%/}"
  if [[ -z "$destination_root" ]]; then
    echo "Refusing to install into an empty destination root." >&2
    exit 1
  fi

  local destination="$destination_root/$skill_name"
  local destination_parent
  destination_parent="$(dirname "$destination")"
  if [[ "$destination_parent" != "$destination_root" || "$(basename "$destination")" != "$skill_name" ]]; then
    echo "Refusing to install outside destination root: $destination" >&2
    exit 1
  fi

  mkdir -p "$destination_root"
  rm -rf -- "$destination"
  mkdir -p "$destination"
  cp -R "$source_dir"/. "$destination"/
  find "$destination" -type d -name '__pycache__' -prune -exec rm -rf {} +
  find "$destination" -type f \( -name '*.pyc' -o -name '*.pyo' \) -delete
  echo "Installed $skill_name -> $destination"
}

copy_collection() {
  local destination_root="$1"
  for skill_name in "${skill_names[@]}"; do
    copy_skill "$destination_root" "$skill_name"
  done
}

install_codex() {
  if [[ "$scope" == "project" ]]; then
    local root="$project_path/.agents/skills"
    copy_collection "$root"
    echo "Codex project install uses the Agent Skills project folder: $root"
    return
  fi

  copy_collection "$HOME/.agents/skills"
}

install_claude() {
  if [[ "$scope" == "project" ]]; then
    copy_collection "$project_path/.claude/skills"
    return
  fi

  copy_collection "$HOME/.claude/skills"
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
