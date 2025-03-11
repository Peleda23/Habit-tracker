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
    # data = Activity.objects.all().values('date', 'value')
    # df = pd.DataFrame(data)
    # df = df.rename(columns={'date': 'ds'})  # Rename to match article

    # Option 2: Generate dummy data (like the article)
    current_year = datetime.datetime.now().year
    dummy_start_date = f"{current_year}-01-01"
    dummy_end_date = datetime.datetime.now()  # Up to today, per current date
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
        dark_theme=False,  # Dark theme like the article's example
        gap=0,  # Zero gap option
        colorscale="purples",  # Custom colorscale
        years_title=True,  # Show year titles
        month_lines_width=3,  # Customize month lines
        month_lines_color="#fff",
    )

    # Convert the figure to HTML for the template
    plot_div = fig.to_html(full_html=False)

    return render(request, "heatmap.html", {"plot_div": plot_div})
