# svgkit

`tools/svgkit.py` holds the SVG primitives every Landing Loop sample page draws with, so twelve repos draw in one visual family: inline SVG, 1.5px strokes, 4px corners, mono labels, the Leader Report template's colour variables, brass for a person's call, grey with a spark for agent work, and green or red only beside the printed word landed or stalled. Standard library only, Python 3.11 or later. Output is byte-reproducible.

did-it-land and eval-kit are the reference pages. Copy from them.

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
- Draw each visual twice, `frame(..., variant="wide")` at 720 and `frame(..., width=TALL, variant="tall")` at 340, and wrap both in `figure(wide, tall, caption=...)`. The CSS shows the tall one under 760px. Small multiples that reflow use `variant="one"`.
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

Tests: `python3 -m unittest discover -s tools -p "test_*.py"`.
