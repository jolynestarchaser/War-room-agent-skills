# Complexity Estimation & Planning

## Contents

1. [Before estimating](#before-estimating)
2. [Complexity rubric](#complexity-rubric)
3. [Sizes and confidence](#sizes-and-confidence)
4. [Plan format](#plan-format)
5. [Risk and re-check](#risk-and-re-check)

## Before estimating

A ticket should have a coherent problem statement, a probable implementation owner, acceptance criteria and key dependencies. If facts are missing, estimate **provisionally** and list unknowns rather than assigning false precision.

## Complexity rubric

Score 0–3 on five dimensions; record evidence, not just the number:

| Dimension | 0 | 1 | 2 | 3 |
|---|---|---|---|---|
| Scope of code change | Single localized change | Several related files | Subsystem change | Broad refactor/new subsystem |
| Technical uncertainty | Well understood | Minor discovery | Important unanswered questions | Fundamental unknowns/prototype needed |
| Cross-repo/integration | None | One local boundary | One remote integration | Multiple repos/services/contracts |
| Data/security/operational risk | Negligible | Low, reversible | Moderate schema/auth/rollout risk | High-impact migration/security/availability risk |
| Verification effort | One focused check | Small test set | Integration/E2E coverage | Multi-system regression/rollout verification |

Sum known dimensions only when all five are assessed. If any dimension is indeterminate, label `Unscored — missing evidence` and give a provisional range or tee up a discovery spike.

## Sizes and confidence

| Total | Size | Interpretation |
|---|---|---|
| 0–3 | S | Localized and well understood |
| 4–6 | M | Several steps or modest dependency/risk |
| 7–10 | L | Significant breadth or multi-system coordination |
| 11–15 | XL | Decompose into smaller work before commitment |

Confidence: `High` = scope, ownership and verification approach grounded in evidence; `Medium` = credible but some unknowns; `Low` = weak repo evidence, uncertain requirements or untested critical hypothesis.

Do **not** translate T-shirt sizes to story points, engineer-days or deadlines without team calibration, capacity and historical velocity. Do not equate Jira priority with engineering complexity. Cite Jira's existing estimate separately.

## Plan format

For each repo (including shared contracts/testing where needed), provide an ordered plan:

1. **Discover/clarify:** unanswered questions, reproductions, owner approvals.
2. **Approach:** recommended option and reasons; include reversible smallest safe change.
3. **Implementation steps:** repo, target components/files if known, preconditions, blockers, success criteria; descriptive only, do not implement.
4. **Verification:** unit/integration/e2e/contract/security/migration checks required to meet acceptance criteria.
5. **Rollout & rollback:** if data, production, compatibility or operational risk warrants it.
6. **Dependencies:** ordering, parallelizable tasks and external owner coordination.

For planning avoid writing exact diffs or prescriptive code where evidence is insufficient. Separate confirmed target files from candidate paths.

Apply the team's rules from `config.md`: start each repo's work from `branch_rule` (or its release ref), respect every `team_rules` entry and each repo's `Repo rules` in the codebase map, and name the `environments` where verification happens. Flag any plan step that conflicts with a rule instead of silently dropping it.

## Risk and re-check

Flag security/privacy, backwards compatibility, schema changes, deployment windows, dependencies, concurrency and ownership boundaries. Give risk severity and one concrete mitigation. If a plan assumes a repo ownership not corroborated, return to the investigator; if it assumes a cause not verified, return to diagnostic discovery.
