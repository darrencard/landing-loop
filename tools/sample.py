"""Assemble the Acme quote-drafting loop record from each skill's own sample run.

Each skill renders its sample in its own repo and writes only its key into
examples/acme/landing/quote-drafting.json (CONTRACT.md). This script merges
those five files in loop order into one record and fails if two skills write
the same key or read different briefs.

Usage: python3 tools/sample.py <dir with the five skill repos> (default: ~)
"""

import json
import sys
from pathlib import Path

ORDER = [
    ("bet-portfolio-review", "portfolio"),
    ("spec-auditor", "spec"),
    ("cost-budget-check", "cost"),
    ("eval-kit", "evals"),
    ("did-it-land", "landed"),
]
BET = "quote-drafting"
ROOT = Path(__file__).resolve().parent.parent


def main() -> int:
    base = Path(sys.argv[1]).expanduser() if len(sys.argv) > 1 else Path.home()
    record: dict = {"schema": "landing-loop/1", "bet": BET}
    for repo, key in ORDER:
        part = json.loads((base / repo / "examples/acme/landing" / f"{BET}.json").read_text())
        if part.get("schema") != "landing-loop/1" or part.get("bet") != BET:
            raise SystemExit(f"{repo}: not a landing-loop/1 record for {BET}")
        if "brief" in part:
            if "brief" in record and record["brief"]["sha256"] != part["brief"]["sha256"]:
                raise SystemExit(f"{repo}: read a different brief")
            record["brief"] = part["brief"]
        if key in record:
            raise SystemExit(f"{repo}: {key} already written")
        for k, v in part.items():
            if k not in ("schema", "bet", "brief", key) and record.get(k) != v:
                raise SystemExit(f"{repo}: changed or invented the {k} key it read")
        record[key] = part[key]
    out = ROOT / "examples/acme/landing" / f"{BET}.json"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(record, indent=2, ensure_ascii=False) + "\n")
    print(f"wrote {out.relative_to(ROOT)}: {', '.join(k for k in record if k not in ('schema', 'bet'))}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
