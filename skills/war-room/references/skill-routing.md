# Skill Routing & Ariyasacca Reference

## Contents

1. [Rules](#rules)
2. [Routing](#routing)
3. [Ariyasacca reference](#ariyasacca-reference)
4. [Fallbacks](#fallbacks)

## Rules

1. Step 0 (`references/setup.md`) has already checked which Skills are installed. Use only those.
2. Load a Skill with the Skill tool in the parent session. Subagents cannot load Skills: pass them the parts they need (method, checklist, file path to read).
3. Report `Used` only when a Skill was actually loaded and applied; otherwise `Unavailable / fallback`.
4. Follow a Skill only where it fits War Room's read-only mission. Skip any step that writes files, commits, changes Jira, or hands off to an implementation Skill.
5. Prefer one Skill per phase rather than loading every Skill.

## Routing

| Step | Situation | Skill | Why |
|---|---|---|---|
| 1–2 | Jira search and ticket details | `atlassian-mcp` | JQL, issue fields, linked pages |
| 3 | Acceptance criteria missing or vague | `feature-forge` | Turn the ticket into testable requirements |
| 4 | Undocumented legacy flow | `spec-miner` | Extract behaviour, APIs and dependencies from code |
| 4 | Change touches a shared table/column, DTO/API field, route, client call or constant | `impact-analysis` | Find consumers in other repos and grade the evidence |
| 5 | Bug, error, wrong data | `debugging-wizard` | Hypothesis-driven trace from symptom to cause |
| 5 | Separate symptom from cause, avoid unsupported certainty | `buddhist-method` + Ariyasacca reference | Evidence discipline for the diagnostician |
| 6 | Solution options | `war-room-brainstormer` (agent, no Skill) | Compare approaches against evidence |
| 6–7 | Cross-service flow or service boundary design (optional) | `microservices-architect` | Only when the ticket changes boundaries |
| 6–7 | REST contract change (optional) | `api-designer` | Only when an API contract changes |
| 8 | Challenge the recommendation and plan | `the-fool` | Pre-mortem, hidden assumptions, missed repos |

Implementation Skills (plan execution, TDD, subagent-driven development) are not used: War Room is planning-only.

## Ariyasacca reference

The diagnostician uses the original `buddhist-method/references/ariyasacca-debug.md`. Its path is `ariyasacca_path` in `config.md`, set by Step 0.

- When the path exists, pass it and the `buddhist-method` `SKILL.md` path to `war-room-diagnostician`, which reads both before analysing. Report the path that was read.
- When it is `unavailable`, say so, then apply the fallback below without attributing it to the missing file. Do not paraphrase the file as though it was read.

Fallback reasoning labels (not a reproduction of the original file):

- Symptom observed: What fails, where, and under which conditions?
- Candidate causes: What mechanisms could explain it? Which are mutually exclusive?
- Evidence gaps: What observation would falsify each cause?
- Resolution conditions: What must be true for the problem to be considered resolved?
- Verification: What tests or measurements would demonstrate durable resolution?

## Fallbacks

If a Skill is unavailable and the user agreed to continue without it, the matching War Room step still applies its straightforward analytical method. State the fallback in the report.
