from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from .models import Habit, HabitEntry
from .forms import HabitEntryForm
import numpy as np

# from . import utils
from plotly_calplot import calplot
import pandas as pd
import plotly.graph_objects as go


def heatmap_view(request):
    # Option 1: Fetch data from the database
    # data = Activity.objects.all().values('date', 'value')
    # df = pd.DataFrame(data)
    # df = df.rename(columns={'date': 'ds'})  # Rename to match article

    # Option 2: Generate dummy data (like the article)
    dummy_start_date = "2024-01-01"
    dummy_end_date = "2025-03-11"  # Up to today, per current date
    df = pd.DataFrame(
        {
            "ds": pd.date_range(dummy_start_date, dummy_end_date),
            "value": np.random.randint(
                low=0,
                high=30,
                size=(
                    pd.to_datetime(dummy_end_date) - pd.to_datetime(dummy_start_date)
                ).days
                + 1,
            ),
        }
    )

    # Create the Plotly calendar heatmap
    fig = calplot(
        df,
        x="ds",
        y="value",
        dark_theme=True,  # Dark theme like the article's example
        gap=0,  # Zero gap option
        colorscale="purples",  # Custom colorscale
        years_title=True,  # Show year titles
        month_lines_width=3,  # Customize month lines
        month_lines_color="#fff",
    )

    # Convert the figure to HTML for the template
    plot_div = fig.to_html(full_html=False)

    return render(request, "heatmap.html", {"plot_div": plot_div})


# @login_required
# def daily_habit_input(request):
#     habits = Habit.objects.filter(user=request.user)

#     if not habits.exists():
#         return render(request, "no_habits.html")

#     selected_date = None
#     if request.method == "POST":
#         for habit in habits:
#             form = HabitEntryForm(request.POST, prefix=str(habit.id))
#             if form.is_valid():
#                 selected_date = form.cleaned_data["date"]
#                 entry, created = HabitEntry.objects.get_or_create(
#                     user=request.user,
#                     habit=habit,
#                     created__date=selected_date,
#                     defaults={
#                         "completed": form.cleaned_data["completed"],
#                         "created": timezone.make_aware(
#                             timezone.datetime.combine(
#                                 selected_date, timezone.datetime.min.time()
#                             )
#                         ),
#                     },
#                 )
#                 if not created:
#                     entry.completed = form.cleaned_data["completed"]
#                     entry.created = timezone.make_aware(
#                         timezone.datetime.combine(
#                             selected_date, timezone.datetime.min.time()
#                         )
#                     )
#                     entry.save()
#         if selected_date:
#             return redirect("habit_heatmap")

#     forms = {
#         habit: HabitEntryForm(
#             initial={"date": timezone.now().date()}, prefix=str(habit.id)
#         )
#         for habit in habits
#     }
#     context = {"forms": forms, "selected_date": selected_date or timezone.now().date()}
#     return render(request, "daily_habit_input.html", context)


# @login_required
# def habit_heatmap(request):
#     habits = Habit.objects.filter(user=request.user)
#     if not habits.exists():
#         return render(request, "no_habits.html")

#     now = timezone.now()
#     start_date = now - timezone.timedelta(days=364)
#     date_range = utils.date_range(start_date, now)

#     habit_charts = []
#     for habit in habits:
#         # Fetch all entries for this habit
#         entries = HabitEntry.objects.filter(user=request.user, habit=habit).order_by(
#             "created"
#         )

#         # Convert to DataFrame
#         data = {
#             "date": [entry.created.date() for entry in entries],
#             "value": [1 if entry.completed else 0 for entry in entries],
#         }
#         df = pd.DataFrame(data)

#         # Create calendar heatmap with GitHub-like style and article customizations
#         fig = plotly_calplot.calplot(
#             df,
#             x="date",
#             y="value",
#             colorscale=[
#                 (0.0, "#ebedf0"),  # 0 contributions (gray)
#                 (0.5, "#ebedf0"),  # Transition point
#                 (0.5, "#c6e48b"),  # 1+ contributions (light green)
#                 (1.0, "#c6e48b"),  # Max value (light green)
#             ],
#             showscale=True,
#             years_title=True,
#             gap=0,  # No gaps between cells, as in the article's "Zero Gap" example
#             # height=320,
#             # width=1300,
#             month_lines_color="#fff",  # White month lines for dark theme
#             month_lines_width=3,
#             # dark_theme=True,  # Apply dark theme as shown in the article
#         )

#         # Customize layout
#         fig.update_layout(
#             title_text=habit.name,
#             margin=dict(t=40, b=40, l=40, r=40),
#             xaxis=dict(
#                 tickangle=0,
#                 tickfont=dict(size=12, color="#fff"),  # White text for dark theme
#                 showgrid=False,
#             ),
#             yaxis=dict(
#                 tickmode="array",
#                 tickvals=[0, 1, 2, 3, 4, 5, 6],
#                 ticktext=["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"],
#                 tickfont=dict(size=12, color="#fff"),  # White text for dark theme
#                 showgrid=False,
#             ),
#             showlegend=False,
#         )

#         # Add a border around the plot
#         fig.update_layout(
#             shapes=[
#                 dict(
#                     type="rect",
#                     xref="paper",
#                     yref="paper",
#                     x0=0,
#                     y0=0,
#                     x1=1,
#                     y1=1,
#                     line=dict(color="#fff", width=1),  # White border for dark theme
#                 )
#             ]
#         )

#         # Hide mode bar
#         chart_html = fig.to_html(config={"displayModeBar": False})
#         habit_charts.append({"name": habit.name, "chart": chart_html})

#     context = {"habit_charts": habit_charts}
#     return render(request, "habit_heatmap.html", context)
