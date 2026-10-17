# War-room-agent-skills

`/war-room` คือ skill ของ Claude Code ที่อ่าน Jira ticket ของคุณ หาว่าต้องแก้ repo ไหน พร้อมหลักฐานจากโค้ด แล้วทำแผนงานพร้อมประเมินขนาด (S/M/L/XL) **มันอ่านอย่างเดียว ไม่แก้โค้ด ไม่แก้ Jira**

`/war-room` is a Claude Code skill that reads your Jira tickets, finds which repositories need to change (with code evidence), and produces a sized implementation plan. **It is read-only: it never edits code or Jira.**

## ในแพ็กเกจ / What's inside

| Path | What |
|---|---|
| `skills/war-room/` | The skill: `SKILL.md`, references, `config.template.md` |
| `skills/impact-analysis/` | Blast-radius analysis skill that War Room uses |
| `agents/war-room-*.md` | 4 subagents: investigator, diagnostician, brainstormer, planner |

## ติดตั้ง / Install

**1. Clone and copy** (Git Bash, macOS, Linux)

```bash
git clone https://github.com/jolynestarchaser/War-room-agent-skills.git
cd War-room-agent-skills
mkdir -p ~/.claude/skills ~/.claude/agents
cp -r skills/war-room skills/impact-analysis ~/.claude/skills/
cp agents/war-room-*.md ~/.claude/agents/
```

PowerShell:

```powershell
git clone https://github.com/jolynestarchaser/War-room-agent-skills.git
cd War-room-agent-skills
New-Item -ItemType Directory -Force "$HOME\.claude\skills", "$HOME\.claude\agents" | Out-Null
Copy-Item -Recurse skills\war-room, skills\impact-analysis "$HOME\.claude\skills\"
Copy-Item agents\war-room-*.md "$HOME\.claude\agents\"
```

If you already have a folder with the same name, back it up first; the copy overwrites it.

**2. Connect Jira.** Add the Atlassian MCP server to Claude Code and sign in with `/mcp`. War Room expects the server to be named `atlassian`; another name still works but asks for permission on each Jira call.

**3. Restart Claude Code** in the folder that contains your repositories (your workspace), then run:

```
/war-room setup
```

Setup checks everything and asks you for whatever is missing before any investigation starts:

- **Config** — creates `.claude/war-room/config.md` in your workspace and asks for Jira site, project keys, repository list, branch rule and team rules in one message.
- **Skills** — lists missing dependencies (below), asks, then installs them to `~/.claude/skills/`.
- **Jira** — checks the connection and that the site matches your config.
- **Codebase map** — builds `.claude/war-room/explore.md`: one Explore agent per repository summarises what it does, its routes, what it calls and its data. War Room reads this map first, then confirms in source.

`config.md` and `explore.md` describe your team's systems. They stay on your machine; do not commit or share them publicly.

## ใช้งาน / Usage

| Command | What it does |
|---|---|
| `/war-room` or `/war-room triage` | Your open assigned tickets, first 5 |
| `/war-room ABC-123` | One ticket |
| `/war-room deep ABC-123` | One ticket, deeper tracing and more options |
| `/war-room all` | All open assigned tickets, investigated in batches |
| `/war-room setup` | Setup check only |
| `/war-room map [repo ...]` | Rebuild the codebase map (all or named repos) |

War Room is user-invoked only: type the command; Claude will not start it on its own.

## Skills ที่ต้องใช้ / Dependencies

Setup installs these when missing (after asking). Credit to their authors.

| Skill | Need | Source |
|---|---|---|
| `atlassian-mcp`, `feature-forge`, `spec-miner`, `debugging-wizard`, `the-fool` | required | [jeffallan/claude-skills](https://github.com/jeffallan/claude-skills) (MIT) |
| `microservices-architect`, `api-designer` | optional | [jeffallan/claude-skills](https://github.com/jeffallan/claude-skills) (MIT) |
| `buddhist-method` | required | [nai0om/buddhist-method](https://github.com/nai0om/buddhist-method) (MIT) |
| `impact-analysis` | required | this repository |

## Update

Pull this repository and copy the files again (step 1). Your `config.md` and `explore.md` are not touched.
