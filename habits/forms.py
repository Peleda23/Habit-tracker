from django import forms
from django.forms import ModelForm, HiddenInput, EmailField, DateTimeInput
from .models import HabitEntry, Habit


class HabitEntryForm(forms.ModelForm):
    value = forms.IntegerField(
        label="Did you do this habit on this date?",
        required=0,
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
