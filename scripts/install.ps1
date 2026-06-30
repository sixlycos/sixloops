param(
  [ValidateSet("codex", "claude", "both")]
  [string]$Target = "both",

  [ValidateSet("user", "project")]
  [string]$Scope = "user",

  [string]$ProjectPath = (Get-Location).Path
)

$ErrorActionPreference = "Stop"

$RepoRoot = Split-Path -Parent $PSScriptRoot
$SkillsRoot = Join-Path $RepoRoot "skills"
$SkillNames = @("sixloops", "sixloops-mine", "sixloops-design", "sixloops-adopt")

foreach ($SkillName in $SkillNames) {
  $Source = Join-Path $SkillsRoot $SkillName
  if (!(Test-Path $Source)) {
    throw "Skill source not found: $Source"
  }
}

function Copy-SixLoopsSkill {
  param([string]$DestinationRoot, [string]$SkillName)

  $Source = Join-Path $SkillsRoot $SkillName
  $DestinationRootFull = [System.IO.Path]::GetFullPath($DestinationRoot)
  $Destination = Join-Path $DestinationRootFull $SkillName
  $DestinationFull = [System.IO.Path]::GetFullPath($Destination)
  $DestinationParent = [System.IO.Path]::GetFullPath((Split-Path -Parent $DestinationFull)).TrimEnd([System.IO.Path]::DirectorySeparatorChar, [System.IO.Path]::AltDirectorySeparatorChar)
  $ExpectedParent = $DestinationRootFull.TrimEnd([System.IO.Path]::DirectorySeparatorChar, [System.IO.Path]::AltDirectorySeparatorChar)

  if ($DestinationParent -ine $ExpectedParent) {
    throw "Refusing to install outside destination root: $DestinationFull"
  }

  New-Item -ItemType Directory -Force -Path $DestinationRootFull | Out-Null
  if (Test-Path -LiteralPath $DestinationFull) {
    Remove-Item -LiteralPath $DestinationFull -Recurse -Force
  }
  New-Item -ItemType Directory -Force -Path $DestinationFull | Out-Null
  Copy-Item -Path (Join-Path $Source "*") -Destination $DestinationFull -Recurse -Force
  Get-ChildItem -LiteralPath $DestinationFull -Directory -Recurse -Filter "__pycache__" -ErrorAction SilentlyContinue |
    Remove-Item -Recurse -Force
  Get-ChildItem -LiteralPath $DestinationFull -File -Recurse -ErrorAction SilentlyContinue |
    Where-Object { $_.Extension -in ".pyc", ".pyo" } |
    Remove-Item -Force
  Write-Output "Installed $SkillName -> $DestinationFull"
}

function Copy-SixLoopsCollection {
  param([string]$DestinationRoot)
  foreach ($SkillName in $SkillNames) {
    Copy-SixLoopsSkill $DestinationRoot $SkillName
  }
}

function Install-Codex {
  if ($Scope -eq "project") {
    $root = Join-Path $ProjectPath ".agents\skills"
    Copy-SixLoopsCollection $root
    Write-Output "Codex project install uses the Agent Skills project folder: $root"
    return
  }

  Copy-SixLoopsCollection (Join-Path $env:USERPROFILE ".agents\skills")
}

function Install-Claude {
  if ($Scope -eq "project") {
    Copy-SixLoopsCollection (Join-Path $ProjectPath ".claude\skills")
    return
  }

  Copy-SixLoopsCollection (Join-Path $env:USERPROFILE ".claude\skills")
}

if ($Target -eq "codex" -or $Target -eq "both") {
  Install-Codex
}

if ($Target -eq "claude" -or $Target -eq "both") {
  Install-Claude
}

Write-Output "Done. Start a new Codex or Claude Code session so the skill index refreshes."
