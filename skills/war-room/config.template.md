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
  <!-- which branch new ticket work starts from, e.g. "from origin/develop" -->

## Filled in by setup

- ariyasacca_path: <<FILL>>
  <!-- path to buddhist-method/references/ariyasacca-debug.md; setup finds it -->

## Optional (leave "none" if not needed)

- environments: none
  <!-- names and hosts, e.g. "dev = dev.example.com; uat = uat.example.com" -->
- team_rules: none
  <!-- rules a plan must respect, e.g. "data changes go through the data-import repo, never in migrations" -->
- report_language: Thai
  <!-- language of the report; technical names stay in English -->
