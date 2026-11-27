# svgkit

`tools/svgkit.py` holds the SVG primitives every Landing Loop sample page draws with, so twelve repos draw in one visual family: inline SVG, 1.5px strokes, 4px corners, mono labels, the Leader Report template's colour variables, brass for a person's call, grey with a spark for agent work, and green or red only beside the printed word landed or stalled. Standard library only, Python 3.11 or later. Output is byte-reproducible.

did-it-land and decision-record are the reference pages for the scorecard rows (1.1.0). Copy from them.

## Scorecard rows (1.1.0, 2026-11-27)

Every visual follows the grammar of the outcome scorecard on dacard.ai/update: HTML and CSS rows, not one scaled SVG.

- One row: name | picture | figure | word, split by 1px hairlines; one mono column head; rows pad 14px; columns 32px apart. Below 560px a row stacks: name and word on one line, the figure under them, the picture under that.
- Sizes as rendered: Geist Mono 12px for every label, figure and word; Geist 14px for names; nothing else. The CSS writes them as `calc(12px / var(--sc-z))`, so a page under a zoom sets `--sc-z` and keeps them.
- Four pictures, each a fixed-height SVG with no viewBox and no text: `range_line` (12px: grey prior dot, status dot, a target tick, no band), `paired_bars` (plan grey above actual ink, 6px each with a 2px gap, scaled to the largest value, the part past plan hatched), `share_bar` (6px), `pips` (8px).
- Words are text, never boxed chips: `status_mark` (the only green or red), `check_word`, `person_call` (brass text and a small person mark).
- One frame: `sc_frame` writes the head (section label, legend, Illustrative tag top right), the column head, the rows and one caption line, with hairlines top and bottom and no box. role="img" with an aria-label that states the answer.

```python
rows = [sk.sc_row("Quote drafting",
                  picture=sk.range_line(prior=21.67, actual=43, target=40, status="landed"),
                  figure=sk.figure_line("43%", prior="21.67%", target="40%"),
                  word=sk.status_mark("landed") + sk.check_word("cost over budget"))]
frame = sk.sc_frame(rows, label="Quote drafting landed.", title="Scorecard",
                    head=["Project", "", "Before → now · target", "Status"],
                    legend=sk.legend("prior", "average before launch") + sk.legend("target", "target"),
                    caption="One row per project.")
```

Put `svgkit.SCORECARD_CSS` in the page's `<style>` after `svgkit.CSS`. In the page's tests, assert `svgs_with_text(page) == []`, `scaled_svgs_in(page) == []`, `boxes_in_frames(page, css) == []` and that `font_sizes(css)` is only `var(--sc-m)` and `var(--sc-n)`. Then measure in a browser at 1280 and 390: every text node in a frame renders 12 or 14px.

## Vendor it

1. Copy the file unchanged into the skill's vendor folder, the one its ruff config already excludes (for example `skills/<name>/scripts/vendor/svgkit.py`). Never edit it there.
2. Pin it in the skill's `VENDORED.json` under a `landing-loop` entry, beside the Leader Report pins:

```json
"landing-loop": {
  "repository": "https://github.com/darrencard/landing-loop",
  "commit": "<40-character landing-loop commit that holds this svgkit.py>",
  "files": {
    "scripts/vendor/svgkit.py": {"from": "tools/svgkit.py", "sha256": "<sha256 of the file>"}
  }
}
```

Get both values with `git -C landing-loop log -1 --format=%H -- tools/svgkit.py` and `shasum -a 256 tools/svgkit.py`.

3. Extend the skill's vendored-file test to check this pin too (eval-kit's `test_every_vendored_file_matches_its_pin` and did-it-land's `test_vendored_files_match_their_pins` do).
4. To update: copy again from a newer commit, then update the commit and hash. Regenerate the sample and check it still reproduces byte for byte.

## Use it

- Put `svgkit.CSS` in the page's `<style>`, after the template's stylesheet.
- Open the page with `page_header(skill, date=..., version=..., illustrative=...)`: mark, DACARD, skill name, date, version, blue Illustrative tag.
- (SVG primitives, before 1.1.0.) Draw each visual twice, `frame(..., variant="wide")` at 720 and `frame(..., width=TALL, variant="tall")` at 340, and wrap both in `figure(wide, tall, caption=...)`. The CSS shows the tall one under 760px. Small multiples that reflow use `variant="one"`.
- Every `frame` takes an aria-label that states the answer in one sentence.
- Draw only figures the page prints. In the page's tests, assert `svgkit.unprinted(page) == []`.
- Paint green or red only through `status_word()`.
- Give each SVG its own hatch pattern id: a pattern inside a hidden SVG does not paint.

## Functions

| Group | Functions |
|---|---|
| Numbers and text | `num`, `esc`, `join`, `scale`, `label_width`, `label`, `value`, `status_word` |
| Frame | `frame`, `figure`, `icon`, `defs`, `hatch_pattern`, `page_header`, `mark`, `CSS` |
| Lines and marks | `line_series`, `point`, `hollow`, `rule`, `target_line`, `target_tick`, `zone`, `deadline` |
| Bars and areas | `range_bar`, `hbar`, `hatched` |
| Grids and blocks | `dot_grid`, `timeline_row`, `tile`, `gate`, `chip`, `chip_width` |
| Who did it | `spark` (agent, grey), `person` (a person's call, brass) |
| Checks for tests | `texts_in`, `numbers_in`, `svgs_in`, `visuals_in`, `page_text`, `unprinted` |
| Scorecard rows (1.1.0) | `SCORECARD_CSS`, `sc_frame`, `sc_row`, `sc_note`, `legend`, `figure_line`, `range_line`, `paired_bars`, `share_bar`, `pips`, `status_mark`, `check_word`, `person_mark`, `person_call` |
| Scorecard checks | `font_sizes`, `svgs_with_text`, `frames_in`, `scaled_svgs_in`, `boxed_classes`, `boxes_in_frames` |

Tests: `python3 -m unittest discover -s tools -p "test_*.py"`.
