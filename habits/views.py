from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from .models import Habit, HabitEntry
from django.views import generic
from django.urls import reverse_lazy, reverse
from django.db.models import Count, Max
from django.utils import timezone
import requests


from .forms import (
    HabitForm,
    HabitEntryForm,
    HabitDescriptionEditForm,
    HabitDescriptionAddForm,
)
import numpy as np

from plotly_calplot import calplot
import pandas as pd
import plotly.graph_objects as go


@login_required
def heatmap_view(request):
    # Get current user
    current_user = request.user

    # Get all habits for the current user
    user_habits = Habit.objects.filter(user=current_user).annotate(
        entry_count=Count("entries"),  # Default related name if not specified
        last_entry_date=Max("entries__date"),
    )

    # Calculate total number of habits
    total_habits = user_habits.count()

    # If no habits exist, return empty page with message
    if not user_habits.exists():
        context = {
            "habit_names": [],
            "message": "No habits found.",
            "user": current_user,
            "total_habits": 0,
        }
        return render(request, "heatmap.html", context)

    # Current date for comparison
    now = timezone.now()

    # Create list of habit names
    habit_names = [
        {
            "id": habit.pk,
            "name": habit.name,
            "entry_count": habit.entry_count,
            "days_since_created": (now - habit.created).days,
            "hours_since_created": ((now - habit.created).seconds // 3600)
            % 24,  # Remaining hours
            "days_since_last_entry": (now - habit.last_entry_date).days + 1
            if habit.last_entry_date
            else None,
        }
        for habit in user_habits
    ]

    # Prepare context for template
    context = {
        "habit_names": habit_names,
        "user": current_user,
        "total_habits": total_habits,
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


class HabitDetailView(generic.DetailView):
    model = Habit
    context_object_name = "habit"
    template_name = "habit_details.html"
    success_url = reverse_lazy("heatmap_view")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        habit = self.get_object()
        current_user = self.request.user
        # Gauti įpročio įrašus
        data = HabitEntry.objects.filter(user=current_user, habit=habit).values(
            "date", "value"
        )
        if not data.exists():
            context["plot_div"] = "<p>No entries for this habit.</p>"
            return context
        # Konvertuoti duomenis į pandas DataFrame
        df = pd.DataFrame(data)
        if df.empty or "date" not in df.columns or "value" not in df.columns:
            context["plot_div"] = "<p>Invalid or empty data for this habit.</p>"
            return context
        df["date"] = pd.to_datetime(df["date"]).dt.date
        df = df.rename(columns={"date": "ds"})  # Sutvarkome stulpelių pavadinimus
        # Sugeneruoti Plotly kalendoriaus heatmap'ą
        fig = calplot(
            df,
            x="ds",
            y="value",
            dark_theme=False,
            gap=2,
            colorscale=[(0, "white"), (1, "green")],
            years_title=True,
            month_lines_width=1,
            month_lines_color="black",
        )

        # Add the heatmap and quotes to the context
        context["plot_div"] = fig.to_html(full_html=False)

        # Add quotes to the context
        api_url = "https://api.api-ninjas.com/v1/quotes"
        response = requests.get(
            api_url, headers={"X-Api-Key": "2upTib173qiLhwUqbVRZtQ==GbDXZrXm3DIDHHYN"}
        )
        if response.status_code == requests.codes.ok:
            data = response.json()
            context["quotes"] = data[0]["quote"]
            context["author"] = data[0]["author"]
        else:
            context["quotes"] = f"Error fetching quotes: {response.status_code}"

        return context


class UserHabitCreateEntryView(LoginRequiredMixin, generic.CreateView):
    model = HabitEntry
    context_object_name = "habit"
    form_class = HabitEntryForm
    template_name = "daily_habit_input.html"
    # Formai užpildžius kur būsime nukreipti
    success_url = reverse_lazy("heatmap_view")

    def form_valid(self, form):
        form.instance.user = self.request.user
        form.instance.habit = Habit.objects.get(pk=self.kwargs["pk"])
        return super().form_valid(form)

    # Displaying habits name.
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Fetch the habit object using the primary key from the URL
        habit = Habit.objects.get(pk=self.kwargs["pk"])
        context["habit_name"] = habit.name  # Add the habit name to the context
        return context

    def test_func(self):
        return self.get_object().user == self.request.user

    # After submiting returning to habit details.
    def get_success_url(self):
        return reverse("habit_details", kwargs={"pk": self.kwargs["pk"]})


class UserHabitDescriptionAddView(LoginRequiredMixin, generic.UpdateView):
    model = Habit
    form_class = HabitDescriptionAddForm
    template_name = "habit_description_add_form.html"
    success_url = reverse_lazy("heatmap_view")

    def form_valid(self, form):
        form.instance.user = self.request.user
        form.instance.habit = Habit.objects.get(pk=self.kwargs["pk"])
        return super().form_valid(form)

    def test_func(self):
        return self.get_object().user == self.request.user

    # After submiting returning to habit details
    def get_success_url(self):
        return reverse("habit_details", kwargs={"pk": self.object.id})


class UserHabitDescriptionEditView(LoginRequiredMixin, generic.UpdateView):
    model = Habit
    form_class = HabitDescriptionEditForm
    template_name = "habit_description_edit_form.html"
    success_url = reverse_lazy("heatmap_view")

    def form_valid(self, form):
        form.instance.user = self.request.user
        form.instance.habit = Habit.objects.get(pk=self.kwargs["pk"])
        return super().form_valid(form)

    def test_func(self):
        return self.get_object().user == self.request.user

    def get_success_url(self):
        return reverse("habit_details", kwargs={"pk": self.object.id})


class UserHabitDeleteView(LoginRequiredMixin, UserPassesTestMixin, generic.DeleteView):
    model = Habit
    success_url = reverse_lazy("heatmap_view")
    context_object_name = "habit"
    template_name = "habit_delete.html"

    def test_func(self):
        return self.get_object().user == self.request.user


# TODO Add profile picture.
# TODO After adding entry or description return to habit details.
# TODO Style calendar
