from django.db import models
from django.utils import timezone
from accounts.models import CustomUser


class Habit(models.Model):
    name = models.CharField(max_length=100)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    description = models.TextField(blank=True, null=True)
    created = models.DateTimeField(auto_now_add=True)  # Added manually
    modified = models.DateTimeField(auto_now=True)  # Added manually

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "habits"


class HabitEntry(models.Model):
    habit = models.ForeignKey(Habit, on_delete=models.CASCADE)
    date = models.DateTimeField(default=timezone.now)  # Added manually
    value = models.IntegerField(default=0)  # Added manually

    def __str__(self):
        return f"{self.habit.name} - {self.date}:{self.value}"
