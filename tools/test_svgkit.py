"""Tests for svgkit. Run from the repo root: python3 -m unittest discover -s tools -p "test_*.py" """

import re
import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

import svgkit as sk  # noqa: E402

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
