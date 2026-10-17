# Step 0 — Setup Check

Run this before every War Room run (and alone for `/war-room setup`). Check in this order. When something is missing, tell the user exactly what is missing, ask for it, and **do not start step 1** until it is resolved. Report one line per check: `OK`, `FIXED`, `WARNING` or `MISSING`.

## Contents

1. [Config](#1-config)
2. [Required Skills](#2-required-skills)
3. [Custom agents](#3-custom-agents)
4. [Jira connection](#4-jira-connection)
5. [Codebase map](#5-codebase-map)

## 1. Config

File: `<workspace>/.claude/war-room/config.md` (workspace = the folder Claude Code was started in).

1. If the file does not exist, create it from the War Room `config.template.md` (in this Skill's folder).
2. Collect every remaining `<<FILL>>` in **one** message, not one question per turn. Offer a suggested value where you can find one, and let the user confirm or correct it:
   - `jira_site`: suggest from `getAccessibleAtlassianResources` if Jira is already connected.
   - `workspace_root`: suggest the workspace folder.
   - `repos`: list the folders under `workspace_root` (depth 1, and depth 2 if none found) that contain a `.git` folder, as `name | path` lines, and ask the user to confirm, remove or add.
   - `jira_projects`, `branch_rule`: ask; there is no safe default.
   - `ariyasacca_path`: do not ask; fill it in check 2.
   - Optional fields: show the current value and say the user may leave it.
3. Wait for the answer, write the values into `config.md`, and show the final file. Never guess a required value.
4. Validate: every repo path exists. Report any that do not and ask again.

## 2. Required Skills

A Skill counts as installed if it appears in this session's skill list, or its `SKILL.md` exists in `~/.claude/skills/<name>/` or `<workspace>/.claude/skills/<name>/`.

| Skill | Need | Used in step | Source |
|---|---|---|---|
| `atlassian-mcp` | required | 1–2 | `https://github.com/jeffallan/claude-skills` → `skills/atlassian-mcp` |
| `feature-forge` | required | 3 | `https://github.com/jeffallan/claude-skills` → `skills/feature-forge` |
| `spec-miner` | required | 4 | `https://github.com/jeffallan/claude-skills` → `skills/spec-miner` |
| `impact-analysis` | required | 4 | War Room package → `skills/impact-analysis` |
| `debugging-wizard` | required | 5 | `https://github.com/jeffallan/claude-skills` → `skills/debugging-wizard` |
| `buddhist-method` | required | 5 | `https://github.com/nai0om/buddhist-method` (repository root is the Skill) |
| `the-fool` | required | 8 | `https://github.com/jeffallan/claude-skills` → `skills/the-fool` |
| `microservices-architect` | optional | 6–7 | `https://github.com/jeffallan/claude-skills` → `skills/microservices-architect` |
| `api-designer` | optional | 6–7 | `https://github.com/jeffallan/claude-skills` → `skills/api-designer` |

If any are missing:

1. List the missing ones with their source and ask the user to confirm installing them to `~/.claude/skills/`.
2. On confirmation, install with Bash (works in Git Bash, macOS and Linux). Clone each source repository once, then copy only the listed folders:

   ```bash
   tmp="$(mktemp -d)"
   git clone --depth 1 https://github.com/jeffallan/claude-skills.git "$tmp/claude-skills"
   cp -r "$tmp/claude-skills/skills/<name>" ~/.claude/skills/   # repeat per missing Skill
   git clone --depth 1 https://github.com/nai0om/buddhist-method.git ~/.claude/skills/buddhist-method
   ```

   For `impact-analysis`, copy `skills/impact-analysis` from the War Room package the user downloaded. If you do not know where that is, ask.
3. Never overwrite an existing Skill folder. If a folder exists but has no `SKILL.md`, report it instead of replacing it.
4. Confirm each `SKILL.md` now exists. Newly installed Skills may not appear in the skill list until Claude Code is restarted; say so if they do not.
5. If the user declines a required Skill, continue only with the user's explicit agreement, and name the fallback in the report.

Then set `ariyasacca_path` in config to the first path that exists:
`~/.claude/skills/buddhist-method/references/ariyasacca-debug.md`, then `<workspace>/.claude/skills/buddhist-method/references/ariyasacca-debug.md`. If neither exists, write `unavailable`.

## 3. Custom agents

Check that `war-room-investigator`, `war-room-diagnostician`, `war-room-brainstormer` and `war-room-planner` are available (the session's agent list, or `~/.claude/agents/<name>.md`). If any are missing, tell the user to copy `agents/*.md` from the War Room package to `~/.claude/agents/` and restart Claude Code. Until then, use the fallback in SKILL.md boundary 6.

## 4. Jira connection

1. Call `atlassianUserInfo` or `getAccessibleAtlassianResources`. If the Atlassian tools are not present at all, report `MISSING — Atlassian MCP not connected` and point the user to the setup section of the `atlassian-mcp` Skill; after adding the server they run `/mcp` to sign in.
2. Check that the connected site matches `jira_site` in config. If not, ask which one is correct.
3. Check that a JQL search tool is available (`searchJiraIssuesUsingJql` or equivalent). Triage modes need it.
4. If the MCP server is registered under a name other than `atlassian`, the tool names differ and the `allowed-tools` pre-approval in SKILL.md will not match; the tools still work but ask for permission. Mention this once.

## 5. Codebase map

File: `<workspace>/.claude/war-room/explore.md`. Build and refresh rules are in `references/codebase-map.md`.

- **Missing:** tell the user the map is required and that building it runs one Explore agent per repo. Build it after the user agrees. If the user says to skip for this run, continue and mark every repo finding as `no map` in the report.
- **A repo in config has no section:** build that section only.
- **Stale:** for each repo, count `git -C <path> rev-list --count <recorded>..HEAD`. Teams that cut a branch per ticket move HEAD on almost every run, so a few commits is normal: show `OK (<n> commits since scan)`. Show a `WARNING` with the count and `/war-room map <repo>` only when the count is 30 or more, the recorded commit no longer exists, or the scan date is more than 30 days old. Never block.
