# War-room-agent-skills

`/war-room` คือ skill ของ Claude Code ที่รับ Jira ticket แล้วพาไปจนจบงาน: หาว่าต้องแก้ repo ไหนพร้อมหลักฐานจากโค้ด, ทำแผนพร้อมประเมินขนาด (S/M/L/XL), ถามคำถามที่ต้องตัดสินใจจนได้ spec ที่อนุมัติแล้ว, ให้ subagent เขียนโค้ดตาม spec, review แบบ senior, เก็บหลักฐาน before/after (FBI) แล้วค่อย commit เมื่อคุณตอบ yes **ไม่ push, ไม่เปิด PR, ไม่แก้ Jira**

`/war-room` is a Claude Code skill that takes a Jira ticket from investigation to a reviewed change: it finds which repositories need to change (with code evidence), sizes the work, grills the open decisions into an approved spec, has subagents implement the spec, reviews the diff as the senior engineer, captures before/after evidence (FBI), and commits only after your yes. **It never pushes, opens a PR or edits Jira.**

## ในแพ็กเกจ / What's inside

| Path | What |
|---|---|
| `skills/war-room/` | The skill: `SKILL.md`, references, `config.template.md` |
| `skills/impact-analysis/` | Blast-radius analysis skill that War Room uses |
| `skills/jira-read/` | Optional: downloads Jira attachments (screenshots, PDFs) so they get read |
| `agents/war-room-*.md` | 5 subagents: investigator, diagnostician, brainstormer, planner, implementer |

## ติดตั้ง / Install

**1. Clone and copy** (Git Bash, macOS, Linux)

```bash
git clone https://github.com/jolynestarchaser/War-room-agent-skills.git
cd War-room-agent-skills
mkdir -p ~/.claude/skills ~/.claude/agents
cp -r skills/war-room skills/impact-analysis skills/jira-read ~/.claude/skills/
cp agents/war-room-*.md ~/.claude/agents/
```

PowerShell:

```powershell
git clone https://github.com/jolynestarchaser/War-room-agent-skills.git
cd War-room-agent-skills
New-Item -ItemType Directory -Force "$HOME\.claude\skills", "$HOME\.claude\agents" | Out-Null
Copy-Item -Recurse skills\war-room, skills\impact-analysis, skills\jira-read "$HOME\.claude\skills\"
Copy-Item agents\war-room-*.md "$HOME\.claude\agents\"
```

If you already have a folder with the same name, back it up first; the copy overwrites it.

**2. Connect Jira.** Add the Atlassian MCP server to Claude Code and sign in with `/mcp`. War Room expects the server to be named `atlassian`; another name still works but asks for permission on each Jira call.

**3. Restart Claude Code** in the folder that contains your repositories (your workspace), then run:

```
/war-room setup
```

Setup interviews you (the person installing) before any investigation starts:

- **Workspace** — asks whether the current folder is your workspace (where War Room keeps its files) and which folder holds your repositories.
- **Config** — creates `.claude/war-room/config.md` in your workspace and asks for Jira site, project keys, repository list, branch rule and team rules in one message.
- **Codebase knowledge** — asks where your team already keeps knowledge about the repositories (a knowledge base, docs, or nothing yet) and points War Room at it.
- **Skills** — lists every missing dependency below with what it is for, asks which to install, then downloads them to `~/.claude/skills/`.
- **Jira** — checks the connection and that the site matches your config.
- **Codebase map** — unless your own knowledge base is the map, builds `.claude/war-room/explore.md`: one read-only agent per repository summarises what it does, its routes, what it calls and its data. War Room reads this map first, then confirms in source.

`config.md`, `explore.md` and `tickets/` describe your team's systems. They stay on your machine; do not commit or share them publicly.

## ใช้งาน / Usage

| Command | What it does |
|---|---|
| `/war-room` or `/war-room triage` | Your open assigned tickets, first 5 |
| `/war-room ABC-123` | One ticket |
| `/war-room deep ABC-123` | One ticket, deeper tracing and more options |
| `/war-room all` | All open assigned tickets, investigated in batches |
| `/war-room implement ABC-123` | Implement an approved spec: branches, implementers, senior review |
| `/war-room review ABC-123` | Review the current changes against the spec (e.g. in a fresh chat) |
| `/war-room fbi ABC-123 [before\|after]` | Before/after evidence and a verdict per acceptance criterion |
| `/war-room setup` | Setup check only |
| `/war-room map [repo ...]` | Rebuild the codebase map (all or named repos) |
| `/war-room maid` | Delete downloaded attachments of finished tickets (needs `jira-read`) |

Flow: investigate → report → take a ticket forward → grilling → `tickets/<KEY>/spec.md` (approved) → `/war-room implement` → review → FBI → your sign-off → commit on yes → PR body drafts → `/retro`.

War Room is user-invoked only: type the command; Claude will not start it on its own.

## Skills ที่ต้องใช้ / Dependencies

Setup installs these when missing (after asking). Credit to their authors.

| Skill | Need | Source |
|---|---|---|
| `atlassian-mcp`, `feature-forge`, `spec-miner`, `debugging-wizard`, `the-fool`, `code-reviewer` | required | [jeffallan/claude-skills](https://github.com/jeffallan/claude-skills) (MIT) |
| `microservices-architect`, `api-designer` | optional | [jeffallan/claude-skills](https://github.com/jeffallan/claude-skills) (MIT) |
| `grilling`, `pr` | required | [mattpocock/skills](https://github.com/mattpocock/skills) (MIT) |
| `retro` | optional, user-invoked | [mattpocock/skills](https://github.com/mattpocock/skills) (MIT) |
| `buddhist-method` | required | [nai0om/buddhist-method](https://github.com/nai0om/buddhist-method) (MIT) |
| `grill-me` | optional, user-invoked | [joshuawheelock/grill-me](https://github.com/joshuawheelock/grill-me) (MIT) |
| `chrome-devtools-cli` | optional (FBI screenshots) | Claude Code plugin [chrome-devtools-mcp](https://github.com/ChromeDevTools/chrome-devtools-mcp) |
| `impact-analysis`, `jira-read` | required / optional | this repository |

## Update

Pull this repository and copy the files again (step 1). Your `config.md`, `explore.md` and `tickets/` are not touched.
