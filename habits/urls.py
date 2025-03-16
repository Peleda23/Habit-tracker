from django.urls import path
from . import views

urlpatterns = [
    path("", views.heatmap_view, name="heatmap_view"),
    path(
        "create_habit/", views.UserHabitCreateView.as_view(), name="user_create_habit"
    ),
]
