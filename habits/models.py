from django.db import models
from accounts.models import CustomUser


class Habit(models.Model):
    name = models.CharField(max_length=255)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    description = models.TextField(blank=True, null=True)
    created = models.DateTimeField(auto_now_add=True)  # Added manually
    modified = models.DateTimeField(auto_now=True)  # Added manually

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "habits"


class HabitEntry(models.Model):
    user = models.ForeignKey(
        CustomUser, on_delete=models.DO_NOTHING, related_name="habit_entries"
    )
    habit = models.ForeignKey(Habit, on_delete=models.CASCADE)
    completed = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True)  # Added manually
    modified = models.DateTimeField(auto_now=True)  # Added manually

    def __str__(self):
        return f"{self.habit.name} - {self.created.strftime('%Y-%m-%d')} - {'Yes' if self.completed else 'No'}"

    class Meta:
        unique_together = ("user", "habit", "created")
