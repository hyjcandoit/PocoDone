"""Static package validator; performs no network calls and reads no Notion data."""

from __future__ import annotations

import csv
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REQUIRED = [
    "SKILL.md",
    "README.md",
    "QUICKSTART.zh-CN.md",
    "CHANGELOG.md",
    "LICENSE",
    "notion_tasks_template.csv",
    "notion_tasks_template_v2.csv",
    "references/DATABASE_SCHEMA.md",
    "references/VIEWS_AND_FORMULAS.md",
    "references/TASK_WORKFLOWS.md",
    "references/AUTOMATION_AND_LIMITATIONS.md",
    "references/MIGRATION_V1_TO_V2.md",
    "references/GITHUB_RELEASE.md",
    "references/AI_SPLIT_AUTOMATION.md",
    "references/AI_SPLIT_TEST_REPORT.md",
    "notion_tasks_template_v2_1.csv",
    "examples/config.example.yaml",
    "examples/automation_prompt.example.md",
    "scripts/planner_logic.py",
    "tests/test_planner_logic.py",
]


def main() -> int:
    errors = []
    for name in REQUIRED:
        path = ROOT / name
        if not path.is_file() or path.stat().st_size == 0:
            errors.append(f"Missing/empty: {name}")

    skill = (ROOT / "SKILL.md").read_text(encoding="utf-8")
    match = re.match(r"\A---\n(.*?)\n---\n", skill, re.DOTALL)
    if match is None:
        errors.append("SKILL.md must have a YAML frontmatter block")
    else:
        front = match.group(1)
        for key in ["name", "description"]:
            if not re.search(rf"(?m)^{key}:\s*\S", front):
                errors.append(f"SKILL.md frontmatter missing {key}")

    for name in ["notion_tasks_template.csv", "notion_tasks_template_v2.csv", "notion_tasks_template_v2_1.csv"]:
        with (ROOT / name).open(encoding="utf-8-sig", newline="") as f:
            rows = list(csv.reader(f))
        if len(rows) < 2 or not {"任务", "分类", "日期", "状态"}.issubset(set(rows[0])):
            errors.append(f"Invalid columns or no sample rows in {name}")

    # These identifiers should live in a user-managed local config, never public files.
    private_patterns = [r"collection://[a-f0-9-]{32,36}", r"view://[a-f0-9-]{32,36}"]
    for p in ROOT.rglob("*"):
        if not p.is_file() or p.suffix not in {".md", ".yaml", ".csv"}:
            continue
        if p.name.endswith(".local.md") or p.name.endswith(".private.md"):
            continue
        text = p.read_text(encoding="utf-8")
        for pat in private_patterns:
            if re.search(pat, text):
                errors.append(f"Likely private Notion instance identifier in {p.relative_to(ROOT)}")

    if errors:
        for error in errors:
            print("FAIL:", error)
        return 1

    print(f"PASS: v2.1 package structure, frontmatter and CSV checked ({len(REQUIRED)} required files).")
    print("NOTE: This does NOT validate your live Notion workspace or install templates/automations.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
