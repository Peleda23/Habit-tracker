from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from .models import Habit, HabitEntry
from .forms import HabitEntryForm
from . import utils
import plotly.express as px
import calendar


@login_required
def daily_habit_input(request):
    today = timezone.now().date()
    habits = Habit.objects.filter(user=request.user)

    if not habits.exists():
        return render(request, "no_habits.html")

    if request.method == "POST":
        for habit in habits:
            form = HabitEntryForm(request.POST, prefix=str(habit.id))
            if form.is_valid():
                entry, created = HabitEntry.objects.get_or_create(
                    user=request.user,
                    habit=habit,
                    created__date=today,
                    defaults={"completed": form.cleaned_data["completed"]},
                )
                if not created:
                    entry.completed = form.cleaned_data["completed"]
                    entry.save()
        return redirect("habit_heatmap")

    forms = {habit: HabitEntryForm(prefix=str(habit.id)) for habit in habits}
    context = {"forms": forms, "today": today}
    return render(request, "daily_habit_input.html", context)


@login_required
def habit_heatmap(request):
    habits = Habit.objects.filter(user=request.user)
    if not habits.exists():
        return render(request, "no_habits.html")

    # Define date range: past year to now
    now = timezone.now()
    start_date = now - timezone.timedelta(days=364)
    date_range = utils.date_range(start_date, now)

    # Calculate the number of weeks (columns) needed
    num_days = len(date_range)  # 365 days
    num_weeks = (num_days + 6) // 7  # Ceiling division to get full weeks (52 or 53)

    # Generate day names starting from the first day
    first_day = date_range[0].weekday()
    day_names = list(calendar.day_name)
    days = day_names[first_day:] + day_names[:first_day]

    # X-axis labels (start of each week)
    x_labels = [date_range[i].date() for i in range(0, num_days, 7)]

    # Generate a heatmap for each habit
    habit_charts = []
    for habit in habits:
        entries = HabitEntry.objects.filter(user=request.user, habit=habit).order_by(
            "created"
        )

        # Initialize 2D list with zeros for 7 rows (days) and num_weeks columns
        counts = [[0] * num_weeks for _ in range(7)]

        # Populate counts by mapping dates to week and day indices
        for i, dt in enumerate(date_range):
            week_number = i // 7
            day_number = dt.weekday()
            entry = entries.filter(created__date=dt.date()).first()
            counts[day_number][week_number] = 1 if entry and entry.completed else 0

        # Create Plotly heatmap
        fig = px.imshow(
            counts,
            x=x_labels,
            y=days,
            color_continuous_scale=["white", "green"],
            height=320,
            width=1300,
        )
        fig.update_traces(xgap=5, ygap=5)
        fig.update_layout(
            plot_bgcolor="white", title_text=habit.name
        )  # Add habit name as title

        # Convert to HTML and store with habit name
        chart_html = fig.to_html()
        habit_charts.append({"name": habit.name, "chart": chart_html})

    context = {"habit_charts": habit_charts}
    return render(request, "habit_heatmap.html", context)
