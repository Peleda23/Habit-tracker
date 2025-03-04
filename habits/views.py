from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm
from .models import Heatmap, CalendarData
from .forms import HeatmapForm
import plotly.graph_objects as go
import numpy as np
from datetime import datetime, timedelta
import json


@login_required
def heatmap_list_view(request):
    heatmaps = Heatmap.objects.filter(user=request.user)
    return render(request, "heatmap_list.html", {"heatmaps": heatmaps})


@login_required
def create_heatmap_view(request):
    if request.method == "POST":
        form = HeatmapForm(request.POST)
        if form.is_valid():
            heatmap = form.save(commit=False)
            heatmap.user = request.user
            heatmap.save()
            return redirect("calendar", heatmap_id=heatmap.id)
        else:
            form = HeatmapForm()
        return render(request, "create_heatmap.html", {"form": form})
