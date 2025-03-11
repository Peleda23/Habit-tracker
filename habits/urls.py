from django.urls import path
from . import views

urlpatterns = [
    path("", views.heatmap_view, name="heatmap_view"),
    # path("input/", views.daily_habit_input, name="daily_habit_input"),
    # path("habits/", views.habit_heatmap, name="habit_heatmap"),
]
