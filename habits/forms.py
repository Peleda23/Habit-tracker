from django import forms
from .models import HabitEntry


class HabitEntryForm(forms.ModelForm):
    completed = forms.BooleanField(
        label="Did you do this habit today?", required=False, widget=forms.CheckboxInput
    )

    class Meta:
        model = HabitEntry
        fields = ["completed"]
