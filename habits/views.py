from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from .models import Habit, HabitEntry
from django.views import generic
from django.urls import reverse, reverse_lazy

from .forms import HabitForm, HabitEntryForm
import numpy as np

from plotly_calplot import calplot
import pandas as pd
import plotly.graph_objects as go


@login_required
def heatmap_view(request):
    # Susirandam useri
    current_user = request.user
    # Susirenkam visus habitus palei prisijungusi useri
    user_habits = Habit.objects.filter(user=current_user)
    # Jei nera habitu, grazina tuscia puslapi su zinute
    if not user_habits.exists():
        context = {
            "habit_heatmaps": [],
            "message": "No habits found. ",
            "user": current_user,
        }
        return render(request, "heatmap.html", context)
    # Tuščias listas kur krausime informacija kiekvenam habitui
    habit_heatmaps = []
    # Iteruojam per visus habitus, kad sukurtume jam kalendoriu
    for habit in user_habits:
        # Ieškom info apie habit_entry pagal useri ir habita
        data = HabitEntry.objects.filter(user=current_user, habit=habit).values(
            "date", "value"
        )
        # Jie habit_entry nėra tam habitui gražinam žinute
        if not data.exists():
            habit_heatmaps.append(
                {
                    "habit_name": habit.name,
                    "plot_div": "<p>No entries for this habit.</p>",
                }
            )
            continue
        # Konvertuojam informacija į datafreima
        df = pd.DataFrame(data)
        # Tikrinam ar turime informacijos, jei ne gražinam žinute
        if df.empty or "date" not in df.columns or "value" not in df.columns:
            habit_heatmaps.append(
                {
                    "habit_name": habit.name,
                    "plot_div": "<p>Invalid or empty data for this habit.</p>",
                }
            )
            continue

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
        # Įdedam habit varda ir calendoriu į lista
        habit_heatmaps.append(
            {
                "habit_name": habit.name,
                "plot_div": plot_div,
            }
        )
    # Surašom contexta templeitui
    context = {
        "habit_heatmaps": habit_heatmaps,
        "user": current_user,
    }

    return render(request, "heatmap.html", context)


class UserHabitCreateView(LoginRequiredMixin, generic.CreateView):
    model = Habit
    form_class = HabitForm
    template_name = "habit_create_form.html"
    # Formai užpildžius kur būsime nukreipti
    success_url = reverse_lazy("heatmap_view")

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)


class UserHabitCreateEntryView(
    LoginRequiredMixin, UserPassesTestMixin, generic.CreateView
):
    model = HabitEntry
    form_class = HabitEntryForm
    template_name = "daily_habit_input.html"
    # Formai užpildžius kur būsime nukreipti
    success_url = reverse_lazy("heatmap_view")

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

    def test_func(self):
        return self.get_object().user == self.request.user


# TODO Prideti forma, iprocio fiksavimui.
# TODO Kekviena karta prisijungus paklaustu ar noriu pazymeti koki iproti.
