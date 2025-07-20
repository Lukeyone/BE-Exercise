"""
Simple auto‑allocator.

Run:
    python manage.py auto_assign_tasks

What it does:
1. Wipes all existing Assignment rows (we were told to ignore them).
2. For every date + position it pushes tasks onto workers of the same
   position, keeping each worker ≤ 8 hours for that date.
3. Prints a couple of quick KPIs at the end.

Heuristic:
* “Fill‑up‑one‑worker‑before‑using‑next” – easy to reason about and matches
  a real‑world shift approach.
* Not optimal but guarantees the 8 h cap and avoids tiny fragments.
"""

from collections import defaultdict

from django.core.management.base import BaseCommand
from django.db import transaction
from django.db.models import Sum

from myapp.models import Assignment, Position, Task, Worker


MAX_HOURS_PER_DAY = 8


class Command(BaseCommand):
    help = "Auto‑assign tasks so each worker tops out at 8 h per day."

    @transaction.atomic
    def handle(self, *args, **options):
        # 1. clear existing assignments
        Assignment.objects.all().delete()

        unplaced_total = 0
        placed_total = 0

        # 2. loop per date so we respect daily capacity
        dates = (
            Task.objects.values_list("date", flat=True)
            .distinct()
            .order_by("date")
        )

        for dt in dates:
            # keep a per‑worker counter for the day
            daily_hours = defaultdict(int)  # worker_id -> hours

            for pos in Position.objects.all():
                # workers of this position, sorted so we fill one completely
                workers = list(pos.workers.order_by("id"))

                tasks = (
                    Task.objects.filter(date=dt, position=pos)
                    .order_by("-duration")  # sort by longest duration first
                )

                for task in tasks:
                    # find first worker with enough remaining capacity
                    for w in workers:
                        if daily_hours[w.id] + task.duration <= MAX_HOURS_PER_DAY:
                            Assignment.objects.create(task=task, worker=w)
                            daily_hours[w.id] += task.duration
                            placed_total += 1
                            break
                    else:
                        # no worker had room – leave it unassigned
                        unplaced_total += 1

        # 3. KPI printout
        util_qs = (
            Assignment.objects.values("worker", "task__date")
            .annotate(hours=Sum("task__duration"))
        )

        avg_util = (
            sum(r["hours"] for r in util_qs) /
            (len(util_qs) * MAX_HOURS_PER_DAY)
            if util_qs else 0
        )

        self.stdout.write(self.style.SUCCESS("Auto‑allocation done"))
        self.stdout.write(f"Placed tasks:     {placed_total}")
        self.stdout.write(f"Unplaced tasks:   {unplaced_total}")
        self.stdout.write(f"Avg daily utilisation: {avg_util:0.2%}")
