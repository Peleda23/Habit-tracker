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


@login_required
def calendar_view(request, heatmap_id):
    try:
        heatmap = Heatmap.objects.get(id=heatmap_id, user=request.user)
    except Heatmap.DoesNotExist:
        return redirect("heatmap_list")

    start_date = datetime.combine(heatmap.start_date, datetime.min.time())
    days_count = (heatmap.end_date - heatmap.start_date).days + 1
    dates = [start_date + timedelta(days=x) for x in range(days_count)]

    db_data = CalendarData.objects.filter(heatmap=heatmap)
    click_data = {data.date: data.value for data in db_data}
    values = [click_data.get(date.date(), 0) for date in dates]

    weeks_count = (days_count + start_date.weekday() + 6) // 7
    z = np.zeros((7, weeks_count))
    first_day_offset = start_date.weekday()

    for week in range(weeks_count):
        for day in range(7):
            pos = week * 7 + day - first_day_offset
            if 0 <= pos < days_count:
                z[day][week] = values[pos]

    fig = go.Figures(
        data=go.Heatmap(
            z=z,
            x=[f"Week {i + 1}" for i in range(weeks_count)],
            y=["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"],
            colorscale="Virvidis",
            showscale=True,
            text=[
                [
                    f"{start_date + timedelta(days=i)}"
                    if (i >= first_day_offset and i < days_count)
                    else ""
                    for i in range(week * 7, week * 7 + 7)
                ]
                for week in range(weeks_count)
            ],
            hoverinfo="text",
        )
    )

    fig.update_layout()
