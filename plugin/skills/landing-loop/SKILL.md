---
name: landing-loop
description: Routes a product or engineering leader to the right Landing Loop step. Use when someone asks where to start, which Dacard skill to use, or how to take a bet from landing brief to board update.
---

# Landing Loop

Eleven skills share one landing brief and one loop record (`landing/<bet>.json`). Each writes only its own key and reads only the keys before it; the Leader Report reads the whole record. Two team skills sit outside the loop.

| Step | Use when | Skill |
|---|---|---|
| 00 Brief | A bet has no landing brief yet | the Leader Report's landing-brief skill |
| 01 Decide | The roadmap needs scoring against its briefs | bet-portfolio-review |
| 01 Decide | A call needs logging with who made it, or open calls are waiting | decision-record |
| 02 Spec | A PRD needs checking before build | spec-auditor |
| 03 Build | A release needs a ready to ship or hold call | release-readiness |
| 03 Build | An AI feature's spend needs checking against its budget | cost-budget-check |
| 03 Build | An AI feature needs evals | eval-kit |
| 04 Learn | A shipped bet needs a landed, watch or stalled call | did-it-land |
| 04 Learn | You need to know whether customers still raise the problem | customer-signal-digest |
| 04 Learn | A bet or incident needs a blameless review with owned fixes | postmortem |
| 05 Report | Leadership, the board or all staff need the update | product-engineering-update |
| 05 Report | The board's likely questions need answers from the record | board-qa-prep |
| Team | How the team works needs reading against Team Operations | team-operations-read |
| Team | A hiring loop for AI-fluent roles needs designing or scoring | ai-native-hiring-loop |

Only did-it-land sets landed, watch or stalled. Every other skill prints it and uses its own check words: meets target or below target (eval-kit), within budget or over budget (cost-budget-check), ready to ship or hold (release-readiness), pass or hold (spec-auditor), problem still raised or not raised (customer-signal-digest), answered or open (board-qa-prep).

Start where the person is. With no brief yet, start at 00 and write the brief with the Leader Report's landing-brief skill, then 01 Decide. Name the next step when a step finishes.
