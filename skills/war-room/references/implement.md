# Implement & Senior Review (steps 12–14)

Used by `/war-room implement <KEY>` (all sections) and `/war-room review <KEY>` (from **Review**). The method follows Matt Pocock's `implement-spec` — a task graph worked from its **frontier**, implementers briefed by **context pointers**, one review pass at the end — adapted to a multi-repo workspace: one branch per repo in its normal folder, no worktrees, no implementer commits.

## 12. Load and check the spec

1. Read `.claude/war-room/tickets/<KEY>/spec.md`. Stop with the reason if it is missing, its status is not `approved` / `implementing` / `in-review`, or a template section is missing.
2. Read `config.md` (`branch_rule`, `team_rules`) and the spec's Repos table. Confirm every repo path exists.

## 13. Prepare branches (parent)

Run these yourself; implementers never touch git state. Check every repo of the spec before branching any of them, so a ticket never ends up half-branched.

**Checks, all repos first:**

1. `git -C <path> status --porcelain` — paths matching `standing_local` in config.md are carried without asking, and so are untracked (`??`) paths absent from the base (`git -C <path> cat-file -e origin/<base>:<path>` fails): checkout leaves them in place. If any other output remains, show all of it and ask the user how to proceed: they commit or move their work, or tell you to carry it. Never stash, reset or discard their changes. Carried paths go into the spec's Log as `Carried local changes (<repo>): <paths>`; they are the user's, so review, implementers and commit staging all leave them alone.
2. `git -C <path> fetch origin`
3. Find the repo's **release ref** with the command in `references/jira-repo-investigation.md` → "Routed owner and release ref". When it differs from the spec's base, stop and ask which one is current; on the chosen ref, check each task's cited lines with `git show <ref>:<path>`, and mark a task already present there as done, with no branch for that repo.
4. When the repo's checks run through npm/npx and `<path>/node_modules` is missing, ask the user once whether to run `npm ci` there, so implementers can run their checks.
5. `git -C <path> rev-parse --verify --quiet refs/heads/<KEY>` — if the branch exists (a reopened ticket), ask: reuse it, or pick a new name such as `<KEY>-v2`.

**Then, once every answer is in, per repo:**

6. `git -C <path> checkout --no-track -b <KEY> origin/<base>`
7. Write `git -C <path> rev-parse HEAD` into the spec's `Start commit` column.

When every repo is ready, set `Status: implementing` and log it.

**FBI baseline.** HEAD still equals base, so this is the cheap moment for the `before` evidence. Ask the user whether their app is running on these branches. On yes, run the `before` phase of `references/fbi.md` before dispatching any implementer. On no, log `fbi before: skipped (<reason>)` and continue; FBI can take the baseline from another environment later.

## Implementers

Work the task graph. The frontier is every task whose `Blocked by` tasks are done. Dispatch one `war-room-implementer` per repo that has frontier tasks, with `model: <implementer_model>` from config; repos run in parallel, tasks inside one repo go to that repo's single implementer in order. When an implementer reports done, recompute the frontier and dispatch the newly unblocked repos.

Brief each implementer with pointers, not copies:

```text
Implement War Room spec <absolute spec path>, tasks <T#, T#> in repo <name> at <path>.
Read the spec's Goal, Decisions, Out of scope, Rules and your tasks first, then the repo's CLAUDE.md and CLAUDE.local.md if present.
You are on branch <KEY> already. Checks to run: <from the Repos table>.
The user's carried local changes, leave untouched: <paths from the spec Log, or "none">.
<Findings to fix, when this is a fix round: numbered, each with file:line>
```

Use the agent type the session lists (`war-room:war-room-implementer` from the plugin, or `war-room-implementer`). If neither is available, run a general-purpose subagent with the `implementer_model` from config, give it the full body of the War Room package's `agents/war-room-implementer.md` as its rules, and report the fallback.

## Review (step 14, the senior engineer)

This session is the reviewer: the implementers' reports are claims, the diff is the evidence.

1. Per repo collect the change: `git -C <path> status --porcelain`, `git -C <path> diff`, and the content of each untracked file. Every changed path must belong to a task or to the spec's carried local changes; anything else is a finding. Carried paths are never sent back as findings.
2. **Standards axis:** load `code-reviewer` and review each repo's diff against the workspace `CLAUDE.md` / `AGENTS.md`, the repo's own conventions files and the spec's Rules.
3. **Spec axis:** build a table `AC | Met? | Evidence (file:line or check output)` and a line per task with `Done when` satisfied or not. Out-of-scope items untouched.
4. **Checks:** confirm each check the implementer claims to have run by its reported output; rerun a cheap one (lint on changed files) yourself when the output is missing.
5. Findings go back to the same repo's implementer as a fix round (continue it with SendMessage when available). After two fix rounds with open findings, stop and bring them to the user instead of looping.
6. When both axes are clean, ask the user to restart the services the diff touches, then run the `after` phase of `references/fbi.md`. Each `Not met` row is a finding for step 5. When the user cannot run the app now, log `fbi after: pending` and say so in the output.
7. When review and FBI are clean, set `Status: in-review`, log it, and continue with `references/delivery.md`.

## Output to the user after review

Report in `report_language`: per repo the branch, changed files, checks run with result, the AC table, the FBI verdict table with the evidence folder path, test files written (and whether `team_rules` keeps them out of the commit), findings fixed, anything not verified, and what the user should run by hand from the spec's Verification section.
