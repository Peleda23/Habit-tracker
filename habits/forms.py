from django import forms
from .models import Heatmap


class HeatmapForm(forms.ModelForm):
    class Meta:
        model = Heatmap
        fields = ["topic", "start_date", "end_date"]
        widgets = {
            "start_date": forms.DateInput(attrs={"type": "date"}),
            "end_date": forms.DateInput(attrs={"type": "date"}),
        }

    # Tikrinam ar viskas suvesta teisingai, ar laukai netusti ir ar datos eina logiska seka.
    def clean(self):
        cleaned_data = super().clean()
        start_date = cleaned_data.get("start_date")
        end_date = cleaned_data.get("end_date")
        if start_date and end_date and end_date < start_date:
            raise forms.ValidationError("End date must be after start date .")
        return cleaned_data
