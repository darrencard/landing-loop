# Landing Loop: brief to board, one install

Six free Claude skills that take a bet from its landing brief to the board update, with every figure computed in code and sourced.

**Why it matters:** most teams can say what shipped. Few can say whether it landed. The loop asks that at every step, against the same brief.

## Install

Paste into Claude Code:

```
/plugin marketplace add darrencard/landing-loop
/plugin install landing-loop@landing-loop
```

That installs all six. Restart Claude Code, then ask: "Where should I start with the Landing Loop?"

## The loop

| Step | Skill | What it does |
|---|---|---|
| 1 Decide | bet-portfolio-review | Scores the roadmap against each bet's brief |
| 2 Spec | spec-auditor | Checks a PRD against its brief, pass or hold |
| 3 Build | eval-kit | Pass rate, autonomy rate and cost per task |
| 3 Build | cost-budget-check | Tokens per task and price per token against the budget |
| 4 Learn | did-it-land | Landed, watch or stalled, from your own data |
| 5 Report | Product & Technology Leader Report | The update, with an evidence ledger |

**How it connects:** one landing brief (problem, definition of good, non-goals, cost budget, the line) and one record per bet, `landing/<bet>.json`. Each skill writes its own section. The report reads them all.

## Go deeper

- Example deck: [dacard.ai/update](https://www.dacard.ai/update)
- Each skill installs on its own too: `/plugin install did-it-land@landing-loop`

MIT licence. Made by [Dacard](https://www.dacard.ai).
