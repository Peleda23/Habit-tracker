from django.urls import path
from . import views

urlpatterns = [
    path("", views.heatmap_view, name="heatmap_view"),
    path(
        "create_habit/", views.UserHabitCreateView.as_view(), name="user_create_habit"
    ),
    path(
        "habit/<int:pk>/",
        views.HabitDetailView.as_view(),
        name="habit_details",
    ),
    path(
        "habit/<int:pk>/delete_habit",
        views.UserHabitDeleteView.as_view(),
        name="habit_delete",
    ),
    path(
        "habit/<int:pk>/add",
        views.UserHabitCreateEntryView.as_view(),
        name="habit_add_entry",
    ),
    path(
        "habit/<int:pk>/description_add/",
        views.UserHabitDescriptionAddView.as_view(),
        name="habit_description_add",
    ),
    path(
        "habit/<int:pk>/description_edit/",
        views.UserHabitDescriptionEditView.as_view(),
        name="habit_description_edit",
    ),
]
