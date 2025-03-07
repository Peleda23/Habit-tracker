"""
URL configuration for django_project project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views
from habits import views

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", views.heatmap_list_view, name="heatmap_list"),
    path("calendar/create/", views.create_heatmap_view, name="create_heatmap"),
    path("calendar/<int:heatmap_id>/", views.calendar_view, name="calendar"),
    path(
        "calendar/<int:heatmap_id>/update/",
        views.update_calendar,
        name="update_calendar",
    ),
    path("accounts/", include("accounts.urls")),
    path("accounts/", include("django.contrib.auth.urls")),
]
