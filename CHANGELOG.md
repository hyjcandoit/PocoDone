# Changelog

## 2.1.0 — 2026-11-10

### Added / enabled in the source instance (NOT portable by copy alone)

- `AI 拆分状态` with `待拆分 / 已拆分 / 需确认 / 无需拆分` and new-task defaults for copyable samples.
- Optional **daily 08:00 AI splitting check** integrated into the existing authorized scheduler; no second scheduled task needed.
- Safe candidate selection, sample-page exclusion, incremental/duplicate-safe child creation, required `所属进度` ↔ `每日步骤` verification, and `需确认` recovery.
- New `references/AI_SPLIT_AUTOMATION.md` implementation guide, revised scheduler prompt, v2.1 example CSV and offline tests.

### First real-write test — controlled immediate run

- A test parent yielded **two linked daily children** within the existing database; the parent was verified with both children and marked `已拆分`.
- Test pages were excluded from normal progress views; **all three test records were moved to Notion Trash** after user confirmation.
- This was a **manual immediate run of the saved automation instructions, executed inline in the conversation**; it is not evidence of unattended 08:00 success.
- **Not tested live:** second identical run/deduplication, child completion 0%→50%→100%, failure recovery and unattended scheduler execution.

### Release and privacy

- This skill package documents the implementation; installing it does **not** create a schedule, connect a Notion workspace, or push changes to GitHub.
- Real Notion identifiers and test row IDs are omitted from the public package.

## 2.0.0 — 2026-11-10

Based on v1 public repository and the verified design iterations from **2026-11-09 to 2026-11-10**.

### Added

- Two-way parent/daily-step relations: `所属进度` and `每日步骤`.
- Daily-step completion formula, `percent_checked` rollup, progress-percentage and 10-segment text progress bars.
- Status category `逾期待办` (red), dynamic overdue indicator and dedicated overdue view.
- Weekly focus flag, deterministic display order, and rollover rules for unfinished parent tasks.
- Month/previous-month carryover workflow, with an explicit distinction between desired calendar-month scoping and the actual `进度追踪=true` view filter.
- Simple-task / large-task selection, copyable example pages and template limits documented.
- Categories for course/PSet, essay stages, AI milestones and other project tasks.
- Weekly/monthly average-progress chart semantics (not hours-weighted).
- Optional recurring review prompt and logic; **does not install, create, or change a recurring automation**.
- Migration guide, portable placeholder configuration, local logic scripts and offline tests.

### Preserved from v1

- One-database planning model.
- Daily, weekly and monthly planning and reviews.
- Real completion state as truth; priority P0–P3.
- History preservation, rollover, duplicate prevention, and user authorization boundaries.
- MIT license and original root filenames.

### Known limitations / intentionally not implemented

- No automatic AI splitting of newly created large tasks.
- No automatic registration of copyable page samples into the native Notion `New ▼` menu.
- No true calendar-month filter when the Notion view only checks `进度追踪=true`.
- No guarantee that all Notion connectors support Formula properties in view filter DSL.
- The Skill is documentation/procedures; it cannot run on a schedule by itself.

## 0.1.0 — initial release

- Unified daily/weekly/monthly Notion planner skill, README, Chinese quickstart, basic CSV, MIT License.
