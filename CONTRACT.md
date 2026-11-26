
# Landing Loop contract, November 2026

Five skills and the Product & Technology Leader Report work as one loop on one landing brief. Set 2026-11-26. Each skill keeps its own repo; this file is what they share.

| Step | Skill | Reads | Writes (its key in the loop record) |
|---|---|---|---|
| 01 Decide | bet-portfolio-review | briefs, roadmap | `portfolio` |
| 02 Spec | spec-auditor | brief, spec | `spec` |
| 03 Build | eval-kit | brief, traces | `evals` |
| 03 Build | cost-budget-check | brief, usage | `cost` |
| 04 Learn | did-it-land | brief, metric, the record so far | `landed` |
| 05 Report | Leader Report | the record | slides and ledger rows |

## The brief

One format: the Linear project template in `product-engineering-update/skills/landing-brief/assets/project-template.md`, parsed by that skill's `scripts/landing_brief.py`. Vendor the parser at a pinned commit SHA (every skill in the loop does). Never fork the format.

## The loop record

One JSON file per bet: `landing/<bet-slug>.json` in the user's working folder.

```json
{
  "schema": "landing-loop/1",
  "bet": "quote-drafting-assistant",
  "brief": {"path": "...", "sha256": "..."},
  "portfolio": {...},
  "spec": {...},
  "evals": {...},
  "cost": {...},
  "landed": {...}
}
```

Rules:

- Each skill writes only its own key and keeps every other key exactly as it found it.
- Every figure inside a key carries `value`, `unit`, `source`, `window` (from, to) and `as_of`. No figure without a source.
- A bet's status words are landed, watch or stalled only, and only did-it-land sets them (`landed.status`). Build checks use their own words: eval-kit says meets target or below target; cost-budget-check says within budget or over budget for each budget line. Neither uses the status colours.
- `evals` uses the Leader Report's evals columns (`tasks`, `tasks_unassisted`, pass rate) so the report reads it unchanged.
- `cost` states tokens per task and price per token as two figures, plus the budget from the brief.
- `landed.status` is computed in code from the brief's bar and date, never written by the model.

## Data in

Live first, CSV as the fallback. Reuse the Leader Report collectors (`skills/product-engineering-update/scripts/from_*.py`), vendored at a pinned SHA, before writing a new one.

## Output for leaders

Anything a leader reads renders as one self-contained HTML page in the Leader Report style guide (`assets/template.html`, `references/design.md`). Markdown stays as the plain-text twin.

## One owner per figure (added 2026-11-26)

| Figure or check | Owner | Everyone else |
|---|---|---|
| Cost per task, tokens per task, price per token | cost-budget-check (`cost`) | eval-kit reads `cost` and cites it. With no `cost` key it says "cost not checked: run cost-budget-check" and prints no cost figure |
| Pass rate, autonomy rate | eval-kit (`evals`) | Others read `evals` |
| Brief completeness (is each part of the brief present) | `landing_brief.py`, vendored byte-identical (sha256 `2d13573543c74ebe…`) | spec-auditor and bet-portfolio-review both call the parser's own check and add no keyword list of their own for brief parts. spec-auditor checks the spec against the brief; bet-portfolio-review checks the portfolio of briefs |
| Landed, watch or stalled | did-it-land (`landed`) | Others print it, never compute it |
| Open decisions | decision-record | Writes the Leader Report's decision format so the report's decision slide reads it unchanged |
