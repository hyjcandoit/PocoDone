# Notion Daily · Weekly · Monthly Planner — v2

A reusable **AI Agent Skill** for managing daily execution, weekly priorities, monthly progress, linked subtasks, overdue carryover, and reviews **inside one Notion task database**.

**Version:** 2.0.0 · **Updated:** 2026-11-10 · **Language:** Chinese-first, with English repository documentation.

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
| AI automatic splitting on creation | Not available | **Not enabled / future optional** |

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
- **No automatic AI task splitting is activated in v2.**

## Repository layout

| File / folder | Description |
|---|---|
| [`SKILL.md`](SKILL.md) | Main agent skill: triggers, safety, planning & execution |
| [`QUICKSTART.zh-CN.md`](QUICKSTART.zh-CN.md) | Chinese setup and everyday usage |
| [`references/`](references/) | Data schema, formulas, views, migration, overdue/automation behavior |
| [`examples/config.example.yaml`](examples/config.example.yaml) | Public placeholder config — create a private `config.local.yaml` |
| [`examples/automation_prompt.example.md`](examples/automation_prompt.example.md) | Optional scheduled-review prompt |
| [`notion_tasks_template.csv`](notion_tasks_template.csv) | Basic CSV template (backward compatible) |
| [`notion_tasks_template_v2.csv`](notion_tasks_template_v2.csv) | Extended CSV example (does **not** create advanced Notion properties) |
| [`scripts/planner_logic.py`](scripts/planner_logic.py) | Pure Python helper for offline date/rollover logic (no Notion API) |
| [`scripts/validate_skill.py`](scripts/validate_skill.py) | Verify package structure and local documentation |
| [`tests/`](tests/) | Offline tests for logic; no real Notion data involved |
| [`CHANGELOG.md`](CHANGELOG.md) | Release notes and v1 → v2 delta |
| [`references/GITHUB_RELEASE.md`](references/GITHUB_RELEASE.md) | Step-by-step upgrade of the existing GitHub repository |
| [`LICENSE`](LICENSE) | MIT license preserved from v1 |

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

## Original v1 repository & licensing

This v2 pack builds on the original [`hyjcandoit/ai-notion-daily-weekly-monthly-planner`](https://github.com/hyjcandoit/ai-notion-daily-weekly-monthly-planner) repository and preserves its file naming and MIT License. It is prepared for the existing repository but **has not been pushed to GitHub automatically**.

## Sample prompts

```text
使用 Notion Daily · Weekly · Monthly Planner v2。
请先读取我现有的任务数据库与三个视图。
帮我把“完成课程 Week 5”作为一个大型任务，拆成课程学习和 PSet 提交两条每日步骤，
建立所属进度关联，并确认本周/本月进度条能够联动。
不要重复创建任务，不要把未完成的事项标记成已完成。
```

```text
使用 v2 Skill，检查本周和上月遗留任务；保留原截止日。
把需要继续推进的追踪任务纳入本周重点，核对逾期提示和排序。
若没有授权的定时服务，不要假装已经设置自动更新。
```
