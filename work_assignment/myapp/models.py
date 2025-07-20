from django.db import models

# Basic role or job type, e.g. "Engineer", "Manager", etc.
class Position(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name
     

# A person who can be assigned to tasks. They optionally belong to a Position.
class Worker(models.Model):
    name = models.CharField(max_length=100)

    # If a worker has a role, it's linked here (e.g. Alice is a 'Manager')
    # Nullable so we can support unassigned/freelancers/general pool
    position = models.ForeignKey(
        Position,
        related_name="workers",
        on_delete=models.CASCADE,
        null=True, blank=True,
    )

    def __str__(self):
        return self.name


# Something that needs to be done on a certain date, for a position (e.g. "Shift for Nurse on Jan 5")
class Task(models.Model):
    # Position required for this task (e.g. this task is only for an Engineer)
    position = models.ForeignKey(
        Position,
        related_name="tasks",
        on_delete=models.CASCADE,
        null=True, blank=True,
    )

    date     = models.DateField()           # When the task is scheduled
    duration = models.IntegerField()        # How long it goes for (in hours or minutes – up to project)

    def __str__(self):
        return f"{self.position.name} @ {self.date}"


# An assignment = a task being given to a specific worker
class Assignment(models.Model):
    task   = models.ForeignKey(Task, related_name='assignments', on_delete=models.CASCADE)
    worker = models.ForeignKey(Worker, related_name='assignments', on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.task} → {self.worker}"
