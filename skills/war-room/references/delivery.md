# Delivery: Sign-off, Commit, PR Draft, Retro (steps 15–17)

Runs after the senior review leaves the spec `in-review`. Every write here waits for an explicit yes from the user to that exact action.

## 15. Human sign-off

1. Show the FBI verdict table from `tickets/<KEY>/evidence/fbi.md` (or say `fbi after: pending`), then ask the user to test what the spec's Verification section lists under "User runs by hand" and what FBI left Not verifiable; they run services themselves.
2. Offer `/grill-me` (a quiz on the changed code) before they approve, so the knowledge of what the agents built stays with them. It is user-invoked; suggest it, do not run it.
3. Changes the user asks for go back through `references/implement.md` as a fix round, then review again.
4. Continue only when the user says the work is OK.

## 16. Commit (ask first)

Per repo, show the proposed commit and wait for yes:

- Message: the repo's convention from its recent `git log`; when it has none, `[<KEY>] <type>: <message>` with type one of feat / fix / refactor / chore. Apply every commit rule in `team_rules` (attribution lines, ticket prefix).
- Files: files changed for the tasks, staged by explicit path. Leave out the spec's carried local changes, `standing_local` paths and local config. When `team_rules` keeps test files out of commits, leave them in the working tree, list them, and ask if one must ship for the build.

On yes: `git -C <path> add -- <paths>` then `git -C <path> commit -m "<message>"`. If a pre-commit hook fails, show its output and fix the cause through a fix round; never skip hooks. Pushing waits for its own explicit request.

## 17. PR drafts, Jira comment, delivered

1. Load `pr` and write one body per repo to `tickets/<KEY>/pr-<repo>.md`: Summary as the smallest diagram or diff-sketch, Evidence listing only checks actually run, the FBI rows with their before/after file names (the user attaches the images), the user's manual test results and a "Not verified" line, Merge Danger with door and blast radius. Suggested title `[<KEY>] <summary>` and target branch = the spec's base. The user opens the PR on `pr_host`.
   For a schema migration, the body also carries the migration's up/down code, the commands that apply, revert and list exactly this migration (a bare "revert last" undoes whichever migration ran last), and the deploy order against the services that read the new structure.
2. Offer a Jira comment draft for the ticket in `tickets/<KEY>/jira-comment.md`. War Room never posts it.
3. Set the spec to `Status: delivered`, log the commit hashes (or "not committed") and the PR draft paths.
4. Tell the user: run `/retro` for this session, pointing it at War Room.
5. When `codebase_map_owner` or `knowledge_sources` name a knowledge base, offer to record the ticket there (decisions, traps found in the touched repos) with that tool. Run it only on the user's yes.

## Retro (user-invoked)

`/retro` belongs to the user; War Room cannot start it. When the user runs it after a War Room ticket, the retro targets War Room itself:

- Read earlier `tickets/*/retro.md` first, so a proposal already made is escalated or dropped rather than repeated.
- Proposals cover the War Room skill (`~/.claude/skills/war-room/`), its agents (`~/.claude/agents/war-room-*.md`), `config.md` team rules, the workspace CLAUDE.md / AGENTS.md and hooks.
- Apply only proposals the user approves. After changing the War Room skill, rerun the relevant cases in `references/evaluation.md`.
- Write `tickets/<KEY>/retro.md`: date, proposals with accepted / rejected, and the files changed.
