"""
myapp/views.py

Two endpoints:

1. /api/table/   → pure JSON for programmatic or test use
2. /table/       → nice HTML table for humans

All heavy lifting (grouping, summing, zero‑filling) happens here so the
frontend has nothing to do except render.
"""

from collections import OrderedDict
from datetime import date
from typing import List

from django.db.models import Sum
from django.http import JsonResponse
from django.shortcuts import render
from django.views.decorators.http import require_GET

from .models import Assignment, Position, Task

# ── helpers ──────────────────────────────────────────────────────────────

def fmt(d: date) -> str:
    """2000‑01‑11 → '11 Jan'   (month name keeps things readable)"""
    return d.strftime("%d %b")

def all_dates() -> List[str]:
    """
    Grabs *every* distinct Task.date from the DB, oldest→newest,
    then formats each with fmt().  Guarantees column order is stable.
    """
    return [fmt(d) for d in (
        Task.objects.order_by("date")
        .values_list("date", flat=True)
        .distinct()
    )]

def build_rows(date_cols: List[str]):
    """
    Core aggregation logic.

    Returns a list:
        [OrderedDict(position_row), OrderedDict(worker_row), …]

    Keys in each dict:
        'name', then one key per date in date_cols
    """
    rows = []

    for pos in Position.objects.order_by("id"):

        # --- position totals --------------------------------------------
        p_totals = {
            fmt(rec["date"]): rec["total"]
            for rec in (
                Task.objects
                .filter(position=pos)
                .values("date")
                .annotate(total=Sum("duration"))
            )
        }
        pos_row = OrderedDict(name=pos.name)
        for d in date_cols:
            pos_row[d] = p_totals.get(d, 0)
        rows.append(pos_row)

        # --- worker totals ----------------------------------------------
        for w in pos.workers.order_by("id"):
            w_totals = {
                fmt(rec["task__date"]): rec["total"]
                for rec in (
                    Assignment.objects
                    .filter(worker=w)
                    .values("task__date")
                    .annotate(total=Sum("task__duration"))
                )
            }
            w_row = OrderedDict(name=w.name)
            for d in date_cols:
                w_row[d] = w_totals.get(d, 0)
            rows.append(w_row)

    return rows

# ── JSON endpoint ────────────────────────────────────────────────────────

@require_GET
def table_api(request):
    """
    /api/table/ → list‑of‑dicts JSON
    Useful for tests, CSV export, or any machine consumer.
    """
    cols = all_dates()
    rows = build_rows(cols)
    return JsonResponse(rows, safe=False)

# ── HTML endpoint ────────────────────────────────────────────────────────

@require_GET
def table_page(request):
    """
    /table/ → rendered HTML (uses templates/table.html)
    Handy for manual inspection in a browser.
    """
    cols = all_dates()
    rows = build_rows(cols)
    return render(request, "table.html", {"rows": rows, "date_cols": cols})
