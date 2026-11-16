# Spec File (`tickets/<KEY>/spec.md`)

The spec is the **hand-off**: everything a fresh chat, an implementer or a reviewer needs, so none of them depends on this conversation. It points at sources (Jira link, codebase map sections, file paths) rather than copying them. Write it in English; quote Jira text in its original language.

## Status lifecycle

`approved` (step 11) → `implementing` (implement.md, branch prep done) → `in-review` (senior review passed, waiting for the human) → `delivered` (delivery.md, after commit decision and PR drafts).

Change the `Status` line and append one line to `## Log` at every transition. A delivery mode refuses a spec that is missing, still a draft, or lacks any section below.

## Template

```markdown
# <KEY> — <Jira summary>

- Status: approved
- Jira: <canonical link>
- Approved: YYYY-MM-DD (grilling confirmed by the user)

## Goal
<1–3 lines: the behaviour after the change, in the user's domain words>

## Facts
- <verified fact the decisions rest on> (`<repo>` `<ref>`:`<path>:<line>`, or the data query that showed it)
- Pattern to copy: <commit> (<what it added, files>) — when the ticket adds a field, flag or feature like an existing one

## Acceptance criteria
- AC1: <observable, checkable statement>
- AC2: ...

## Decisions
<every grilling answer, one line each: decision and the reason given>
- D1: <decision> (because <reason>)

## Out of scope
- <what stays untouched, including tempting nearby cleanups>

## Rules
<team_rules from config.md plus the Repo rules of each affected repo in the codebase map, as short lines>

## Repos
| Repo | Path | Base | Branch | Checks the implementer runs | Start commit |
|---|---|---|---|---|---|
| example-api | /path/to/example-api | origin/develop | <KEY> | `npm run lint` | (filled by branch prep) |

## Tasks
<a task graph: each task names what blocks it; tasks with nothing open in "Blocked by" form the frontier>

### T1 — <title>
- Repo: <name>
- Blocked by: none
- Files: confirmed `<path>`; candidate `<path>`
- Change: <what changes and why, no code>
- Done when: <checkable condition tied to an AC>

## Verification
- Implementer runs: <per repo, only the checks listed in Repos>
- User runs by hand: <services, curl calls, screens to click>
- Evidence plan (FBI, `references/fbi.md`):

  | AC | Type | Target | Test data | Expected |
  |---|---|---|---|---|
  | AC1 | ui / api / pdf / db / log | <URL and clicks, endpoint, PDF, query> | <test record id> | <what the after capture shows> |

- Not verifiable here: <anything nobody can check before merge>

## Risks
- <risk>: <mitigation>

## Log
- YYYY-MM-DD approved by the user after grilling
```

## Rules for writing it

- Every task's `Done when` maps to at least one AC; every AC is covered by at least one task.
- Base comes from `branch_rule` (or the release ref, when `release_ref_pattern` is set) as confirmed during grilling.
- Checks are the repo's own commands from its CLAUDE.md or the codebase map's `Tests` line. Leave out service starts, full production builds and anything that writes to a shared database; those belong under "User runs by hand".
- Record a candidate path as candidate; implementers confirm it in source before editing.
- The Evidence plan has at least one row per AC, or a reason the AC cannot be captured; test data is test records only (never real customer data).
