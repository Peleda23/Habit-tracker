from django import forms
from django.forms import ModelForm, HiddenInput, EmailField, DateTimeInput
from .models import HabitEntry, Habit


class HabitEntryForm(forms.ModelForm):
    completed = forms.BooleanField(
        label="Did you do this habit on this date?",
        required=False,
        widget=forms.CheckboxInput,
    )
    date = forms.DateField(
        label="Select Date", widget=forms.DateInput(attrs={"type": "date"})
    )

    class Meta:
        model = HabitEntry
        fields = ["date"]


class HabitForm(ModelForm):
    class Meta:
        model = Habit
        fields = "__all__"
