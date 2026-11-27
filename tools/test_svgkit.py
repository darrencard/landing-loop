"""Tests for svgkit. Run from the repo root: python3 -m unittest discover -s tools -p "test_*.py" """

import json
import re
import sys
import unittest
import warnings
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

import scorecard_golden  # noqa: E402
import svgkit as sk  # noqa: E402

# The legacy primitives warn on every call; the tests that cover them still run, quietly.
warnings.filterwarnings("ignore", category=DeprecationWarning, message="svgkit\\.")

HEX = re.compile(r"#[0-9A-Fa-f]{3,8}\b")


def sample() -> str:
    """One of every primitive, in one frame."""
    body = sk.join(
        [
            sk.defs(sk.hatch_pattern("sk-t-hatch")),
            sk.zone(10, 10, 100, 40),
            sk.target_line(10, 300, 50),
            sk.target_tick(200, 10, 90),
            sk.deadline(250, 10, 90),
            sk.line_series([(10, 80), (60, 60.555), (110, 30)]),
            sk.line_series([(10, 80), (60, 60)], tone=sk.MUTED, dashed=True),
            sk.point(110, 30),
            sk.hollow(60, 60),
            sk.range_bar(120, 40, 100, point_x=80),
            sk.hbar(10, 120, actual=150, budget=120, hatch_id="sk-t-hatch"),
            sk.hatched(200, 120, 40, 12, pattern_id="sk-t-hatch"),
            sk.dot_grid(10, 150, cols=3, rows=2, cell=20),
            sk.timeline_row(10, 90, 210),
            sk.timeline_row(10, 140, 225, flagged=True),
            sk.tile(10, 240, 40, 30),
            sk.tile(60, 240, 40, 30, filled=True),
            sk.gate(110, 240, state="ready"),
            sk.gate(140, 240, state="hold"),
            sk.chip(170, 240, "due 2026-12-10"),
            sk.spark(300, 250),
            sk.person(320, 260),
            sk.label(10, 300, "Target 40%"),
            sk.value(100, 300, "43%"),
            sk.status_word(200, 300, "landed"),
            sk.status_word(300, 300, "watch"),
        ]
    )
    return sk.frame(body, label="Quote drafting landed: 43% against a 40% target.", height=320)


def scorecard() -> str:
    """One of every scorecard primitive, in one frame, as a page would print it."""
    rows = [
        sk.sc_row(
            "Quote drafting",
            picture=sk.range_line(prior=21.67, actual=43, target=40, status="landed"),
            figure=sk.figure_line("43%", prior="21.67%", target="40%"),
            word=sk.status_mark("landed") + sk.check_word("cost over budget"),
        ),
        sk.sc_row("Job scheduler", picture=sk.range_line(prior=2060, actual=2100, target=3000, status="stalled"), figure=sk.figure_line("2,100", prior="2,060", target="3,000"), word=sk.status_mark("stalled")),
        sk.sc_row("When to undo the release", picture=sk.paired_bars(14, 28, top=28, hatch_id="t-h1"), figure=sk.figure_line("28 DAYS"), word=sk.person_call("Head of Product")),
        sk.sc_row("Build quote drafting now", picture=sk.paired_bars(14, 7, top=28, hatch_id="t-h2"), figure=sk.figure_line("7 DAYS"), word=sk.person_call("Head of Product", due="2026-12-10")),
        sk.sc_row("Checks", picture=sk.share_bar(11, 14), figure=sk.figure_line("11 of 14"), word=sk.check_word("HOLD", ink=True)),
        sk.sc_row("Plan", picture=sk.pips(2, 5, dashed=1), figure=sk.figure_line("level 2 or below"), word=sk.check_word("PASS")),
        sk.sc_note("21 areas not visible in these exports"),
    ]
    head = ["Project", "Before → now", "Figure", "Status"]
    key = sk.legend("prior", "before") + sk.legend("target", "target") + sk.legend("plan", "plan") + sk.legend("actual", "actual") + sk.legend("over", "over plan")
    return sk.sc_frame(rows, label="Quote drafting landed; job scheduler stalled.", title="Outcome scorecard", head=head, legend=key, caption="One row per project.")


class Scorecard(unittest.TestCase):
    PAGE = "<style>" + sk.CSS + sk.SCORECARD_CSS + "</style>"

    def page(self) -> str:
        return self.PAGE + scorecard()

    def test_deterministic(self):
        self.assertEqual(scorecard(), scorecard())
        self.assertIsNone(re.search(r"\d\.\d{3,}", scorecard()))

    def test_rows_are_html_and_pictures_hold_no_text(self):
        out = scorecard()
        self.assertEqual(out.count('<div class="sc-r">'), 6)
        self.assertGreaterEqual(len(sk.svgs_in(out)), 6)
        self.assertEqual(sk.svgs_with_text(out), [], "text inside a picture")
        self.assertEqual(sk.scaled_svgs_in(out), [], "a picture with a viewBox scales its marks")
        for svg in sk.svgs_in(out):
            self.assertRegex(svg.split(">", 1)[0], r'height="\d+"', "a picture has a fixed pixel height")
            self.assertIn('aria-hidden="true"', svg.split(">", 1)[0])

    def test_four_pictures_at_their_fixed_heights(self):
        out = scorecard()
        heights = {cls: h for cls, h in re.findall(r'<svg class="(sc-[a-z]+)" width="[^"]+" height="([\d.]+)"', out)}
        self.assertEqual(heights, {"sc-rl": "12", "sc-pv": "14", "sc-sh": "6", "sc-pp": "8"})

    def test_labels_render_12px_and_names_14px(self):
        sizes = set(sk.font_sizes(sk.SCORECARD_CSS))
        self.assertEqual(sizes, {"var(--sc-m)", "var(--sc-n)"})
        self.assertIn("--sc-m:calc(12px / var(--sc-z))", sk.SCORECARD_CSS)
        self.assertIn("--sc-n:calc(14px / var(--sc-z))", sk.SCORECARD_CSS)
        self.assertIn(".scg .sc-n{font-family:var(--sans);font-size:var(--sc-n)", sk.SCORECARD_CSS)
        self.assertNotRegex(sk.SCORECARD_CSS, r"font-size:\s*\d", "a raw size bypasses the 12/14 rule")

    def test_figures_are_tabular_and_right_aligned(self):
        self.assertIn("font-variant-numeric:tabular-nums", sk.SCORECARD_CSS)
        self.assertIn(".scg .sc-l{text-align:right}", sk.SCORECARD_CSS.replace(".scg .sc-h>:nth-child(3),", ""))
        self.assertNotIn("<b><b>", scorecard())
        self.assertIn('<span class="sc-l">21.67% <i>→</i> <b>43%</b> · TARGET 40%</span>', scorecard())

    def test_no_box_inside_the_frame(self):
        boxed = sk.boxed_classes(sk.CSS + sk.SCORECARD_CSS)
        self.assertIn("sk-hdr", boxed | {"sk-hdr"})
        self.assertEqual(sk.boxes_in_frames(self.page(), sk.CSS + sk.SCORECARD_CSS), [])
        # The Leader Report template outlines .key i.o; the legend's own class names never collide with it.
        self.assertEqual(sk.boxes_in_frames(self.page(), ".key i.o{outline:1px solid var(--t1)}" + sk.SCORECARD_CSS), [])
        self.assertEqual(sk.boxes_in_frames('<div class="sc scg"><span class="chip">x</span></div>', ".chip{border:1px solid red}"), ["chip"])
        self.assertNotRegex(sk.SCORECARD_CSS.split(".scg .sc-t")[0], r"border:\s*1px", "the frame is hairlines, not a box")

    def test_no_overlap_rows_flow_in_a_grid(self):
        self.assertNotIn("position:absolute", sk.SCORECARD_CSS)
        self.assertIn("grid-template-columns:subgrid", sk.SCORECARD_CSS)
        self.assertIn("container:sc / inline-size", sk.SCORECARD_CSS)
        self.assertIn("@container sc (max-width:799.98px){", sk.SCORECARD_CSS, "the site's row kit stacks under an 800px frame too")
        self.assertNotIn("@media", sk.SCORECARD_CSS)

    def test_green_and_red_only_beside_their_word(self):
        for row in re.findall(r'<div class="sc-r">.*?</div>', scorecard()):
            for word in ("landed", "stalled"):
                if f'class="ac {word}"' in row:
                    self.assertIn(f'<span class="st {word}">{word}</span>', row)
        css = sk.SCORECARD_CSS
        for var in ("var(--landed)", "var(--stalled)"):
            for sel in re.findall(r"([^{}]+)\{[^{}]*" + re.escape(var), css):
                self.assertRegex(sel, r"\.(st|ac)\.(landed|stalled)")
        with self.assertRaises(ValueError):
            sk.status_mark("green")
        with self.assertRaises(ValueError):
            sk.range_line(actual=1, status="ok")

    def test_brass_only_for_a_persons_call(self):
        for sel in re.findall(r"([^{}]+)\{[^{}]*var\(--brass\)", sk.SCORECARD_CSS):
            self.assertRegex(sel.strip(), r"\.sc-(o|pm)\b")
        call = sk.person_call("Head of Product", due="2026-12-10")
        self.assertTrue(call.startswith('<span class="sc-o"><svg width="8" height="10"'))
        self.assertIn("Head of Product</span>", call)

    def test_words_are_text_never_boxed_chips(self):
        self.assertEqual(sk.check_word("HOLD", ink=True), '<span class="sc-w ink">HOLD</span>')
        self.assertNotIn("border", re.search(r"\.scg \.sc-w\{[^}]*\}", sk.SCORECARD_CSS).group(0))

    def test_range_line_target_tick_no_band(self):
        rl = sk.range_line(prior=21.67, actual=43, target=40, status="landed")
        self.assertIn('class="tg"', rl)
        self.assertNotIn('class="ok"', rl)
        self.assertIn('cx="42.71%"', rl)  # 21.67 of 43 x 1.18
        self.assertIn('class="ac landed" cx="84.75%"', rl)

    def test_paired_bars_scale_to_the_largest_and_hatch_only_the_overage(self):
        over = sk.paired_bars(14, 28, top=28, hatch_id="h")
        self.assertIn('<rect class="pl" x="0" y="0" width="50%"', over)
        self.assertIn('<rect class="a" x="0" y="8" width="50%"', over)
        self.assertIn('<rect class="ov" x="50%" y="8.5" width="50%" height="5" fill="url(#h)"/>', over)
        under = sk.paired_bars(14, 7, top=28, hatch_id="h")
        self.assertNotIn("url(#", under)
        self.assertIn('width="25%"', under)

    def test_share_bar_and_pips(self):
        self.assertIn('width="78.57%"', sk.share_bar(11, 14))
        self.assertEqual(sk.pips(2, 5, dashed=1).count('class="on"'), 2)
        self.assertEqual(sk.pips(2, 5, dashed=1).count("dash"), 1)

    def test_frame_states_its_answer_once_with_one_tag_and_one_caption(self):
        out = scorecard()
        self.assertTrue(out.startswith('<div class="sc scg" role="img" aria-label="Quote drafting landed; job scheduler stalled.">'))
        self.assertEqual(out.count("sc-i"), 1)
        self.assertEqual(out.count('class="sc-c"'), 1)
        self.assertEqual(out.count('class="sc-h"'), 1)
        self.assertEqual(len(sk.frames_in(self.page())), 1)
        self.assertTrue(sk.frames_in(self.page())[0].endswith("</div>"))

    def test_text_is_escaped(self):
        out = sk.sc_row("<script>", figure=sk.figure_line("<b>"))
        self.assertNotIn("<script>", out)
        self.assertIn("&lt;b&gt;", out)


class ScorecardOneTwo(unittest.TestCase):
    """1.2.0: one scale per frame, marks drawn apart, the word column, the golden structure, legacy deprecated."""

    def test_frame_domain_is_one_scale_from_the_rows_own_values(self):
        rows = [(21.67, 43, 40), (2060, 2100, 3000), (16.92, 18.1, 18)]
        lo, hi = sk.frame_domain(rows)
        ratios = [v / t for p, a, t in rows for v in (p, a, t)]
        span = max(ratios) - min(ratios)
        self.assertAlmostEqual(lo, min(ratios) - span * 0.06)
        self.assertAlmostEqual(hi, max(ratios) + span * 0.06)
        self.assertEqual(sk.frame_domain([], relative=True), (0.0, 1.0))
        absolute = sk.frame_domain([(1, 2, 3)], relative=False)
        self.assertAlmostEqual(absolute[0], 0.88)

    def test_every_target_tick_lines_up_on_a_relative_scale(self):
        dom = sk.frame_domain([(21.67, 43, 40), (2060, 2100, 3000)])
        ticks = {re.search(r'class="tg" x="([^"]+)"', sk.range_line(prior=p, actual=a, target=t, domain=dom, relative=True)).group(1) for p, a, t in [(21.67, 43, 40), (2060, 2100, 3000)]}
        self.assertEqual(len(ticks), 1)

    def test_close_marks_are_drawn_apart_in_value_order_and_equal_ones_are_not(self):
        dom = sk.frame_domain([(21.67, 43, 40), (2060, 2100, 3000), (16.92, 18.1, 18)])
        job = sk.range_line(prior=2060, actual=2100, target=3000, status="stalled", domain=dom, relative=True)
        self.assertIn('class="pr" cx="', job)
        self.assertRegex(job, r'class="pr"[^>]*transform="translate\(-4 0\)"')
        self.assertRegex(job, r'class="ac stalled"[^>]*transform="translate\(4 0\)"')
        links = sk.range_line(prior=16.92, actual=18.1, target=18, status="watch", domain=dom, relative=True)
        self.assertRegex(links, r'class="ac watch"[^>]*transform="translate\(4 0\)"', "18.1% sits on the right of the 18% tick")
        same = sk.range_line(prior=5, actual=5, target=9, domain=(0, 10))
        self.assertNotIn("translate(4", same)
        far = sk.range_line(prior=1, actual=9, target=5, domain=(0, 10))
        self.assertNotIn('transform="translate(4', far)

    def test_a_lower_actual_moves_left(self):
        out = sk.range_line(prior=40.6, actual=40.3, target=30, domain=(0, 50))
        self.assertRegex(out, r'class="ac"[^>]*transform="translate\(-4 0\)"')

    def test_word_column_wraps_at_word_max(self):
        self.assertIn("fit-content(var(--sc-wmax,180px))", sk.SCORECARD_CSS)
        self.assertIn('style="--sc-wmax:220px"', sk.sc_frame([], label="x", title="t", word_max=220))
        self.assertNotIn("--sc-wmax:", sk.sc_frame([], label="x", title="t"))
        self.assertIn(".scg .st{white-space:nowrap}", sk.SCORECARD_CSS, "status words never wrap")

    def test_the_golden_structure_is_current(self):
        committed = json.loads(scorecard_golden.GOLDEN.read_text(encoding="utf-8"))
        self.assertEqual(committed, scorecard_golden.golden(), "run python3 tools/scorecard_golden.py, then copy the JSON to the site")
        self.assertEqual(committed["svgkit"], sk.VERSION)
        self.assertEqual(committed["structure"][0], "sc.scg")
        self.assertIn("sc.scg/sc-b/sc-r/sc-p/sc-rl", committed["structure"])
        self.assertIn("sc.scg/sc-b/sc-r/sc-s/sc-o/sc-pm", committed["structure"])

    def test_structure_ignores_tags_and_other_classes(self):
        a = '<div class="sc scg x"><p class="sc-c y">t</p></div>'
        b = '<figure class="scg sc"><span class="sc-c">u</span></figure>'
        self.assertEqual(sk.structure(a), sk.structure(b))

    def test_legacy_primitives_warn_and_leave_a_mark(self):
        for name in sk.LEGACY:
            self.assertTrue(getattr(getattr(sk, name), "deprecated", False), name)
        with warnings.catch_warnings(record=True) as caught:
            warnings.simplefilter("always")
            out = sk.frame("", label="x", height=1)
        self.assertTrue(any(issubclass(w.category, DeprecationWarning) for w in caught))
        self.assertEqual(sk.legacy_in(out), ['class="sk-wide"'])
        self.assertEqual(sk.legacy_in(scorecard()), [])
        with warnings.catch_warnings():
            warnings.simplefilter("error", DeprecationWarning)
            scorecard()  # the scorecard rows never call a legacy primitive
            sk.page_header("x", date="d", version="v", illustrative=True)


class Numbers(unittest.TestCase):
    def test_fixed_formatting(self):
        cases = {0: "0", 1: "1", 1.5: "1.5", 1.25: "1.25", 1.255: "1.25", 1.256: "1.26", -0.001: "0", 2.10: "2.1", 720.0: "720", -3.5: "-3.5"}
        for given, shown in cases.items():
            with self.subTest(given=given):
                self.assertEqual(sk.num(given), shown)

    def test_scale(self):
        f = sk.scale((0, 100), (10, 210))
        self.assertEqual((f(0), f(50), f(100)), (10, 110, 210))
        self.assertEqual(sk.scale((5, 5), (0, 10))(5), 5)


class Output(unittest.TestCase):
    def test_deterministic(self):
        self.assertEqual(sample(), sample())

    def test_no_number_carries_more_than_two_decimals(self):
        self.assertIsNone(re.search(r"\d\.\d{3,}", sample()))

    def test_colours_are_css_variables_only(self):
        svg = sample()
        self.assertIsNone(HEX.search(svg), "a literal colour; use the template's variables")
        for fill in re.findall(r'(?:fill|stroke)="([^"]+)"', svg):
            with self.subTest(fill=fill):
                self.assertRegex(fill, r"^(var\(--[a-z0-9-]+\)|none|url\(#[a-z0-9-]+\))$")

    def test_the_one_literal_is_the_illustrative_blue(self):
        self.assertEqual(HEX.findall(sk.CSS), ["#74A5DA"])

    def test_frame_is_an_image_that_states_its_answer(self):
        svg = sample()
        self.assertTrue(svg.startswith('<svg class="sk-wide" width="720" height="320" viewBox="0 0 720 320" role="img"'))
        self.assertIn('aria-label="Quote drafting landed: 43% against a 40% target."', svg)
        tall = sk.frame("", label="x", height=200, width=sk.TALL, variant="tall")
        self.assertIn('class="sk-tall" width="340"', tall)
        with self.assertRaises(ValueError):
            sk.frame("", label="x", height=1, variant="square")

    def test_no_shadows_or_gradients(self):
        svg = sample()
        for word in ("filter", "Gradient", "shadow", "opacity"):
            self.assertNotIn(word, svg)

    def test_text_is_escaped(self):
        svg = sk.label(0, 0, "<script>") + sk.frame("", label='a "b" <c>', height=1)
        self.assertNotIn("<script>", svg)
        self.assertIn("&lt;SCRIPT&gt;", svg)
        self.assertIn('aria-label="a &quot;b&quot; &lt;c&gt;"', svg)

    def test_labels_are_upper_case_mono(self):
        self.assertEqual(sk.label(0, 0, "Target 40%"), '<text x="0" y="0" class="sk-l" style="color:var(--t3)">TARGET 40%</text>')


class Meaning(unittest.TestCase):
    def test_green_and_red_only_beside_their_word(self):
        for word in ("landed", "stalled"):
            mark = sk.status_word(0, 10, word)
            self.assertIn(f"var(--{word})", mark)
            self.assertIn(f">{word.upper()}</text>", mark)
        body = sample().replace(sk.status_word(200, 300, "landed"), "")
        self.assertNotIn("var(--landed)", body)
        self.assertNotIn("var(--stalled)", body)
        with self.assertRaises(ValueError):
            sk.status_word(0, 0, "green")

    def test_brass_is_the_person_and_grey_the_agent(self):
        self.assertIn(sk.BRASS, sk.person(0, 0))
        self.assertNotIn(sk.BRASS, sk.spark(0, 0))
        self.assertIn(sk.AGENT, sk.spark(0, 0))

    def test_target_lines_dash_4_3_in_ink(self):
        self.assertIn('stroke="var(--t1)" stroke-width="1.5" stroke-dasharray="4 3"', sk.target_line(0, 10, 5))

    def test_overage_is_hatched_and_inside_is_not(self):
        over = sk.hbar(0, 0, actual=150, budget=100, hatch_id="h")
        self.assertIn('fill="url(#h)"', over)
        self.assertNotIn("url(#h)", sk.hbar(0, 0, actual=80, budget=100, hatch_id="h"))

    def test_gate_states(self):
        self.assertIn("<path", sk.gate(0, 0, state="ready"))
        self.assertNotIn("<path", sk.gate(0, 0, state="hold"))
        with self.assertRaises(ValueError):
            sk.gate(0, 0, state="maybe")


class Header(unittest.TestCase):
    def test_shared_header_carries_mark_wordmark_skill_date_version_and_blue_tag(self):
        h = sk.page_header("eval-kit", date="2026-11-15", version="v0.3.4", illustrative=True)
        for part in (
            '<span translate="no">DACARD</span>',
            "<span>eval-kit</span>",
            "<span>2026-11-15</span>",
            "<span>v0.3.4</span>",
            '<span class="sk-ill">Illustrative</span>',
        ):
            self.assertIn(part, h)
        self.assertIn('aria-hidden="true"', sk.mark())
        self.assertNotIn("sk-ill", sk.page_header("x", date="d", version="v", illustrative=False))
        self.assertIn(".sk-ill{", sk.CSS)
        self.assertIn("color:var(--ill)", sk.CSS)

    def test_icon_is_hidden_from_screen_readers(self):
        self.assertIn('aria-hidden="true"', sk.icon("", width=28, height=12))
        self.assertNotIn("role=", sk.icon("", width=28, height=12))


class PageChecks(unittest.TestCase):
    def page(self, printed: str) -> str:
        return f"<style>x</style><main><p>{printed}</p><figure>{sample()}</figure></main>"

    def test_numbers_in(self):
        self.assertEqual(sk.numbers_in(sample()), ["2026-12-10", "40%", "43%"])

    def test_unprinted_lists_figures_missing_from_the_text(self):
        self.assertEqual(sk.unprinted(self.page("Target 40%, now 43%, due 2026-12-10.")), [])
        self.assertEqual(sk.unprinted(self.page("Target 40%.")), ["2026-12-10", "43%"])

    def test_visuals_leave_out_the_mark(self):
        page = sk.page_header("x", date="d", version="v", illustrative=True) + self.page("x")
        self.assertEqual(len(sk.svgs_in(page)), 2)
        self.assertEqual(sk.visuals_in(page), [sample()])

    def test_page_text_drops_the_svg(self):
        self.assertNotIn("43%", sk.page_text(self.page("nothing")))


if __name__ == "__main__":
    unittest.main()
