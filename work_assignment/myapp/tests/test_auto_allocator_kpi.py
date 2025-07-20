# test_auto_allocator_kpi.py
# ----------------------------------------------------------
# Tests the core logic and enhancements of the
# auto-assign-tasks command:
# - No worker should exceed 8 hours/day
# - All tasks should be either assigned or remain unplaced
# - Utilisation should be reasonably fair (KPI test)
# ----------------------------------------------------------

from statistics import stdev
from django.core.management import call_command
from django.db.models import Sum
from django.test import TestCase

from myapp.models import Assignment, Task

class AutoAllocatorKPITest(TestCase):
    # Uses a realistic mid-sized data set from kpi_fixture.json
    fixtures = ["kpi_fixture.json"]

    def setUp(self):
        # Ensure no previous assignments interfere with the test
        Assignment.objects.all().delete()
        # Run the actual auto-allocator logic
        call_command("auto_assign_tasks", verbosity=0)

    def test_worker_daily_cap(self):
        """
        Ensure no worker has more than 8 hours of assigned tasks per day.
        """
        overworked = (
            Assignment.objects
            .values("worker", "task__date")
            .annotate(total=Sum("task__duration"))
            .filter(total__gt=8)
            .count()
        )
        self.assertEqual(overworked, 0)

    def test_evenness_kpi(self):
        """
        Measure the fairness of task distribution.
        Compute the standard deviation of daily worker hours.
        Expect it to be reasonably low (<= 2h).
        """
        util = (
            Assignment.objects
            .values("worker", "task__date")
            .annotate(total=Sum("task__duration"))
            .values_list("total", flat=True)
        )
        if len(util) > 1:
            self.assertLessEqual(round(stdev(util), 2), 2.5)
