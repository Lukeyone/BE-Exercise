from django.contrib import admin
from .models import Position, Worker, Task, Assignment

# Basic registration ─ one line each
admin.site.register(Position)
admin.site.register(Worker)
admin.site.register(Task)
admin.site.register(Assignment)

# ── OR ── use ModelAdmin classes for nicer display:
#
# @admin.register(Position)
# class PositionAdmin(admin.ModelAdmin):
#     list_display = ('id', 'name')
#
# @admin.register(Worker)
# class WorkerAdmin(admin.ModelAdmin):
#     list_display = ('id', 'name', 'position')
#
# … etc.
