---
name: landing-loop
description: Routes a product or engineering leader to the right Landing Loop step. Use when someone asks where to start, which Dacard skill to use, or how to take a bet from landing brief to board update.
---

# Landing Loop

Six skills share one landing brief and one loop record (`landing/<bet>.json`). Each writes its own section; the Leader Report reads the record.

| Step | Use when | Skill |
|---|---|---|
| 00 Brief | A bet has no landing brief yet | the Leader Report's landing-brief skill |
| 01 Decide | The roadmap needs scoring against its briefs | bet-portfolio-review |
| 02 Spec | A PRD needs checking before build | spec-auditor |
| 03 Build | An AI feature needs evals, or its spend needs checking | eval-kit, cost-budget-check |
| 04 Learn | A shipped bet needs a landed, watch or stalled call | did-it-land |
| 05 Report | Leadership, the board or all staff need the update | product-engineering-update |

Only did-it-land sets landed, watch or stalled. eval-kit says meets target or below target; cost-budget-check says within budget or over budget.

Start where the person is. With no brief yet, start at 00 and write the brief with the Leader Report's landing-brief skill, then 01 Decide. Name the next step when a step finishes.
