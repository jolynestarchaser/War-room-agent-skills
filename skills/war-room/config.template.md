# War Room config

Setup copies this file to `<workspace>/.claude/war-room/config.md` and asks you for every `<<FILL>>` value.
War Room will not start an investigation while a required `<<FILL>>` remains.
Keep this file out of public repositories: it describes your team's systems.

## Required

- jira_site: <<FILL>>
  <!-- e.g. yourcompany.atlassian.net -->
- jira_projects: <<FILL>>
  <!-- comma-separated project keys to triage, e.g. ABC, XYZ. Write "all" for no filter. -->
- workspace_root: <<FILL>>
  <!-- absolute folder that contains your repositories -->
- repos: <<FILL>>
  <!-- one line per repo: name | absolute path. Setup can scan workspace_root for git repos and ask you to confirm the list. -->
- branch_rule: <<FILL>>
  <!-- which branch new ticket work starts from, e.g. "from origin/develop", or per repo: "api: origin/main; web: origin/release" -->

## Codebase knowledge (setup asks)

- codebase_map: .claude/war-room/explore.md
  <!-- the file War Room reads first to know what each repo does and how they connect. Default: War Room builds and owns it. -->
- codebase_map_owner: war-room
  <!-- "war-room", or the tool/person that maintains the map (e.g. "Obsidian vault, refresh with /my-kb update"). Any other value: War Room reads the map and never rebuilds it. -->
- knowledge_sources: none
  <!-- other docs to read before investigating, one per line: path | what it holds. e.g. "docs/architecture.md | service boundaries", "/kb/Gotchas | known traps per repo" -->

## Filled in by setup

- ariyasacca_path: <<FILL>>
  <!-- path to buddhist-method/references/ariyasacca-debug.md; setup finds it -->

## Optional (leave "none" if not needed)

- release_ref_pattern: none
  <!-- remote branches where released work lands, when the base moves every sprint, e.g. "refs/remotes/origin/release-*". War Room takes the newest by commit date as each repo's release ref. "none" = the base from branch_rule. -->
- environments: none
  <!-- names and hosts, e.g. "dev = dev.example.com; uat = uat.example.com" -->
- team_rules: none
  <!-- rules a plan, an implementer and a commit must respect, e.g. "data changes go through the data-import repo, never in migrations", "test files stay uncommitted", "no AI attribution in commits" -->
- standing_local: none
  <!-- per repo, paths that are always dirty (local config, notes) and carried onto every branch without asking, e.g. "web: package.json, untracked *.md" -->
- gateway_routes: none
  <!-- file mapping API paths to services (an API gateway config); read to find which service really handles an endpoint -->
- implementer_model: sonnet
  <!-- model for implementer and map subagents: a cheaper, faster model than the session's -->
- pr_host: none
  <!-- where the user opens PRs, e.g. GitHub, Bitbucket, GitLab. War Room only drafts the body. -->
- report_language: English
  <!-- language of reports and grilling questions; technical names stay in English -->
