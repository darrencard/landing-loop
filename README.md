# Landing Loop: brief to board, one install

Six free Claude skills that take a bet from its landing brief to the board update, with every figure computed in code and sourced.

**Why it matters:** most teams can say what shipped. Few can say whether it landed. The loop asks that at every step, against the same brief.

## Install

Paste into Claude Code:

```
/plugin marketplace add darrencard/landing-loop
/plugin install landing-loop@landing-loop
```

That installs all six. Restart Claude Code, then paste: "Write a landing brief for one bet I'm working on, then tell me which Landing Loop step comes next."

## The loop

| Step | Skill | What it does |
|---|---|---|
| 00 Brief | Leader Report's landing-brief skill | Writes the landing brief every step reads |
| 01 Decide | bet-portfolio-review | Scores the roadmap against each bet's brief |
| 02 Spec | spec-auditor | Checks a PRD against its brief, pass or hold |
| 03 Build | eval-kit | Pass rate and autonomy rate for one AI feature, meets target or below target |
| 03 Build | cost-budget-check | Tokens per task and price per token, within budget or over budget |
| 04 Learn | did-it-land | Landed, watch or stalled, from your own data. The only step that sets a bet's status |
| 05 Report | Product & Technology Leader Report | The update, with an evidence ledger |

**How it connects:** one landing brief (problem, definition of good, non-goals, cost budget, the line) and one record per bet, `landing/<bet>.json`. Each skill writes its own section. The report reads them all.

## Go deeper

- Example deck: [dacard.ai/update](https://www.dacard.ai/update)
- How the skills connect: [CONTRACT.md](CONTRACT.md)
- Each skill installs on its own too: `/plugin install did-it-land@landing-loop`

MIT licence. Made by [Dacard](https://www.dacard.ai).
