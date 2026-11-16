# FBI — Evidence Verification

Used by `/war-room fbi <KEY> [before|after]`, by `references/implement.md` (a baseline after branch prep, the after pass after review) and by `references/delivery.md`.

FBI checks whether the change **works**, one acceptance criterion at a time, and keeps the **evidence**: before and after captures with matching file names, plus a verdict table. Implementer reports and the senior review are claims about code; FBI's captures show behaviour.

## Contents

1. [Phases and where "before" comes from](#phases)
2. [Evidence plan](#evidence-plan)
3. [Capture by type](#capture-by-type)
4. [Safety](#safety)
5. [Verdict and fbi.md](#verdict-and-fbimd)

## Phases

Needs `tickets/<KEY>/spec.md` with status `approved` or later. FBI never changes the spec's Status; it appends a Log line.

- `before`: the behaviour without the change. Use the first source that applies and record which one you used:
  1. The user's running app on the ticket branch right after branch prep, while every repo's HEAD still equals its `Start commit` (check with `git -C <path> rev-parse HEAD` and `git -C <path> status --porcelain`, ignoring carried paths).
  2. An environment from `environments` in config.md that does not have the change yet. Ask the user which one and confirm it is running the base branch.
  If none applies, write `before: not captured (<reason>)`. A baseline is always captured, never rebuilt from code or memory.
- `after`: the user's running app with the change: each repo on branch `<KEY>` with the implemented diff present, or dev after deploy. Record the commit or deploy.
- No phase given: run `before` when `evidence/before/` is empty and the code is still at the start commit, otherwise `after`.

The user starts services. Ask for the base URL of each surface you need (the web app, the gateway, the API), check each with `curl -s -o /dev/null -w "%{http_code}" <url>`, and wait for the user if one is down.

## Evidence plan

Read the spec's `Evidence plan` under Verification. Older specs may not have one. In that case, derive it from the ACs and "User runs by hand", show it to the user, write it into the spec after they confirm, and log the change.

One row per check: `AC | type (ui / api / pdf / db / log) | target (URL and clicks, endpoint, PDF source, query) | test data | expected`. Every AC has at least one row, or a reason it cannot be checked here.

Test data uses test records only: an account, order or record id the spec or the user gives you, never real customer data.

## Capture by type

File names: `<AC>-<slug>.<ext>`, identical in `before/` and `after/` so each pair lines up (`AC2-sticker-print.png` in both). PNG is required for anything visual. SVG is kept whenever the source can give one.

- **ui:** chrome-devtools MCP: `navigate_page`, `wait_for` the expected text, then `take_screenshot` with `filePath` set to the evidence path (full page, or the element under test by `uid`). When the element under test is an inline `<svg>` (a chart, barcode, signature or icon), also save its `outerHTML` from `evaluate_script` as `.svg`. When the MCP is not connected, use the `chrome-devtools-cli` skill. When it reports `The browser is already running for …chrome-profile`, an earlier session's Chrome holds the profile: ask the user to close that window, then retry (the login usually survives). The user does the login in that browser; you never type credentials. To find uids, `take_snapshot` with `filePath` and grep that file; read API data with `get_network_request` and `responseFilePath`, so the page's menu is not repeated in context.
- **pdf:** save the PDF as `<AC>-<slug>.pdf`, then render each page with PyMuPDF:

  ```bash
  python -P - "<file.pdf>" <<'PY'
  import sys, pymupdf
  src = sys.argv[1]; doc = pymupdf.open(src); stem = src[:-4]
  for i, page in enumerate(doc, 1):
      page.get_pixmap(dpi=110).save(f"{stem}-p{i}.png")
      open(f"{stem}-p{i}.svg", "w", encoding="utf-8").write(page.get_svg_image())
  PY
  ```

- **api:** `curl -sS -D <name>.headers.txt -o <name>.json <url>`. Remove `Authorization` and cookie values from the saved headers. A response is evidence of the contract; a screen showing it is evidence of the feature, so capture both when the AC is about what the user sees.
- **db:** a read-only `SELECT`, its result saved as `.txt`.
- **log:** the relevant lines saved as `.txt`, with timestamps.

When a capture tool is unavailable, mark that row `not captured: <tool> unavailable` and ask the user to drop a screenshot into the folder. A file the user supplied is labelled `user-supplied` in the table.

## Safety

- FBI looks: navigation, viewing, `GET`, `SELECT`, opening a PDF. An action that writes (save, submit, `POST/PUT/DELETE`, sending to an external system, printing to a real printer) runs only after the user says yes to that exact step. On a shared environment (staging, UAT) the yes must name the environment, because its database is shared.
- FBI writes only under `tickets/<KEY>/evidence/` and the spec's Evidence plan and Log. It edits no code and changes no git state.
- Evidence can show personal or customer data. It stays in the workspace folder. Uploading or attaching it (Jira, a PR, any hosted page) is the user's own action.

## Verdict and fbi.md

Open every captured PNG with Read and compare it with the row's expected result. Write one line on what the image shows; a file that merely exists proves nothing.

- **Met:** the after evidence shows the expected behaviour. A before capture showing the old behaviour makes it stronger; without one, write `no baseline`.
- **Not met:** the after evidence contradicts the expected result. During `/war-room implement` this goes back as a fix round (`references/implement.md`, step 5 of Review), and FBI runs `after` again once the fix lands.
- **Not verifiable:** the check could not run here; say why and who can run it.

Write `tickets/<KEY>/evidence/fbi.md`:

```markdown
# FBI — <KEY>

- Before: <source: local start commit <sha> | env <name> (<url>, <branch/deploy>)>, <date> | not captured (<reason>)
- After: <source>, <date>

| AC | Check | Before | After | Verdict | Evidence |
|---|---|---|---|---|---|
| AC1 | <what was checked> | <one line seen> | <one line seen> | Met | before/AC1-x.png, after/AC1-x.png, after/AC1-x.svg |

## Not verified
- <AC or check>: <reason, who can run it>
```

FBI is done when every AC has a row with a verdict, and every verdict cites an artifact path or the reason it is Not verifiable. Append `YYYY-MM-DD fbi <phase>: <n> Met, <n> Not met, <n> Not verifiable` to the spec's Log. Then report the table to the user in `report_language` with the evidence folder path.
