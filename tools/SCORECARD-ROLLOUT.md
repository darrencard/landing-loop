# Scorecard rollout: one skill, step by step

How a Landing Loop skill moves its sample page to the scorecard grammar. The grammar is the outcome scorecard on dacard.ai/update, built here as svgkit 1.2.0 rows. did-it-land 0.3.4 and decision-record 0.3.3 are the reference pages: read their `scripts/render_html.py` and their page tests before you start. Every skill follows the same steps in the same order, so several people can work in parallel and get the same result.

## 0. Before you start

- Work in the skill's repository, on main, with a clean tree. Use Python 3.11 or later (`python3.12` on most Macs).
- Read `tools/SVGKIT.md` (the API) and this file to the end.
- Find your skill's row in the mapping table (step 3). If it is not there, stop and ask. Do not invent a new picture.

## 1. Vendor and pin svgkit

1. Copy `tools/svgkit.py` from landing-loop main, unchanged, to `skills/<name>/scripts/vendor/svgkit.py`. Never edit it there.
2. Get the pin values: `git -C ~/landing-loop log -1 --format=%H -- tools/svgkit.py` and `shasum -a 256 ~/landing-loop/tools/svgkit.py`.
3. In `skills/<name>/VENDORED.json`, set `landing-loop.commit` to the 40-character commit and `files["scripts/vendor/svgkit.py"].sha256` to the hash.
4. If a test asserts the commit literally (decision-record's `test_svgkit_matches_its_landing_loop_pin` does), update it.

## 2. Build the page's CSS and frame

- Put `svgkit.SCORECARD_CSS` in the page's `<style>`, after `svgkit.CSS` and before the page's own rules: `stylesheet() + sk.CSS + sk.SCORECARD_CSS + PAGE_CSS`.
- Keep the shared header (`sk.page_header`). It is not deprecated.
- Write one `sk.sc_frame(rows, label=..., title=..., head=[4 column heads], legend=..., caption=..., illustrative=...)` per visual.
  - `label`: one sentence that states the answer (the verdict). It becomes the aria-label.
  - `title`: the section label in the frame head, in plain words ("Scorecard", "Days to decide", "Checks").
  - `head`: four mono column heads, name | picture | figure | word. Leave the picture head empty when the legend says it.
  - `legend`: `sk.legend(kind, text)` marks, each printed once: `plan`, `actual`, `over`, `prior`, `target`. A reference value (a plan, a usual time) prints here once, never per row.
  - `caption`: one plain sentence that says how to read the rows.
  - `word_max`: leave it at the default (180px) unless the word column holds long roles that should wrap sooner.
- Rows: `sk.sc_row(name, picture=..., figure=..., word=...)`. The name is plain text. A group with no rows becomes one `sk.sc_note("...")` line, never an empty row.
- Delete the old picture code: anything calling `frame`, `figure`, `label`, `value`, `status_word`, `chip`, `icon` or any other name in `svgkit.LEGACY`. Those calls now raise a DeprecationWarning, and the tests in step 5 turn it into a failure.

## 3. Map your data to a picture

Four pictures only. Use the one your row names; draw no other.

| Skill | Rows | Picture (svgkit) | Figure (`figure_line`) | Word |
|---|---|---|---|---|
| Portfolio review | one per project, ranked | `pips(filled, 4)`: plan, owner, work linked, cost budget | `11 of 14` | next step as `check_word`; rank 1 `check_word("DO FIRST", ink=True)` |
| Decision record | one per decision | `paired_bars(plan, days, top=frame max, hatch_id=unique)` | `28 DAYS` | `person_call(decider)` |
| Spec auditor | one per check, holds first | none (`picture=""`); a frame-level `share_bar` row first: "11 of 14 pass" | line refs | `check_word("HOLD", ink=True)` or `check_word("PASS")` |
| Release readiness | one per gate | none; a `share_bar` row first: "6 of 7 ready" | expiry date for a waiver | `check_word("READY")` or `check_word("HOLD", ink=True)`; waiver approver `person_call` |
| Cost budget check | usage, price, cost per task; then over budget by model | `paired_bars(budget, actual, top=row max, hatch_id=...)` | `9,000 → 10,300 · +14%` | `check_word("OVER", ink=True)` or `check_word("WITHIN")` |
| Eval kit | one per version | `range_line` with the frame's domain (step 4) | `21 of 30` | `check_word("TOO CLOSE TO CALL")`, `check_word("MEETS TARGET")`, `check_word("BELOW TARGET", ink=True)` |
| Did it land? | one per project | `range_line(prior, actual, target, status, domain, relative=True)` | `prior → actual · TARGET x` | `status_mark(status)` and the cost word |
| Customer signals | still raised; gone | `share_bar(last30, total)` | `7 accounts · 5 in 30 days` | `check_word` |
| Postmortem | incidents, then fixes | incidents: `paired_bars(plan, time to fix, ...)`; fixes: none | hours or days | fixes: `person_call(owner)`, due as the figure |
| Board Q&A prep | open first, then answered | none; a `share_bar` row first: "13 of 15 answered" | due date or source | open: `person_call(owner)`; answered: `check_word("ANSWERED")` |
| Team operations read | one per area read | `pips(floor, 5, dashed=band width)` | `level 2 or below` | one row `check_word("START HERE", ink=True)`; unread areas as one `sc_note` |
| AI-native hiring loop | one per candidate | `range_line` with the frame's domain | `3.23 · TARGET 3.00 · RESTRAINT 2.33 < FLOOR 2.50` | `check_word("MEETS TARGET")` or `check_word("BELOW TARGET", ink=True)`; decider `person_call` in the head |

Rules that hold for every row:

- Green and red only through `status_mark` (landed, watch, stalled). Check words are muted, or ink when they need attention. Never a boxed chip.
- Brass only through `person_call` (an owner, a decider, an approver).
- Hatching only for over plan or over budget (`paired_bars` does it).
- A figure the picture draws must print in the figure line or the word. Never draw a value the page does not print.

## 4. One scale per frame

- Range lines: build the domain once per frame and pass it to every row.
  `domain = sk.frame_domain([(prior, actual, target) for each row])`, then `sk.range_line(..., domain=domain, relative=True)`. Each value reads as a share of its row's target, so every target tick lines up across the frame.
  Rows already in one unit (an eval pass rate, a hiring score) may use `relative=False` with `frame_domain(..., relative=False)`.
- Marks closer than 2.5% of the line are drawn 4px apart in value order. Equal values stay on one spot. You do nothing for this; never change a value to separate marks.
- Paired bars: `top` is the largest plan or actual in the frame (cost budget check: per row, because its three lines are in different units). Give each `paired_bars` call its own `hatch_id`.

## 5. Copy the tests

Copy these into the skill's page tests (did-it-land `evals/test_loop_live_html.py` class `Html`; decision-record `evals/test_loop.py` class `Page`), changing only names:

1. `svgkit.svgs_with_text(page) == []`: no text inside an SVG.
2. `svgkit.scaled_svgs_in(page) == []`: no picture with a viewBox.
3. `set(svgkit.font_sizes(css)) == {"var(--sc-m)", "var(--sc-n)"}`, with `--sc-m:calc(12px / var(--sc-z))` and `--sc-n:calc(14px / var(--sc-z))` in the CSS: labels 12px, names 14px.
4. `svgkit.boxes_in_frames(page, css) == []`, and no `class="chip"` before the engineers' fold: no box inside the frame.
5. `"position:absolute" not in svgkit.SCORECARD_CSS`: rows flow in a grid, so nothing overlaps.
6. `svgkit.legacy_in(page) == []`, and render the page under `warnings.simplefilter("error", DeprecationWarning)`: no legacy primitive.
7. For each status row: a `class="ac landed"` or `"ac stalled"` dot only in a row that prints `<span class="st landed">landed</span>` (or stalled).
8. One frame per visual (`len(svgkit.frames_in(page))`), one row per item, each row's figure line printed exactly, and the aria-label equal to the verdict.
9. For range lines: every `class="tg"` x is the same within a frame (one scale).
10. `svgkit.unprinted(page) == []` and the sample still reproduces byte for byte (the repo's existing sample test).

## 6. Regenerate, then check in a browser

1. Regenerate the sample (`python3.12 examples/acme/sample.py`) and run every test (`python3.12 -m unittest discover -s evals`).
2. Serve the sample folder: `~/.local/bin/python3.12 -m http.server <port> --directory examples/acme`, in the background.
3. Open the page at 1280 wide, paste `tools/scorecard-check.browser.js` (this repo) into the console, and read the table. Then do the same at 390 wide. Pass: every frame prints `sizes` with only 12 and 14, and 0 for `off`, `boxes` and `overlaps`, with `reach` 95 or more.
4. Look at the page next to www.dacard.ai/update at 1280 and 390. Rows split by hairlines, one mono head, the word on the right, the figure right-aligned, nothing larger than 12px inside the frame except names. Below 800px of frame width the rows stack: name and word on one line, the figure under them, the picture under that.
5. Stop the server.

## 7. Words and docs

- Public copy says project, target, the landing brief (defined once as "a one-page plan: what good looks like, by when, at what cost"), the project file, plan. SKILL.md tells Claude to use the user's own word if they say bet. Keep record keys, file names, flags and code identifiers as they are.
- No em dashes. British spelling.

## 8. Version and commit

1. Bump the patch version everywhere the repo's version test reads it (plugin.json, pyproject.toml, SKILL.md frontmatter, the script's VERSION, and the test itself).
2. Add a dated CHANGELOG entry that names the picture, the svgkit version and pin, and the new tests.
3. Regenerate the sample after the bump (the header prints the version) and rerun the tests.
4. Commit signed (`git log '--format=%G?' -1` prints G), ending the message with the repository's attribution line, and push main. No tags or releases unless asked.

## The site

The site's row kit is `components/skills/visuals/rows.tsx` in dacard-v0. It mirrors svgkit with the same class names, and `rows.test.tsx` checks its class structure against `tools/scorecard-golden.json`. When svgkit's markup changes, run `python3 tools/scorecard_golden.py`, copy the JSON to `components/skills/visuals/scorecard-golden.json` in the site, and make the site test pass. The site's browser check is `scripts/scorecard-rows.browser.js`. Site sizes are `calc(Npx / var(--zoom))`, so they render 12 and 14px under the 80% zoom above 768px.
