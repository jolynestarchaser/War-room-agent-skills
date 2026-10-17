# War Room Report Contract

## Contents

1. [Summary](#summary)
2. [Per-ticket template](#per-ticket-template)
3. [Quality gates](#quality-gates)

## Summary

Produce the report in `report_language` from `config.md` (default Thai) with English technical names, in this order:

**WAR ROOM / [date and timezone]**

- Mode and input (e.g. `triage`, ticket key, `deep`), Jira authenticated identity if verified, actual JQL used, issue count/selected count, pagination/truncation status.
- Setup: the Step 0 result line per check (`OK / FIXED / WARNING / MISSING`), including codebase map date and any stale repos.
- Environment: Jira connector status; number of authorized repositories checked; whether custom subagents actually ran; existing Skills actually loaded; whether original Ariyasacca reference was read.
- Table: `Ticket | Priority | Current status | Primary repo | Other repos | Size | Confidence | Readiness | Next action`.
- Cross-ticket dependencies, shared repos, capacity/sequence concerns, blockers and recommended ordering. Note if only a subset was deeply investigated.

## Per-ticket template

### [KEY] — [Summary] — [link]

- **Facts:** type, priority, Jira status, acceptance criteria, explicit dependencies; distinguish `Observed / Inferred / Unknown`.
- **Problem definition:** expected vs actual outcome or requested change.
- **Repositories:** list `Repo (role; confidence; evidence URL or file:line; open questions)`; if none verified, say `Unknown`.
- **Investigation:** inspected paths, relevant symbols/contracts, reproduction or code trace if safely observed; alternative causes; evidence gaps.
- **Ariyasacca/Buddhist method:** `Original reference read at [path]` or `Not available`; briefly report how observed facts and hypotheses were differentiated. Do not cite the missing reference as evidence.
- **Options:** at least two when nontrivial, with expected effects, constraints, risks and trade-offs; recommend one if confidence supports it.
- **Complexity:** dimension scores `scope / uncertainty / integration / risk / verification`, total and S/M/L/XL, confidence, reasoning. Use `Unscored` if evidence insufficient.
- **Proposed plan:** ordered per-repo subtasks with dependencies, acceptance tests, rollout/rollback needs; **no changes executed**.
- **Decision gate:** `READY TO PLAN | NEEDS DISCOVERY | NEEDS CLARIFICATION | BLOCKED`; one next action, owner/question if needed.
- **Sources:** Jira issue, PR/ADR/docs, repository path:lines; source gaps explicit.

For large result sets, give compact per-ticket triage rows first; expand only user-selected/high priority/uncertain tickets in detail. Do not imply uninspected tickets were fully analyzed.

## Quality gates

- All claims about a repo, file or root cause have an identifiable evidence source or are explicitly `Hypothesis`.
- All Jira items shown actually came from the connected source.
- All repository/tool coverage limitations are visible.
- Sizes and confidence are justified and reproducible with the rubric.
- No implementation action or Jira modification occurred.
- If a gate fails, return to the necessary step or report why it cannot be resolved.
