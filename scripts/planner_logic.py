"""Local, dependency-free reference logic for Notion Planner Skill v2.

These functions do not connect to Notion and do not modify any account.
The Notion workspace's own status/formulas remain the source of truth.
"""

from __future__ import annotations

from dataclasses import dataclass
from datetime import date, timedelta
from typing import Optional

COMPLETE = "已完成"
OVERDUE = "逾期待办"


@dataclass(frozen=True)
class Task:
    title: str
    status: str
    start: Optional[date] = None
    end: Optional[date] = None
    tracked: bool = False
    # Set to a value from 0.0..1.0 only if a linked child list is verified.
    children_completion: Optional[float] = None
    is_template: bool = False

    def __post_init__(self) -> None:
        if self.start and self.end and self.end < self.start:
            raise ValueError("end must be on or after start")
        if self.children_completion is not None and not (0.0 <= self.children_completion <= 1.0):
            raise ValueError("children_completion must be in [0, 1]")

    @property
    def deadline(self) -> Optional[date]:
        return self.end or self.start


def monday_to_sunday(day: date) -> tuple[date, date]:
    """ISO natural week Monday--Sunday, based on an already-local date."""
    monday = day - timedelta(days=day.weekday())
    return monday, monday + timedelta(days=6)


def calendar_month(day: date) -> tuple[date, date]:
    first = day.replace(day=1)
    if day.month == 12:
        next_first = date(day.year + 1, 1, 1)
    else:
        next_first = date(day.year, day.month + 1, 1)
    return first, next_first - timedelta(days=1)


def has_completed(task: Task) -> bool:
    """Keep completed user statuses; a verified 100% children can suppress carryover.

    A full child rollup does not automatically change the parent Notion Status.
    """
    return task.status == COMPLETE or task.children_completion is not None and task.children_completion >= 1.0


def is_overdue(task: Task, today: date) -> bool:
    if task.is_template or has_completed(task) or task.deadline is None:
        return False
    return task.deadline < today


def overlaps(task: Task, window_start: date, window_end: date) -> bool:
    if task.start is None or task.is_template:
        return False
    return task.start <= window_end and (task.end or task.start) >= window_start


def show_in_week(task: Task, today: date) -> bool:
    if not task.tracked or task.is_template:
        return False
    start, end = monday_to_sunday(today)
    return overlaps(task, start, end) or is_overdue(task, today)


def show_in_month(task: Task, today: date) -> bool:
    """Recommended future month-scoped logic, NOT the current 'tracked only' view."""
    if not task.tracked or task.is_template:
        return False
    start, end = calendar_month(today)
    return overlaps(task, start, end) or is_overdue(task, today)


def completion_percent(task: Task) -> int:
    """Simplified offline rule, without production legacy CS50P/essay checkbox fallback."""
    if task.children_completion is not None:
        return round(task.children_completion * 100)
    return 100 if task.status == COMPLETE else 0


def unique_step_key(parent_id: str, title: str, deadline: Optional[date]) -> tuple[str, str, str]:
    """Normalize a potential child step before deduplicating within a verified parent."""
    canonical_title = " ".join(title.casefold().strip().split())
    return (parent_id.strip(), canonical_title, deadline.isoformat() if deadline else "")


def is_auto_split_candidate(
    title: str,
    task_type: str | None,
    split_state: str | None,
    status: str,
    template_marker: str = "【模板样板】",
) -> bool:
    """Select real pending large tasks for optional scheduled AI splitting.

    This function only makes a local decision; it never writes to Notion.
    Templates are excluded even if an example is configured as pending.
    """
    return (
        task_type == "大型任务"
        and split_state == "待拆分"
        and status != COMPLETE
        and template_marker not in title
    )


def steps_to_create(
    parent_id: str,
    planned: list[tuple[str, date | None]],
    existing: list[tuple[str, date | None]],
) -> list[tuple[str, date | None]]:
    """Pure function: list missing child steps, without duplicating an existing key.

    Matching titles and dates is one conservative guard. A live Notion worker
    MUST ALSO re-read two-way Relations, scope, and deliverable descriptions.
    """
    current = {unique_step_key(parent_id, title, when) for title, when in existing}
    missing = []
    for title, when in planned:
        key = unique_step_key(parent_id, title, when)
        if key not in current:
            missing.append((title, when))
            current.add(key)
    return missing


def may_mark_split_done(
    parent_id: str,
    planned: list[tuple[str, date | None]],
    verified_children: list[tuple[str, date | None]],
) -> bool:
    """Mark split done only after every intended step has verified child evidence.

    This static comparison is necessary but not sufficient: the caller must
    confirm the actual parent/child Notion relation IDs before modifying a row.
    """
    return bool(planned) and not steps_to_create(parent_id, planned, verified_children)
