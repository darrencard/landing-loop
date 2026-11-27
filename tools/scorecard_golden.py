"""The canonical scorecard frame and its class structure, written to tools/scorecard-golden.json.

The site's row kit (dacard-v0 components/skills/visuals/rows.tsx) renders the same frame from the same inputs and
must give the same structure: its test reads a copy of the JSON, pinned by this repo's commit. Regenerate after any
change to the markup svgkit writes, then copy the JSON to the site:

  python3 tools/scorecard_golden.py            # writes tools/scorecard-golden.json
  python3 tools/scorecard_golden.py --check    # exits 1 if the committed JSON is stale

Standard library only. Python 3.11 or later.
"""

import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

import svgkit as sk  # noqa: E402

GOLDEN = Path(__file__).resolve().parent / "scorecard-golden.json"

# The inputs, in words the site's fixture repeats exactly.
FIXTURE = {
    "title": "Scorecard",
    "label": "Quote drafting landed; payment links is on watch; two calls, one over plan.",
    "head": ["Project", "", "Before → now · target", "Status"],
    "caption": "One frame, every row type.",
    "range_rows": [
        {"name": "Quote drafting", "prior": 21.67, "actual": 43, "target": 40, "shown": ["21.67%", "43%", "40%"], "status": "landed", "check": "cost over budget"},
        {"name": "Payment links", "prior": 16.92, "actual": 18.1, "target": 18, "shown": ["16.92%", "18.1%", "18%"], "status": "watch"},
    ],
    "bar_rows": [
        {"name": "When to undo the release", "plan": 14, "actual": 28, "who": "Head of Product"},
        {"name": "Prices from the price book", "plan": 14, "actual": 5, "who": "Tech lead"},
    ],
}


def canonical() -> str:
    f = FIXTURE
    domain = sk.frame_domain([(r["prior"], r["actual"], r["target"]) for r in f["range_rows"]])
    rows = [
        sk.sc_row(
            r["name"],
            picture=sk.range_line(prior=r["prior"], actual=r["actual"], target=r["target"], status=r["status"], domain=domain, relative=True),
            figure=sk.figure_line(r["shown"][1], prior=r["shown"][0], target=r["shown"][2]),
            word=sk.status_mark(r["status"]) + (sk.check_word(r["check"]) if r.get("check") else ""),
        )
        for r in f["range_rows"]
    ]
    top = max(max(r["plan"], r["actual"]) for r in f["bar_rows"])
    rows += [
        sk.sc_row(r["name"], picture=sk.paired_bars(r["plan"], r["actual"], top=top, hatch_id=f"g{i}"), figure=sk.figure_line(f"{r['actual']} DAYS"), word=sk.person_call(r["who"]))
        for i, r in enumerate(f["bar_rows"])
    ]
    key = sk.legend("prior", "average before launch") + sk.legend("target", "target")
    return sk.sc_frame(rows, label=f["label"], title=f["title"], head=f["head"], legend=key, caption=f["caption"])


def golden() -> dict:
    return {"svgkit": sk.VERSION, "fixture": FIXTURE, "structure": sk.structure(canonical())}


def main() -> int:
    text = json.dumps(golden(), indent=2, ensure_ascii=False) + "\n"
    if "--check" in sys.argv:
        same = GOLDEN.exists() and GOLDEN.read_text(encoding="utf-8") == text
        print("scorecard-golden: ok" if same else "scorecard-golden: stale; run python3 tools/scorecard_golden.py")
        return 0 if same else 1
    GOLDEN.write_text(text, encoding="utf-8")
    print(f"scorecard-golden: wrote {GOLDEN.name}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
