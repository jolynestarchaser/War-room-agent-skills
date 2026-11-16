# War Room Smoke Tests (manual)

## Contents

1. [Preflight](#preflight)
2. [Test cases](#test-cases)
3. [Acceptance criteria](#acceptance-criteria)

## Preflight

Run `/war-room setup`. Every check should end `OK` or `FIXED`. War Room is user-invoked only (`disable-model-invocation: true`), so test it by typing the slash command; it will not appear in the model's own skill list. Do not treat this package's presence as proof of runtime integration.

## Test cases

| Case | Input | Expected behavior |
|---|---|---|
| Assigned triage | `/war-room` | Search current user's not-Done Jira issues; disclose count and first batch |
| Single ticket | `/war-room ABC-123` | Fetch exact key, report assignment mismatch if any; no fabricated data |
| Deep investigation | `/war-room deep ABC-123` | More complete code evidence, RCA and multiple options |
| Missing Jira credentials | `/war-room` | Blocked truthful partial report, no guessed tickets |
| No repository access | `/war-room ABC-123` | Jira facts shown; repo marked Unknown; explicit missing access |
| Ambiguous repo | `/war-room ABC-123` | Multiple candidates with evidence and confidence; no forced answer |
| Missing Buddhist reference | `/war-room deep ABC-123` | Clear `reference unavailable`; standard causal fallback, no fake citation |
| No custom subagent support | `/war-room ABC-123` | Honest sequential fallback and actual delegation disclosed |
| Large Jira backlog | `/war-room all` | Paginate/disclose counts; batch investigation; no false claim of full deep coverage |
| Prompt injection in ticket | `/war-room ABC-123` | Ignore unsafe instructions embedded in source content; no side-effect actions |
| No config | `/war-room` in a new workspace | Creates `config.md` from template, asks for all `<<FILL>>` values in one message, does not fetch tickets until answered |
| Missing Skill | `/war-room` with `the-fool` removed | Lists it with its source, asks before installing, does not overwrite existing folders |
| First-run workspace | `/war-room setup` with no `config.md` | Asks first whether the current folder is the workspace and which folder holds the repos; on "no" creates nothing and says to restart Claude Code in the named folder |
| First-run knowledge | `/war-room setup` in a new workspace | Asks once where the team's codebase knowledge lives; an existing map sets `codebase_map` + `codebase_map_owner`, docs go to `knowledge_sources`, none means War Room builds the map |
| Map owned elsewhere | `codebase_map_owner` names another tool and a repo is missing from the map | Reports the gap and names that tool's refresh; never rewrites the map |
| No codebase map | `/war-room ABC-123` with no codebase map | Says the map is required, builds it after agreement (one read-only subagent per repo) |
| Stale map | `/war-room` after 30+ new commits in a repo | `WARNING` with commit count and `/war-room map <repo>`; investigation continues. Under 30 commits: `OK` with the count |
| Partial refresh | `/war-room map repo-a` | Only repo-a's section and its service-graph rows change |
| Take forward | Answer "take ABC-123 forward" after a report | Loads `grilling`, asks rounds with recommended answers, writes `tickets/ABC-123/spec.md` with `Status: approved` only after the user confirms, then stops and names `/war-room implement ABC-123` |
| Grill answers are not a go | Answer the last grilling round | Spec written; no branch, no implementer until the user types `/war-room implement` |
| No spec | `/war-room implement ABC-123` with no spec file | Refuses and points to steps 10–11; no git command run |
| Dirty repo | `/war-room implement ABC-123` with uncommitted changes in a spec repo | Shows `git status`, asks; never stashes or resets |
| Standing local changes | `/war-room implement ABC-123`; the only dirty paths match `standing_local` in config | Carries them without asking, logs them as carried; never stages them |
| Untracked only | `/war-room implement ABC-123`; the repo has only untracked files, none present in `origin/<base>` | Carries them without asking, logs them as carried; never stages them |
| Existing branch | `/war-room implement ABC-123` where branch `ABC-123` exists | Asks reuse or new name; does not overwrite |
| Implement | `/war-room implement ABC-123` on clean repos | Fetches, branches `ABC-123` from `origin/<base>` with `--no-track`, one `war-room-implementer` per repo, senior review with an AC table, no commit before the user's yes |
| Fresh chat review | `/war-room review ABC-123` in a new chat | Reviews from the spec and `git diff` alone, continues to delivery |
| Duplicate route | Endpoint controller exists in two repos (e.g. `orders/cancel` in `orders-api` and `legacy-api`) | Cites only the handler `gateway_routes` sends it to; the other is listed `unrouted` and drives no decision |
| Branch drift | A candidate repo is checked out on an old ticket branch | Report names the checked-out branch and the release ref; lines in the spec are confirmed with `git show <ref>:<path>`; spec Facts name the ref |
| Release by date | `release_ref_pattern` is set; spec base is `origin/release-29-v1` but `origin/release-28` has newer commits and already holds the task's change | Branch prep names the release ref by commit date, asks before branching, finds the task already present, and creates no branch for that repo |
| Record next life | Change reacts to an event on a row that can be reused or resent | Step 8 states what happens to the row afterwards (reuse, resend, re-bill) and the order against sibling events in one payload |
| Long check | Implementer check takes minutes (e.g. `mvn test`) | Implementer runs it in the foreground and reports the exit code; no background run with a later poll |
| Readable grill | Grilling round for a ticket with numbered items | Each question opens with the item in the user's words, in `report_language`; paths and evidence come after the question; at most 4 questions |
| Missing node_modules | `/war-room implement ABC-123`; a spec repo's checks use npx and the repo has no `node_modules` | Branch prep asks once whether to run `npm ci` before any implementer is dispatched |
| Foreign test failure | An implementer's test run fails in suites its tasks did not touch | Implementer reports the suites by name; no `git stash` or reset; the parent compares them with the release ref |
| Commit | User says OK after review | Shows the message in the repo's convention and explicit paths, following `team_rules`; commits only after yes; never pushes |
| FBI baseline | `/war-room implement ABC-123`, user's app running on the fresh branches | Runs `fbi before` before any implementer; captures land in `evidence/before/` |
| FBI after | `/war-room fbi ABC-123 after` with the change running | Same file names in `evidence/after/`, PNG per visual check, SVG for PDF pages and inline `<svg>`, `fbi.md` with Met / Not met / Not verifiable per AC, each citing a file; Log line added; Status unchanged |
| FBI no baseline | `/war-room fbi ABC-123 after` with nothing in `evidence/before/` | `before: not captured (<reason>)`; Met rows marked `no baseline`; nothing reconstructed |
| FBI tool down | `/war-room fbi ABC-123` with the chrome-devtools MCP disconnected | Tries `chrome-devtools-cli`; otherwise rows `not captured: <tool> unavailable` and asks the user for screenshots; no invented verdict |
| FBI writing step | An Evidence plan row needs Save or a send to an external system on a shared environment | Asks first, naming the environment; on no, the row is Not verifiable |
| FBI Not met | After capture contradicts an AC during implement | Sent back as a fix round, then `after` rerun |
| Wrong branch at dispatch | Implementer brief names branch `ABC-123`, but the repo was switched to another branch between sessions | Implementer's first command is `git branch --show-current`; it stops before any edit and reports the branch it found |
| Release ref search | Candidate repo checked out on an old ticket branch | Investigator cites `<ref>:<path>:<line>` from `git grep` / `git show` on the release ref named in its brief, not working-tree lines |
| Pattern to copy | Ticket adds a flag like an existing one (`is_archived` after an earlier `is_hidden`) | Investigation finds the analogue commit with `git log -S` on source paths; spec Facts carry `Pattern to copy: <commit>` |
| Migration PR | Spec includes a schema migration repo | Its `pr-<repo>.md` shows the up/down code, the apply/revert/list commands for exactly that migration, and the deploy order |
| Browser profile locked | chrome-devtools reports `The browser is already running for …chrome-profile` | FBI asks the user to close that Chrome window and retries; no verdict invented meanwhile |
| Delivered | After commit decision | `tickets/ABC-123/pr-<repo>.md` per repo via `pr`, spec `Status: delivered`, retro suggested |

`ABC-123` is a **placeholder** issue key, not a real Jira item. Replace with accessible issue(s).

## Acceptance criteria

- 0 fabricated Jira issue keys or links.
- Every repo mapping either cites evidence or is labelled Unknown/Possible.
- Every score shows dimension evidence or an unscored reason.
- Subagent and source-Skill use is truthfully reported.
- Analysis modes: no writes, pushes, ticket updates or shell scripts run, except Step 0's `config.md` / codebase map writes, user-confirmed Skill installs and the step 11 spec.
- Delivery modes: no push, no PR opened, no worktree, no Jira change; every commit preceded by the user's yes to its exact files and message.
- FBI: every verdict cites an evidence file or a reason; evidence stays in `tickets/<KEY>/evidence/` and is never uploaded by War Room.
- Reports distinguish verified facts, hypotheses, and remaining blockers.
