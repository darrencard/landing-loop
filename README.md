# Landing Loop: brief to board, one install

Free Claude skills that take a bet from its landing brief to the board update, with every figure computed in code and sourced.

**Why it matters:** most teams can say what shipped. Few can say whether it landed. The loop asks that at every step, against the same brief.

## Install

Paste into Claude Code:

```
/plugin marketplace add darrencard/landing-loop
/plugin install landing-loop@landing-loop
```

That installs every skill marked "in the bundle" below. Restart Claude Code, then paste: "Write a landing brief for one bet I'm working on, then tell me which Landing Loop step comes next."

## The loop

Eleven skills share one brief and one record per bet, the Product & Technology Leader Report among them. Two more, below, read the team. Thirteen in all.

| Step | Skill | What it does | Record key | In the bundle |
|---|---|---|---|---|
| 00 Brief | Leader Report's landing-brief skill | Writes the landing brief every step reads | `brief` | yes |
| 01 Decide | bet-portfolio-review | Scores the roadmap against each bet's brief | `portfolio` | yes |
| 01 Decide | decision-record | Logs each call with who decided and their words: open, decided, dropped, waiting longer than usual or past due | `decisions` | yes |
| 02 Spec | spec-auditor | Checks a PRD against its brief, pass or hold | `spec` | yes |
| 03 Build | release-readiness | Ready to ship or hold, per check and per release; a waived check still reads hold | `release` | yes |
| 03 Build | cost-budget-check | Tokens per task and price per token, within budget or over budget | `cost` | yes |
| 03 Build | eval-kit | Pass rate and autonomy rate for one AI feature: meets target, not confirmed: inside noise, or below target | `evals` | yes |
| 04 Learn | did-it-land | Landed, watch or stalled, from your own data. The only step that sets a bet's status | `landed` | yes |
| 04 Learn | customer-signal-digest | What customers say about the bet: problem still raised or problem not raised | `signals` | yes |
| 04 Learn | postmortem | What changed, each with evidence, and one owner and due date per fix | `postmortem` | yes |
| 05 Report | board-qa-prep | The board's likely questions, each answered from the record or open with an owner | `board_qa` | yes |
| 05 Report | Product & Technology Leader Report | The update, with an evidence ledger | reads the record | yes |

**How it connects:** one landing brief (problem, definition of good, non-goals, cost budget, the line) and one record per bet, `landing/<bet>.json`. Each skill writes only its own key and reads only the keys before it. The report reads them all.

## For the team, outside the loop

Two skills read the team that runs the bets, not a bet, so they write no record key.

| Skill | What it does | In the bundle |
|---|---|---|
| team-operations-read | Scores how the team works against the Team Operations framework, from GitHub, Linear or CSV exports | yes |
| ai-native-hiring-loop | Designs a structured hiring loop for an AI-fluent PM, designer or engineer and combines interview scores in code | yes |

## Go deeper

- Example deck: [dacard.ai/update](https://www.dacard.ai/update)
- How the skills connect: [CONTRACT.md](CONTRACT.md)
- Each skill installs on its own too: `/plugin install did-it-land@landing-loop`

MIT licence. Made by [Dacard](https://www.dacard.ai).

Claude and Claude Code are trademarks of Anthropic, PBC. These skills are independent and not affiliated with or endorsed by Anthropic.
