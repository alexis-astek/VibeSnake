# Bug Backlog

## [Template] UI Test Run
- [ ] <Severity:P0|P1|P2> <Short title>
  - Status: <Open|Resolved|Released>
  - Area: <page/feature>
  - Versions: [V.N, ...]  
    Current run version where this bug is observed must be appended.
  - FixVersions: [V.M, ...]
  - Steps: <steps to reproduce>
  - Expected: <expected behavior>
  - Actual: <actual behavior/error>
  - Evidence: <link/screenshot/console excerpt if available>

Guidance:
- Mark as regression if the bug (same title/area) appears again in a later version.
- A regression is implied when `Versions` contains multiple distinct versions.
- Dev agent sets Status to "Resolved" after implementing a fix; CICD sets it to "Released" and appends the release version to `FixVersions`.

---

> The UI Tester Agent will append dated runs below.
