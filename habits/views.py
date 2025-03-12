from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from .models import Habit, HabitEntry
from .forms import HabitEntryForm
import numpy as np
import datetime

# from . import utils
from plotly_calplot import calplot
import pandas as pd
import plotly.graph_objects as go


def heatmap_view(request):
    # Option 1: Fetch data from the database
    data = HabitEntry.objects.all().values("date", "value")

    df = pd.DataFrame(data)

    # Sutvarko data kad nebūtu sekundžiu, su sekundėm neatvaizduoja
    df["date"] = pd.to_datetime(df["date"]).dt.date
    df = df.rename(columns={"date": "ds"})  # Rename to match article
    print(df)

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

    return render(request, "heatmap.html", {"plot_div": plot_div})
