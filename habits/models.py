from django.db import models
from accounts.models import CustomUser


class Heatmap(models.Model):
    user = models.ForeignKey(
        CustomUser, on_delete=models.CASCADE, related_name="heatmaps"
    )
    topic = models.CharField(max_length=100)
    start_date = models.DateField()
    end_date = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("user", "topic")

    def __str__(self):
        return f"{self.user.username} - {self.topic}"


class CalendarData(models.Model):
    heatmap = models.ForeignKey(
        Heatmap, on_delete=models.CASCADE, related_name="data_pionts"
    )
    date = models.DateField()
    value = models.IntegerField(choices=[(0, "Zero"), (1, "One"), (2, "Two")])

    class Meta:
        db_table = "calendar_data"
        unique_together = ("heatmap", "data")

    def __str__(self):
        return f"{self.heatmap.topic} - {self.date}: {self.value}"
