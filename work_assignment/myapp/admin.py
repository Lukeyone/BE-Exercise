from django.contrib import admin
from .models import Position, Worker, Task, Assignment

# Basic registration ─ one line each
admin.site.register(Position)
admin.site.register(Worker)
admin.site.register(Task)
admin.site.register(Assignment)