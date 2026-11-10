# PocoDone

**Make starting easy. Make progress fun.**

### AI-Assisted Planning & Workflow Automation

**Current Version:** v2.1.0

*Formerly: Notion Daily · Weekly · Monthly Planner*

A reusable **AI Agent Skill** for managing daily execution, weekly priorities, monthly progress, linked subtasks, overdue carryover, and reviews **inside one Notion task database**.

**Version:** 2.1.0 · **Updated:** 2026-11-10 · **Language:** Chinese-first, with English repository documentation.

> This repository is a reusable skill and implementation guide, **not a hosted app, background worker, or Notion template installer**. It requires your own Notion account and an assistant/integration with appropriate permissions. No private database IDs, credentials, or real user tasks are included.

## What changed in v2

| Capability | v1 | v2 |
|---|---|---|
| Single Notion database | ✓ | ✓ |
| Daily / weekly / monthly planning | ✓ | ✓ |
| Priorities, reviews, rollover | ✓ | ✓ |
| Parent-child task relations | Guidance only | **Two-way Relation design** |
| Progress percentage / text bars | Manual review | **Formula + Rollup specification** |
| Red overdue status & alerts | Guidance only | **Status + formula + workflow** |
| Weekly tasks include unfinished history | Manual rollover | **Scheduled/manual focus refresh design** |
| Monthly carryover | Manual rollover | **Carryover logic and limitations documented** |
| Simple / large task entry | Generic new task | **Copyable sample-page workflow** |
| AI automatic splitting | Not available | **Optional daily polling; live manual-run test passed in one workspace** |

## Architecture

```text
                  One Notion database
           ┌──────────────┴──────────────┐
       Tracked parent                Daily child tasks
     (weekly/monthly)            (Relation: 所属进度)
           └───────── Daily steps ─────────┘
                       │
              Status: 已完成
                       │
              Formula: 步骤完成
                       │
          Rollup: 步骤完成率 / %
                       │
           Formula: 进度百分比
                       │
       Progress displayed in week/month

   Overdue status & weekly focus refresh:
   requires user action or separate scheduler.
```

**Important distinctions:**

- **Formula progress is reactive.** The percentage updates when linked daily steps are completed.
- **Red Status labels are not reactive.** Changing Status to `逾期待办` requires a user or separately configured authorized process. A Formula can display a red overdue *message* without editing Status.
- A weekly view filtered by `本周重点=true` relies on that checkbox being maintained; it is not automatically tied to Monday without a scheduler.
- A monthly view filtered only by `进度追踪=true` contains **all tracked tasks**, not just this month. The Skill explains a more accurate month-scoped enhancement but does not claim it is installed.
- The two sample pages are **copyable rows**, not necessarily native templates in Notion's `New ▼` dropdown.
- **v2.1 includes an optional AI auto-split workflow.** The source Notion instance has a separately authorized scheduled checker enabled. Installing this repository **does not** enable a scheduled task in another account. Its initial **manual run** successfully created 2 child rows and linked them, but unattended 08:00 execution and retry/idempotency behavior are not yet end-to-end verified. See [test report](references/AI_SPLIT_TEST_REPORT.md).

## Repository layout

| File / folder | Description |
|---|---|
| [`SKILL.md`](SKILL.md) | Main agent skill: triggers, safety, planning & execution |
| [`QUICKSTART.zh-CN.md`](QUICKSTART.zh-CN.md) | Chinese setup and everyday usage |
| [`references/`](references/) | Data schema, formulas, views, migration, overdue/automation behavior; **AI split guide & anonymized live test report** |
| [`examples/config.example.yaml`](examples/config.example.yaml) | Public placeholder config — create a private `config.local.yaml` |
| [`examples/automation_prompt.example.md`](examples/automation_prompt.example.md) | Optional **scheduled review + AI auto-split** prompt |
| [`notion_tasks_template.csv`](notion_tasks_template.csv) | Basic CSV template (backward compatible) |
| [`notion_tasks_template_v2.csv`](notion_tasks_template_v2.csv) | Extended v2 CSV example (does **not** create advanced Notion properties) |
| [`notion_tasks_template_v2_1.csv`](notion_tasks_template_v2_1.csv) | v2.1 CSV example including AI split state (**cannot create relations or scheduling**) |
| [`scripts/planner_logic.py`](scripts/planner_logic.py) | Pure Python helper for offline date/rollover logic (no Notion API) |
| [`scripts/validate_skill.py`](scripts/validate_skill.py) | Verify package structure and local documentation |
| [`tests/`](tests/) | Offline tests for logic; no real Notion data involved |
| [`CHANGELOG.md`](CHANGELOG.md) | Release notes and v1 → v2 delta |
| [`references/GITHUB_RELEASE.md`](references/GITHUB_RELEASE.md) | Step-by-step upgrade of the existing GitHub repository |
| [`LICENSE`](LICENSE) | MIT license preserved from v1 |

## v2.1 changes: AI task auto-splitting

- New `AI 拆分状态` Select field: `待拆分` / `已拆分` / `需确认` / `无需拆分`.
- Large-task template defaults to pending; simple-task template defaults to no split. Template sample pages must be skipped by the checker.
- An authorized daily scheduler can check at 08:00 (local timezone), create linked daily steps, verify relations, and then mark a parent as split. It is polling, **not an instant Notion-created webhook**.
- A controlled immediate-run test passed for one sample parent and two linked daily children. All three test records were subsequently moved to Trash at the user's request.
- Still untested: unattended scheduled run, repeat-run deduplication under live conditions, and 0%→50%→100% progress updates on live example data.

See [AI split workflow](references/AI_SPLIT_AUTOMATION.md), [anonymized test report](references/AI_SPLIT_TEST_REPORT.md), and [CHANGELOG](CHANGELOG.md).

## Quick start

1. Download the repo or the Skill zip. Load `SKILL.md` in an assistant that supports Agent Skills or reusable instructions.
2. Connect **your own Notion** through a supported integration, and authorize only the requested database.
3. Read [`QUICKSTART.zh-CN.md`](QUICKSTART.zh-CN.md) and map the columns; do not blindly overwrite an existing task database.
4. Use the existing database and views. For complex tasks, create daily steps linked by `所属进度` to the parent task; set the parent's `进度追踪=true`.
5. If you want scheduled weekly rollover, **explicitly enable** an independent scheduled task. The Skill file alone does not schedule anything.
6. Before public GitHub upload, ensure local/private configs and real task data are excluded.

## Verify the skill locally

No third-party Python packages are needed for the bundled offline tests:

```bash
python3 scripts/validate_skill.py
python3 -m unittest discover -s tests -v
```

The tests check **the reference logic**, not whether your Notion connector can create or update particular view/Formula APIs.

## Compatibility and limitations

The data model uses Notion Status, Checkbox, Date, Formula, Rollup, and a **two-way self Relation**. Formula syntax and view DSL may depend on your Notion workspace and integration. CSV imports do not create formula properties, Relations, Rollups, Views, real database templates, or automatic schedulers. Read the [migration guide](references/MIGRATION_V1_TO_V2.md) before modifying a production database.

## Project History & Licensing

This project was originally released as v0.1.0 and has since evolved into v2.0.0 and v2.1.0.
Version 2.1.0 introduces AI-assisted task decomposition, scheduled workflow support, and additional testing documentation.
The project is open-source under the MIT License.
For previous versions and release history, see the [GitHub Releases](https://github.com/hyjcandoit/ai-notion-daily-weekly-monthly-planner/releases) page.

## Sample prompts

```text
Use Notion Daily · Weekly · Monthly Planner v2.1.
First, read my existing task database and its three views.
Set up "Complete Course Week 5" as a large task and split it into two daily steps: course study and PSet submission.
Link them to the parent task through the 所属进度 relation, and confirm that the weekly and monthly progress bars update together.
Do not create duplicate tasks, and do not mark unfinished items as completed.
```

```text
Use the v2.1 Skill to check this week's tasks and anything left over from last month. Keep their original due dates.
Add the tracked tasks that still need work to this week's focus (本周重点), then check the overdue alerts and the sort order.
If there's no authorized scheduled service, don't claim that automatic updates have been set up.
```
