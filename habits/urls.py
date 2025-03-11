from django.urls import path
from . import views

urlpatterns = [
    path("", views.heatmap_view, name="heatmap_view"),
]
