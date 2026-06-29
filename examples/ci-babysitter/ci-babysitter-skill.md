---
name: ci-babysitter
description: Repeated user requests to inspect CI logs before patching and to avoid pushing before verification.
---

# CI Babysitter Loop

## Overview

Repeated user requests to inspect CI logs before patching and to avoid pushing before verification.

## Workflow

1. Check CI status.
2. Read failed job logs.
3. Patch only evidenced failures.

## Inputs

- CI status
- failed job logs
- git diff

## Verification

- Verifier: Relevant local test passes.
- CI becomes green or is clearly blocked.
- PASS evidence: command output, status result, screenshot, schema result, or explicit checker note.
- Stop policy: stop when verification passes, the same failure repeats, evidence stops changing, or human approval is required.

## Safety

- push
- merge
