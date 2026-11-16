# Step 0 — Setup Check

Run this before every War Room run (and alone for `/war-room setup`). The person running it is the one who installed War Room: setup interviews them for everything it cannot find itself. Check in this order. When something is missing, tell the user exactly what is missing, ask for it, and **do not start step 1** until it is resolved. Report one line per check: `OK`, `FIXED`, `WARNING` or `MISSING`.

## Contents

1. [Config](#1-config)
2. [Codebase knowledge](#2-codebase-knowledge)
3. [Required Skills](#3-required-skills)
4. [Custom agents](#4-custom-agents)
5. [Jira connection](#5-jira-connection)
6. [Codebase map](#6-codebase-map)

## 1. Config

File: `<workspace>/.claude/war-room/config.md` (workspace = the folder Claude Code was started in).

1. **Workspace.** When `config.md` does not exist yet, ask this first, before creating any file:

   ```text
   War Room keeps its config, codebase map and ticket specs in <current folder>/.claude/war-room/.
   1. Is <current folder> your workspace (the folder you will start Claude Code in for War Room)?
   2. Which folder holds your repositories? (suggested: <current folder>)
   ```

   - Yes to 1: continue here; answer 2 becomes `workspace_root`.
   - No to 1: create nothing. Tell the user to restart Claude Code in the folder they name and run `/war-room setup` there, then stop.
   - Validate answer 2 exists; when it holds no `.git` folder at depth 1–2, say so and ask again.
2. If `config.md` does not exist, create it from the War Room `config.template.md` (in this Skill's folder).
3. Collect every remaining `<<FILL>>` in **one** message, not one question per turn. Offer a suggested value where you can find one, and let the user confirm or correct it:
   - `jira_site`: suggest from `getAccessibleAtlassianResources` if Jira is already connected.
   - `workspace_root`: already answered in item 1; show it.
   - `repos`: list the folders under `workspace_root` (depth 1, and depth 2 if none found) that contain a `.git` folder, as `name | path` lines, and ask the user to confirm, remove or add.
   - `jira_projects`, `branch_rule`: ask; there is no safe default.
   - `ariyasacca_path`: do not ask; fill it in check 3.
   - Optional fields: show the current value and say the user may leave it. `team_rules` deserves a sentence: it is where the team's commit, test and data rules go, and implementers and commits follow it.
4. Wait for the answer, write the values into `config.md`, and show the final file. Never guess a required value. A `config.md` from an older War Room may lack keys the template now has: add each missing key with its template default and say which were added.
5. Validate: every repo path exists. Report any that do not and ask again.

## 2. Codebase knowledge

War Room maps a ticket to code through a **codebase map**: what each repo does, what it exposes and calls, its data and its rules. Ask once, on the first setup (while `codebase_map_owner` is still the template default and the map file does not exist):

```text
Does your team already keep knowledge about these repositories somewhere?
1. Yes, a map or knowledge base (Obsidian vault, docs folder, ARCHITECTURE.md, wiki export, generated graph): give the path and how you refresh it.
2. Some docs, but no map (README, CLAUDE.md / AGENTS.md, ADRs): give the paths; War Room builds its own map and reads these too.
3. Nothing yet: War Room builds a map (one read-only subagent per repo).
```

- **Answer 1:** set `codebase_map` to the given file (or the index note of the folder) and `codebase_map_owner` to the tool or refresh command. Read it once and check it names each repo in `repos`; list repos it does not cover. War Room never rewrites a map owned elsewhere.
- **Answer 2:** keep the default map, add each path to `knowledge_sources` with one line on what it holds.
- **Answer 3:** keep the defaults; check 6 builds the map.

Record the answer in `config.md` and show the changed lines. On later runs skip the question and only validate that each path still exists.

## 3. Required Skills

A Skill counts as installed if it appears in this session's skill list (plugin skills appear with a prefix, e.g. `war-room:impact-analysis`), or its `SKILL.md` exists in `~/.claude/skills/<name>/` or `<workspace>/.claude/skills/<name>/`. Installed as the `war-room` plugin, `impact-analysis` and `jira-read` come with it.

| Skill | Need | Used in step | Source |
|---|---|---|---|
| `atlassian-mcp` | required | 1–2 | `https://github.com/jeffallan/claude-skills` → `skills/atlassian-mcp` |
| `feature-forge` | required | 3 | `https://github.com/jeffallan/claude-skills` → `skills/feature-forge` |
| `spec-miner` | required | 4 | `https://github.com/jeffallan/claude-skills` → `skills/spec-miner` |
| `impact-analysis` | required | 4 | War Room package → `skills/impact-analysis` |
| `debugging-wizard` | required | 5 | `https://github.com/jeffallan/claude-skills` → `skills/debugging-wizard` |
| `buddhist-method` | required | 5 | `https://github.com/nai0om/buddhist-method` (repository root is the Skill) |
| `the-fool` | required | 8 | `https://github.com/jeffallan/claude-skills` → `skills/the-fool` |
| `grilling` | required | 10 | `https://github.com/mattpocock/skills` → `skills/productivity/grilling` |
| `code-reviewer` | required | 14 | `https://github.com/jeffallan/claude-skills` → `skills/code-reviewer` |
| `pr` | required | 17 | `https://github.com/mattpocock/skills` → `skills/engineering/pr` |
| `jira-read` | optional | 2 | War Room package → `skills/jira-read` (needs a Jira API token, see its SKILL.md) |
| `microservices-architect` | optional | 6–7 | `https://github.com/jeffallan/claude-skills` → `skills/microservices-architect` |
| `api-designer` | optional | 6–7 | `https://github.com/jeffallan/claude-skills` → `skills/api-designer` |
| `chrome-devtools-cli` | optional | 14, `fbi` | Claude Code plugin `chrome-devtools-mcp` (`https://github.com/ChromeDevTools/chrome-devtools-mcp`); install the plugin, not a folder copy |
| `grill-me` | optional, user-invoked | 15 | `https://github.com/joshuawheelock/grill-me` → `skills/grill-me` |
| `retro` | optional, user-invoked | after 17 | `https://github.com/mattpocock/skills` → `skills/engineering/retro` |

If any are missing:

1. Show the user one list: each missing Skill, required or optional, what War Room uses it for (one line), and its source. Ask which to install to `~/.claude/skills/`; default is all required ones.
2. On confirmation, install with Bash (works in Git Bash, macOS and Linux). Clone each source repository once, then copy only the listed folders:

   ```bash
   tmp="$(mktemp -d)"
   git clone --depth 1 https://github.com/jeffallan/claude-skills.git "$tmp/claude-skills"
   cp -r "$tmp/claude-skills/skills/<name>" ~/.claude/skills/   # repeat per missing Skill
   git clone --depth 1 https://github.com/mattpocock/skills.git "$tmp/mattpocock"
   cp -r "$tmp/mattpocock/skills/productivity/grilling" "$tmp/mattpocock/skills/engineering/pr" ~/.claude/skills/
   git clone --depth 1 https://github.com/nai0om/buddhist-method.git ~/.claude/skills/buddhist-method
   ```

   For `impact-analysis` and `jira-read` without the plugin, copy `skills/<name>` from the War Room package the user downloaded. If you do not know where that is, ask.
3. Never overwrite an existing Skill folder. If a folder exists but has no `SKILL.md`, report it instead of replacing it.
4. Confirm each `SKILL.md` now exists. Newly installed Skills may not appear in the skill list until Claude Code is restarted; say so if they do not.
5. If the user declines a required Skill, continue only with the user's explicit agreement, and name the fallback in the report.

Then set `ariyasacca_path` in config to the first path that exists:
`~/.claude/skills/buddhist-method/references/ariyasacca-debug.md`, then `<workspace>/.claude/skills/buddhist-method/references/ariyasacca-debug.md`. If neither exists, write `unavailable`.

## 4. Custom agents

Check that `war-room-investigator`, `war-room-diagnostician`, `war-room-brainstormer`, `war-room-planner` and `war-room-implementer` (delivery modes) are available (the session's agent list, as `war-room:<name>` from the plugin or `<name>`, or `~/.claude/agents/<name>.md`). If any are missing, tell the user to install the `war-room` plugin, or copy `agents/*.md` from the War Room package to `~/.claude/agents/`, and restart Claude Code. Until then, use the fallback in SKILL.md boundary 6.

## 5. Jira connection

1. Call `atlassianUserInfo` or `getAccessibleAtlassianResources`. If the Atlassian tools are not present at all, report `MISSING — Atlassian MCP not connected` and point the user to the setup section of the `atlassian-mcp` Skill; after adding the server they run `/mcp` to sign in.
2. Check that the connected site matches `jira_site` in config. If not, ask which one is correct.
3. Check that a JQL search tool is available (`searchJiraIssuesUsingJql` or equivalent). Triage modes need it.
4. If the MCP server is registered under a name other than `atlassian`, the tool names differ and the `allowed-tools` pre-approval in SKILL.md will not match; the tools still work but ask for permission. Mention this once.
5. When `jira-read` is installed, check that its environment variables are set (its SKILL.md lists them). Missing ones are a `WARNING`: attachments are then read only when the user pastes them.

## 6. Codebase map

File: `codebase_map` from config (default `<workspace>/.claude/war-room/explore.md`). Build and refresh rules are in `references/codebase-map.md`. When `codebase_map_owner` is not `war-room`, never build or rewrite the map here: report missing repos and staleness and name the owner's refresh command in place of `/war-room map`.

- **Missing:** tell the user the map is required and that building it runs one read-only subagent per repo. Build it after the user agrees. If the user says to skip for this run, continue and mark every repo finding as `no map` in the report.
- **A repo in config has no section:** build that section only.
- **Stale:** for each repo, count `git -C <path> rev-list --count <recorded>..HEAD`. Teams that cut a branch per ticket move HEAD on almost every run, so a few commits is normal: show `OK (<n> commits since scan)`. Show a `WARNING` with the count and `/war-room map <repo>` only when the count is 30 or more, the recorded commit no longer exists, or the scan date is more than 30 days old. Never block.
