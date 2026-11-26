"""Check the marketplace and the bundle agree: every dependency is listed, names are unique."""

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
market = json.loads((ROOT / ".claude-plugin/marketplace.json").read_text())
bundle = json.loads((ROOT / "plugin/.claude-plugin/plugin.json").read_text())

names = [p["name"] for p in market["plugins"]]
errors = []
if len(names) != len(set(names)):
    errors.append("duplicate plugin names in marketplace.json")
for dep in bundle["dependencies"]:
    if dep not in names:
        errors.append(f"dependency {dep} is not in marketplace.json")
for name in names:
    if name != bundle["name"] and name not in bundle["dependencies"]:
        errors.append(f"{name} is listed but the bundle does not install it")
if not (ROOT / "plugin/skills/landing-loop/SKILL.md").exists():
    errors.append("missing plugin/skills/landing-loop/SKILL.md")

for e in errors:
    print(f"error: {e}")
print("ok" if not errors else f"{len(errors)} error(s)")
sys.exit(1 if errors else 0)
