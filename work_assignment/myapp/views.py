"""
myapp/views.py

WHAT THIS FILE DOES
───────────────────
1. Builds a summary table of task‑hours per day.
2. Handles edge‑cases:
      • Workers (and/or tasks) with *no* Position   → "(No Position)" group
      • Tasks with *no* Assignment                 → "Unassigned" row
3. Exposes the data in two flavours:
      • /api/table/   → JSON (for tests / export)
      • /table/       → HTML  (for humans)
"""

from collections import OrderedDict
from datetime import date
from typing import List, Dict

from django.db.models import Sum
from django.http import JsonResponse
from django.shortcuts import render
from django.views.decorators.http import require_GET

from .models import Assignment, Position, Task, Worker

from rest_framework.views import APIView          
from rest_framework.response import Response

class TableAPI(APIView):
    authentication_classes = []
    permission_classes = []

    def get(self, request):
        cols = date_columns()
        data = build_rows(cols)
        return Response(data)

# ── Helpers ──────────────────────────────────────────────────────────────


def fmt(d: date) -> str:
    """Convert 2000‑01‑11 → '11 Jan' (short & human‑friendly)."""
    return d.strftime("%d %b")


def date_columns() -> List[str]:
    """Return all distinct task dates (oldest → newest) already formatted."""
    qs = (
        Task.objects.order_by("date")
        .values_list("date", flat=True)
        .distinct()
    )
    return [fmt(d) for d in qs]


def totals_for_position(pos: Position) -> Dict[str, int]:
    """Sum duration of tasks belonging to *one* position, grouped by date."""
    return {
        fmt(r["date"]): r["total"]
        for r in (
            Task.objects.filter(position=pos)
            .values("date")
            .annotate(total=Sum("duration"))
        )
    }


def totals_for_worker(w: Worker) -> Dict[str, int]:
    """Sum duration of tasks assigned to *one* worker, grouped by date."""
    return {
        fmt(r["task__date"]): r["total"]
        for r in (
            Assignment.objects.filter(worker=w)
            .values("task__date")
            .annotate(total=Sum("task__duration"))
        )
    }


def unassigned_task_totals() -> Dict[str, int]:
    """Sum duration of tasks that have NO assignment."""
    return {
        fmt(r["date"]): r["total"]
        for r in (
            Task.objects.exclude(
                id__in=Assignment.objects.values("task_id")
            )
            .values("date")
            .annotate(total=Sum("duration"))
        )
    }


# ── Core aggregation ─────────────────────────────────────────────────────


def build_rows(cols: List[str]) -> List[OrderedDict]:
    """Return one OrderedDict per table row (positions first, then workers)."""
    rows: List[OrderedDict] = []

    # 1. regular positions (those that actually have workers)
    for pos in (
        Position.objects.filter(workers__isnull=False)
        .distinct()
        .order_by("id")
    ):
        # --- position row ------------------------------------------------
        p_row = OrderedDict(name=pos.name)
        p_totals = totals_for_position(pos)
        for d in cols:
            p_row[d] = p_totals.get(d, 0)
        rows.append(p_row)

        # --- worker rows -------------------------------------------------
        for w in pos.workers.order_by("id"):
            w_row = OrderedDict(name=w.name)
            w_totals = totals_for_worker(w)
            for d in cols:
                w_row[d] = w_totals.get(d, 0)
            rows.append(w_row)

    # 2. workers WITHOUT a position  → "(No Position)" pseudo‑group
    no_pos_workers = Worker.objects.filter(position__isnull=True).order_by("id")
    if no_pos_workers.exists():
        # group row (tasks whose position is NULL)
        group_row = OrderedDict(name="(No Position)")
        group_totals = {
            fmt(r["date"]): r["total"]
            for r in (
                Task.objects.filter(position__isnull=True)
                .values("date")
                .annotate(total=Sum("duration"))
            )
        }
        for d in cols:
            group_row[d] = group_totals.get(d, 0)
        rows.append(group_row)

        # individual worker rows
        for w in no_pos_workers:
            w_row = OrderedDict(name=w.name)
            w_totals = totals_for_worker(w)
            for d in cols:
                w_row[d] = w_totals.get(d, 0)
            rows.append(w_row)

    # 3. tasks WITHOUT an assignment  → "Unassigned" summary row
    un_totals = unassigned_task_totals()
    if un_totals:  # only include if such tasks exist
        u_row = OrderedDict(name="Unassigned")
        for d in cols:
            u_row[d] = un_totals.get(d, 0)
        rows.append(u_row)

    return rows


# ── Endpoints ────────────────────────────────────────────────────────────


@require_GET
def table_api(request):
    """/api/table/ → JSON list of dicts (easy for tests / exports)."""
    cols = date_columns()
    data = build_rows(cols)
    return JsonResponse(data, safe=False)


@require_GET
def table_page(request):
    """/table/ → HTML table for quick human inspection."""
    cols = date_columns()
    data = build_rows(cols)
    return render(
        request,
        "table.html",
        {
            "rows": data,
            "date_cols": cols,
        },
    )
