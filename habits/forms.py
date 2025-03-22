from django import forms
from django.forms import ModelForm
from .models import HabitEntry, Habit


class HabitEntryForm(forms.ModelForm):
    value = forms.BooleanField(
        label="Did you do this habit on this date?",
        required=False,
        widget=forms.CheckboxInput,
    )
    date = forms.DateField(
        label="Select Date", widget=forms.DateInput(attrs={"type": "date"})
    )

    class Meta:
        model = HabitEntry
        fields = ["date", "value"]


class HabitForm(ModelForm):
    class Meta:
        model = Habit
        fields = ["name", "description"]


class HabitDescriptionAddForm(ModelForm):
    class Meta:
        model = Habit
        fields = ["description"]


class HabitDescriptionEditForm(ModelForm):
    class Meta:
        model = Habit
        fields = ["description"]
