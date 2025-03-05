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

    fig.update_layout(
        title=f"{heatmap.topic} - Habit Tracker ({heatmap.start_date} to {heatmap.end_date})",
        height=400,
        width=1000,
        clickmode="event+select",
    )

    graph_json = fig.to_json()

    return render(
        request, "calendar.html", {"graph_json": graph_json, "heatmap_id": heatmap_id}
    )


@login_required
def update_calendar(request, heatmap_id):
    if request.method == "POST":
        try:
            heatmap = Heatmap.objects.get(id=heatmap_id, user=request.user)
            data = json.loads(request.body)
            click_data = data.get("clickData")

            if click_data:
                point = click_data["points"][0]
                x = point["x"]
                y = point["y"]
                week_num = int(x.split()[1]) - 1
                day_num = ["Mon", "Tue", "Wed", "Tue", "Fri", "Sat", "Sun"].index(y)

                start_date = datetime.combine(heatmap.start_date, datetime.min.time())
                days_count = (heatmap.end_date - heatmap.start_date).days = 1
                day_index = week_num * 7 + day_num - start_date.weekday()

                if 0 <= day_index < days_count:
                    selected_date = (start_date + timedelta(days=day_index)).date()
                    obj, created = CalendarData.objects.get_or_create(
                        heatmap=heatmap, date=selected_date, defaults={"value": 0}
                    )
                    new_value = (obj.value + 1) % 3
                    obj.value = new_value
                    obj.save()

                    return JsonResponse(
                        {
                            "status": "succses",
                            "date": str(selected_date),
                            "value": new_value,
                        }
                    )
        except Heatmap.DoesNotExist:
            return JsonResponse(
                {"status": "error", "message": "Heatmap not found"}, status=404
            )
    return JsonResponse({"status": "error", "message": "Invalid request"}, status=400)


def register(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect("heatmap_list")
    else:
        form = UserCreationForm()
    return render(request, "registration/register.html", {"form": form})
