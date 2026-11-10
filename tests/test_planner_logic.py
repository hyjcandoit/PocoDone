import sys
import unittest
from datetime import date
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))
from planner_logic import (
    Task,
    calendar_month,
    completion_percent,
    is_overdue,
    monday_to_sunday,
    show_in_month,
    show_in_week,
    unique_step_key,
    is_auto_split_candidate,
    steps_to_create,
    may_mark_split_done,
)


class PlannerLogicTests(unittest.TestCase):
    def setUp(self):
        self.today = date(2026, 11, 10)

    def test_monday_sunday(self):
        self.assertEqual(monday_to_sunday(self.today), (date(2026, 11, 9), date(2026, 11, 15)))

    def test_cross_year_month(self):
        self.assertEqual(calendar_month(date(2026, 12, 30)), (date(2026, 12, 1), date(2026, 12, 31)))

    def test_strict_overdue(self):
        self.assertFalse(is_overdue(Task("today", "待开始", date(2026, 11, 10)), self.today))
        self.assertTrue(is_overdue(Task("yesterday", "进行中", date(2026, 11, 9)), self.today))

    def test_done_never_overdue(self):
        self.assertFalse(is_overdue(Task("finished", "已完成", date(2026, 10, 1)), self.today))

    def test_children_100_suppresses_carryover(self):
        self.assertFalse(is_overdue(Task("pending parent status", "进行中", date(2026, 10, 1), children_completion=1), self.today))

    def test_overdue_from_october_in_week(self):
        t = Task("prior month", "逾期待办", date(2026, 10, 25), tracked=True)
        self.assertTrue(show_in_week(t, self.today))
        self.assertTrue(show_in_month(t, self.today))

    def test_next_week_not_in_current_week(self):
        t = Task("future", "待开始", date(2026, 11, 17), tracked=True)
        self.assertFalse(show_in_week(t, self.today))
        self.assertTrue(show_in_month(t, self.today))

    def test_range_intersection(self):
        t = Task("spans weeks", "进行中", date(2026, 11, 5), date(2026, 11, 29), tracked=True)
        self.assertTrue(show_in_week(t, self.today))

    def test_template_never_overdue_or_tracked(self):
        t = Task("【模板样板】", "待开始", date(2026, 1, 1), tracked=True, is_template=True)
        self.assertFalse(is_overdue(t, self.today))
        self.assertFalse(show_in_week(t, self.today))

    def test_completion_percent(self):
        self.assertEqual(completion_percent(Task("child-based", "逾期待办", children_completion=0.5)), 50)
        self.assertEqual(completion_percent(Task("simple", "已完成")), 100)
        self.assertEqual(completion_percent(Task("simple", "进行中")), 0)

    def test_dedupe_key(self):
        self.assertEqual(unique_step_key("parent", "  Finish   PSet  ", date(2026, 11, 10)),
                         unique_step_key("parent", "finish pset", date(2026, 11, 10)))

    def test_pending_large_task_is_candidate(self):
        self.assertTrue(is_auto_split_candidate("Prepare essay", "大型任务", "待拆分", "待开始"))

    def test_skip_template_even_if_pending(self):
        self.assertFalse(is_auto_split_candidate("【模板样板】大型任务", "大型任务", "待拆分", "待开始"))

    def test_skip_simple_done_and_legacy(self):
        self.assertFalse(is_auto_split_candidate("Simple", "简单任务", "待拆分", "待开始"))
        self.assertFalse(is_auto_split_candidate("Done", "大型任务", "待拆分", "已完成"))
        self.assertFalse(is_auto_split_candidate("Legacy", None, "待拆分", "待开始"))
        self.assertFalse(is_auto_split_candidate("Already split", "大型任务", "已拆分", "进行中"))
        self.assertFalse(is_auto_split_candidate("Needs review", "大型任务", "需确认", "待开始"))

    def test_do_not_duplicate_existing_step(self):
        date_a = date(2026, 11, 10)
        date_b = date(2026, 11, 11)
        planned = [(" Outline  ", date_a), ("First draft", date_b)]
        existing = [("outline", date_a)]
        self.assertEqual(steps_to_create("parent", planned, existing), [("First draft", date_b)])

    def test_two_identical_planned_steps_deduplicated(self):
        when = date(2026, 11, 11)
        self.assertEqual(steps_to_create("p", [("A", when), ("  a ", when)], []), [("A", when)])

    def test_confirm_before_mark_split_done(self):
        w = date(2026, 11, 10)
        steps = [("A", w), ("B", w)]
        self.assertFalse(may_mark_split_done("p", steps, [("A", w)]))
        self.assertTrue(may_mark_split_done("p", steps, steps))
        self.assertFalse(may_mark_split_done("p", [], []))


if __name__ == "__main__":
    unittest.main()
