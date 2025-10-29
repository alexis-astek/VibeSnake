# VibeSnake

A small GitHub Pages web app with an agent-driven CI flow.

## Overview
- Deployed via GitHub Pages.
- Bugs tracked in `BUGS.md` with fields: Status, Versions, FixVersions.
- Versioning file: `VERSION` holds integer N for last released version (V.N).
- Lightweight pipeline state: `PIPELINE_STATE.json` coordinates turn-taking between agents.

## Agents
- UI Tester (`uiTesterAgent/agent.py`)
  - Reads `PAGES_URL`, `VERSION`, `PIPELINE_STATE.json`.
  - Appends issues to `BUGS.md` with `Versions` and `Status: Open`.
  - Sets `PIPELINE_STATE.json.next = "dev"` when done.
- Dev (`devAgent/agent.py`)
  - Fixes all Open items, sets `Status: Resolved`, checks items.
  - Maintains this README when behavior changes.
  - Sets `PIPELINE_STATE.json.next = "cicd"` when done.
- CICD (`cicdAgent/agent.py`)
  - Reads `VERSION`, increments to next; prefixes commit with `V.<next>`.
  - Converts Resolved → Released in `BUGS.md`, appends `V.<next>` to `FixVersions`.
  - Sets `PIPELINE_STATE.json.next = "uiTester"` when done.

## Run Sequence (PowerShell)
1. `$env:PAGES_URL = "https://<user>.github.io/<repo>/"`
2. `adk run uiTesterAgent/agent.py:root_agent`
3. `adk run devAgent/agent.py:root_agent`
4. `adk run cicdAgent/agent.py:root_agent`

Ensure git auth is configured for pushes.

## Versioning
- `VERSION` value N means the latest release is `V.N`.
- CICD increments to `N+1` during its commit.

## Bug semantics
- Regression: implied when a bug reappears in a later `V.*` and `Versions` contains multiple entries.
- `Status`: Open → Resolved (Dev) → Released (CICD).

## Maintenance (Dev Agent)
- Keep this README accurate after feature or behavior changes.
