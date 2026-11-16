---
name: impact-analysis
description: Source-code blast-radius analysis before changing something other code depends on. Use when a change looks small but touches a shared table or column, an entity, DTO or API field, a route or gateway mapping, an HTTP client call, a shared constant, enum, base class, config key or generated artifact, or when the user asks "what uses this?", "what can this break?", or "is this safe to change?". Maps callers, consumers in other repositories, schemas, contracts, tests, generated artifacts and runtime behavior, and grades how well each claim is proven. Not for chaos engineering or failure injection (use chaos-engineer) and not for designing new service boundaries (use microservices-architect).
metadata:
  source: adapted from the `blast-radius` skill in pstack (https://github.com/cursor/plugins/tree/main/pstack), MIT, Copyright (c) 2026 Lauren Tan
---

# Impact Analysis

Answer one question before the edit: this change looks small, so what else can it break?

Listing callers is the easy half. The job is the breakage a symbol search does not show: a native query naming the column, a client in another repository reading the field, a report, a cached value, a job that runs at night.

This skill is read-only analysis. It never widens the change: anything it finds outside the task is reported, not fixed, and the repository guardrails in `CLAUDE.md` (smallest change, existing conventions first, no modernization) still decide what gets edited.

## When to skip

Skip it when the thing being changed has no existing consumers: new code, a private method whose callers are all in the diff, a test-only change. Say in one line that it was skipped and why.

## Steps

1. **State the change exactly.** Name the symbol, field, column, route or key, and the kind of change: rename, removal, type change, new required input, changed default, changed meaning with the same shape. A changed meaning is the most dangerous kind because nothing fails to compile.

2. **Name the fact the change is safe because of.** One sentence, such as "nothing outside this service reads `visit_status`" or "every caller already passes a non-null id". The rest of the analysis exists to prove or break that sentence.

3. **Read what the repository already says.** Check the repository's `CLAUDE.md` for sections on connections, callers and gotchas, and use a repository-local impact agent or command when one exists (for example a `change-impact` agent) for the in-repository part.

4. **Trace consumers, then look where search stops.** Work down this list and record what was checked, including the lines that came back empty.

   | Surface | What to look for |
   | --- | --- |
   | Same repository | Callers, implementations and overrides; references by string rather than by symbol: JPQL and native SQL, projection getters, mapper configuration, JSON property names and naming strategies, template bindings, form definitions, translation and permission keys |
   | Other repositories | HTTP clients calling the endpoint (Feign, WebClient, RestTemplate, Angular services, PHP and Node callers), gateway or proxy route configuration, constants and enums duplicated across services. In a multi-repository workspace search the sibling repositories, not only the current one |
   | Database | Other services reading or writing the same table or column, migrations, data-import scripts, views, audit or history tables, reports and SQL exports, indexes that depend on the column |
   | Contracts | Request and response field names, nullability and required fields, enum values, error shape, pagination, OpenAPI or Swagger output, message formats such as HL7 segments |
   | Generated artifacts | Generated mappers, clients, typings and bundles. Find the source or generator; never plan an edit to the generated file |
   | Runtime | Per-environment configuration, feature flags, scheduled jobs, caches and their keys, transactions and locks, async listeners, ordering and timing, permissions |
   | Tests | Which tests exercise the changed behavior, and which consumers have no test that would notice |

5. **Grade each claim.** Say where the evidence for each one stopped:

   1. Assumed. Worth nothing; label it as a guess.
   2. Pointed at a real `file:line`.
   3. Showed the bad case cannot happen (every caller read, every writer of the column found).
   4. Ran a check that would fail loudly: a test, a query, a script, a build of the consumer.
   5. Reproduced on the running system.

   Push the one fact from step 2 as far up this ladder as is practical. Never invent a caller or cite a line that was not read. Write "not checked" for a surface that was not searched.

## Output

```
Change: <what is changing and the kind of change>
Safe because: <the one fact> — evidence level <1-5>, or "unproven"

Affected
- <file:line or repository/path> — <how it breaks> — likelihood / cost — <what to update or check>

Cleared
- <surface> — <what was searched and found safe>

Not checked
- <surface> — <why>

Before merging: <the cheapest check that would catch the worst item>
```

Keep it short. For a low-risk change the whole report is a few lines; do not pad it to fill the template.
