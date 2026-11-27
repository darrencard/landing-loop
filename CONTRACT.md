# Landing Loop contract, November 2026

Eleven skills, the Product & Technology Leader Report among them, work as one loop on one landing brief. Two team skills sit outside it. Set 2026-11-26. Each skill keeps its own repo; this file is what they share.

| Step | Skill | Reads | Writes (its key in the loop record) |
|---|---|---|---|
| 01 Decide | bet-portfolio-review | briefs, roadmap | `portfolio` |
| 01 Decide | decision-record | brief, `portfolio` | `decisions` |
| 02 Spec | spec-auditor | brief, spec | `spec` |
| 03 Build | release-readiness | brief, `spec`, checks | `release` |
| 03 Build | cost-budget-check | brief, usage | `cost` |
| 03 Build | eval-kit | brief, traces, `cost` | `evals` |
| 04 Learn | did-it-land | brief, metric, the record so far | `landed` |
| 04 Learn | customer-signal-digest | brief, feedback, `landed` | `signals` |
| 04 Learn | postmortem | brief, incidents, the record so far | `postmortem` |
| 05 Report | Leader Report | the record | slides and ledger rows |
| 05 Report | board-qa-prep | the record | `board_qa` |

Record order (tools/sample.py in landing-loop): portfolio, decisions, spec, release, cost, evals, landed, signals, postmortem, board_qa. A skill reads only keys earlier in this order.

Outside the loop (team-level, no bet record): team-operations-read and ai-native-hiring-loop. They read the team, not a bet, and write no key. Set 2026-11-26.

Check words, so status words stay did-it-land's (set 2026-11-26):

| Skill | Check words |
|---|---|
| decision-record | open, decided, dropped, waiting longer than usual, past due (a passed decide-by date only); a decision's outcome is worked, pending or missed |
| release-readiness | ready to ship or hold, per check and per release; a waived check still reads hold |
| customer-signal-digest | problem still raised or problem not raised |
| postmortem | what changed (each with evidence) and who owns each fix (one owner and a due date) |
| board-qa-prep | answered or open for each likely question |

Acme people are roles, never invented names, in every sample (loop and team). The quote-drafting bet, which every sample follows, uses four: Head of Product, Quoting squad (decides the next step, as the brief says); Lead, Quoting squad; Tech lead, Quoting squad; Product manager, Quoting squad. Acme's other bets use the same forms for their own squad (Head of Product, Payments squad; Lead, Payments squad). A decider is a person's name or a role scoped to one team, written "<role>, <team>" (decision-record's rule).

## The brief

One format: the Linear project template in `product-engineering-update/skills/landing-brief/assets/project-template.md`, parsed by that skill's `scripts/landing_brief.py`. Vendor the parser at a pinned commit SHA (as spec-auditor and bet-portfolio-review already do). Never fork the format.

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
- A bet's status words are landed, watch or stalled only, and only did-it-land sets them (`landed.status`). Build checks use their own words: eval-kit says meets target, not confirmed: too close to call (the point estimate meets it but the 95% interval's low end does not), or below target; did-it-land's own noise flag says inside normal ups and downs, so no two skills share a check word; cost-budget-check says within budget or over budget for each budget line. Neither uses the status colours.
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
