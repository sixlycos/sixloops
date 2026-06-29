param(
  [ValidateSet("codex", "claude", "both")]
  [string]$Target = "both",

  [ValidateSet("user", "project")]
  [string]$Scope = "user",

  [string]$ProjectPath = (Get-Location).Path
)

$ErrorActionPreference = "Stop"

$RepoRoot = Split-Path -Parent $PSScriptRoot
$Source = Join-Path $RepoRoot "skills\session-to-loop"

if (!(Test-Path $Source)) {
  throw "Skill source not found: $Source"
}

function Copy-SixLoopsSkill {
  param([string]$DestinationRoot)

  $Destination = Join-Path $DestinationRoot "session-to-loop"
  New-Item -ItemType Directory -Force -Path $Destination | Out-Null
  Copy-Item -Path (Join-Path $Source "*") -Destination $Destination -Recurse -Force
  Write-Output "Installed session-to-loop -> $Destination"
}

function Install-Codex {
  if ($Scope -eq "project") {
    $root = Join-Path $ProjectPath ".agents\skills"
    Copy-SixLoopsSkill $root
    Write-Output "Codex project install uses the Agent Skills project folder: $root"
    return
  }

  Copy-SixLoopsSkill (Join-Path $env:USERPROFILE ".agents\skills")
}

function Install-Claude {
  if ($Scope -eq "project") {
    Copy-SixLoopsSkill (Join-Path $ProjectPath ".claude\skills")
    return
  }

  Copy-SixLoopsSkill (Join-Path $env:USERPROFILE ".claude\skills")
}

if ($Target -eq "codex" -or $Target -eq "both") {
  Install-Codex
}

if ($Target -eq "claude" -or $Target -eq "both") {
  Install-Claude
}

Write-Output "Done. Start a new Codex or Claude Code session so the skill index refreshes."
