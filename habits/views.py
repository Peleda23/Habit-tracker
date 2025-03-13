from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import Habit, HabitEntry
from .forms import HabitEntryForm
import numpy as np


# from . import utils
from plotly_calplot import calplot
import pandas as pd
import plotly.graph_objects as go


@login_required
def heatmap_view(request):
    current_user = request.user
    user_habits = Habit.objects.filter(user=current_user)
    # Renkam informacija iš duomenų bazes
    data = HabitEntry.objects.filter(user=current_user).values("date", "value")

    if not data.exists():
        context = {
            "plot_div": "<p>No habit entries found.</p>",
            "user": current_user,
            "habit": user_habits,
        }
        return render(request, "heatmap.html", context)
    df = pd.DataFrame(data)

    # Sutvarko data kad nebūtu sekundžiu, su sekundėm neatvaizduoja
    df["date"] = pd.to_datetime(df["date"]).dt.date

    df = df.rename(columns={"date": "ds"})  # Rename to match article

    # Create the Plotly calendar heatmap
    fig = calplot(
        df,
        x="ds",
        y="value",
        dark_theme=False,  # Dark theme like the article's example
        gap=0,  # Zero gap option
        colorscale=[
            (0, "white"),
            (1, "green"),
        ],  # Custom colorscale
        years_title=True,  # Show year titles
        month_lines_width=1,  # Customize month lines
        month_lines_color="black",
    )

    # Convert the figure to HTML for the template
    plot_div = fig.to_html(full_html=False)
    context = {"plot_div": plot_div, "user": current_user, "habit": user_habits}

    return render(request, "heatmap.html", context)
