# Acme: one bet through the loop

Acme is an invented company (invoicing software for trades businesses). Every figure is illustrative.

`briefs/` holds the canonical landing briefs every skill's sample reads. The bet followed end to end is `quote-drafting`. Each skill renders its own sample from these briefs and writes its key into `landing/quote-drafting.json`; `tools/sample.py` runs them in loop order.

## The timeline

The record reads in loop order, and the dates follow it. Each step writes only its own key; a figure a later step owns is absent until that step runs.

| Date | Step | Key | What it says |
|---|---|---|---|
| 2026-07-20 | 00 Brief | `brief` | The brief is written: bar 40% quote draft acceptance by 2026-11-15, 9,000 tokens per task at $0.000003 |
| 2026-07-27 | 01 Decide | `portfolio` | Quote drafting's brief is complete (14 of 14); no spec yet, so spec-auditor is next |
| 2026-07-27 | 01 Decide | `decisions` | 3 decided (build now, approve before send, prices from the price book); 2 open (rollback trigger, model tier), 1 past due |
| 2026-08-03 | 02 Spec | `spec` | The PRD holds on two findings (rollback trigger, eval timing) |
| 2026-09-05 | 03 Build | `release` | v1.0 is ready to ship: 6 of 7 checks ready, the open-bugs check on hold under a waiver to 2026-09-19, both spec holds closed |
| 2026-09-07 | | | Quote drafting ships |
| 2026-11-15 | 03 Build | `cost` | 1 to 14 November: all three budget lines over budget, driver vendor-a/xl |
| 2026-11-15 | 03 Build | `evals` | v1.4's held-out pass rate is 80%, meets target. Cites cost-budget-check: $0.0338 per task |
| 2026-11-26 | 04 Learn | `landed` | Landed: 43% against the 40% bar, 41% at the date |
| 2026-11-26 | 04 Learn | `signals` | Problem still raised: 7 signals from 7 accounts say quote drafts still miss line items |
| 2026-11-26 | 04 Learn | `postmortem` | Two incidents; the long-draft routing to vendor-a/xl stayed in place after the first. 4 fixes, each with one owner and a due date |
| 2026-11-26 | 05 Report | `board_qa` | 17 likely board questions: 13 answered from the record, 4 open with an owner |

People are named by role (Head of Product, Quoting squad; Quoting squad lead), as the brief names who decides.

Only did-it-land sets landed, watch or stalled. The build checks use their own words (meets target, within budget, over budget).

## Versions

Each record names the skill version that wrote it, as that skill's code says: bet-portfolio-review, spec-auditor, cost-budget-check and did-it-land 0.3.1, eval-kit 0.3.3, and decision-record, release-readiness, customer-signal-digest, postmortem and board-qa-prep 0.3.0. `marketplace.json` pins the released versions, so it lags the record until those releases are cut. The Leader Report reads the record and writes none of it.
