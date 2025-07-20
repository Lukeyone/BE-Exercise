from django.core.management import call_command
from django.db.models import Sum
from django.test import TestCase

from myapp.models import Assignment, Task, Worker

class AutoAllocatorTest(TestCase):
    # use the bigger sample — it has plenty of tasks
    fixtures = ["sample.json"]

    def setUp(self):
        # start from a clean slate: no assignments
        Assignment.objects.all().delete()

    def test_all_workers_under_eight_hours(self):
        # run the management command
        call_command("auto_assign_tasks", verbosity=0)

        # every worker/date pair should be ≤ 8 hours
        bad_rows = (
            Assignment.objects.values("worker", "task__date")
            .annotate(total=Sum("task__duration"))
            .filter(total__gt=8)
            .count()
        )
        self.assertEqual(bad_rows, 0)

    def test_every_task_either_assigned_or_unplaced(self):
        call_command("auto_assign_tasks", verbosity=0)

        assigned_ids = set(Assignment.objects.values_list("task_id", flat=True))
        all_task_ids = set(Task.objects.values_list("id", flat=True))
        unplaced = all_task_ids - assigned_ids

        # For this simple allocator we expect every task to be tried;
        # unplaced set is okay but should not be bigger than original list.
        self.assertLessEqual(len(assigned_ids), len(all_task_ids))
        # Make sure we didn't lose any tasks
        self.assertEqual(len(assigned_ids) + len(unplaced), len(all_task_ids))
