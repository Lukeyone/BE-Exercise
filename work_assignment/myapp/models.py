from django.db import models

class Position(models.Model):
    name = models.CharField(max_length=100)
    def __str__(self):
        return self.name
     
class Worker(models.Model):
    name = models.CharField(max_length=100)
    position = models.ForeignKey(Position, related_name='workers', on_delete=models.CASCADE)
    def __str__(self):
        return self.name

class Task(models.Model):
    position = models.ForeignKey(Position, related_name='tasks', on_delete=models.CASCADE)
    date = models.DateField()
    duration = models.IntegerField()
    def __str__(self):
        return f"{self.position.name} @ {self.date}"
    
class Assignment(models.Model):
    task = models.ForeignKey(Task, related_name='assignments', on_delete=models.CASCADE)
    worker = models.ForeignKey(Worker, related_name='assignments', on_delete=models.CASCADE)
    def __str__(self):
        return f"{self.task} → {self.worker}"