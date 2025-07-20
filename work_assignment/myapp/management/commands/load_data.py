import json
import os
from django.core.management.base import BaseCommand
from myapp.models import Position, Worker, Task, Assignment

class Command(BaseCommand):
    help = 'Loads data from JSON files into the database'

    def handle(self, *args, **kwargs):
        BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
        DATA_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), 'fixtures')

        with open(os.path.join(DATA_DIR, 'positions.json')) as f:
            positions = json.load(f)
            for p in positions:
                Position.objects.update_or_create(id=p['id'], defaults={'name': p['name']})

        with open(os.path.join(DATA_DIR, 'workers.json')) as f:
            workers = json.load(f)
            for w in workers:
                position = Position.objects.get(id=w['position_id'])
                Worker.objects.update_or_create(id=w['id'], defaults={'name': w['name'], 'position': position})

        with open(os.path.join(DATA_DIR, 'tasks.json')) as f:
            tasks = json.load(f)
            for t in tasks:
                position = Position.objects.get(id=t['position_id'])
                Task.objects.update_or_create(
                    id=t['id'],
                    defaults={
                        'position': position,
                        'duration': t['duration'],
                        'date': t['date']
                    }
                )

        with open(os.path.join(DATA_DIR, 'assignments.json')) as f:
            assignments = json.load(f)
            for a in assignments:
                task = Task.objects.get(id=a['task_id'])
                worker = Worker.objects.get(id=a['worker_id'])
                Assignment.objects.update_or_create(task=task, worker=worker)

        self.stdout.write(self.style.SUCCESS('Data successfully loaded'))
