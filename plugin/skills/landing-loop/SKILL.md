---
name: landing-loop
description: Routes a product or engineering leader to the right Landing Loop step. Use when someone asks where to start, which Dacard skill to use, or how to take a bet from landing brief to board update.
---

# Landing Loop

Six skills share one landing brief and one loop record (`landing/<bet>.json`). Each writes its own section; the Leader Report reads the record.

| Step | Use when | Skill |
|---|---|---|
| 1 Decide | The roadmap needs scoring against its briefs | bet-portfolio-review |
| 2 Spec | A PRD needs checking before build | spec-auditor |
| 3 Build | An AI feature needs evals, or its spend needs checking | eval-kit, cost-budget-check |
| 4 Learn | A shipped bet needs a landed, watch or stalled call | did-it-land |
| 5 Report | Leadership, the board or all staff need the update | product-engineering-update |

Start where the person is. With no brief yet, start at step 1 or write the brief with the Leader Report's landing-brief skill. Name the next step when a step finishes.
