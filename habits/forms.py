from django import forms
from .models import HabitEntry


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
