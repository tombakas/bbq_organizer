from django import forms
from bbq_organizer.models import Event


class EventForm(forms.ModelForm):
    class Meta:
        model = Event
        fields = ["date"]
        widgets = {
            'date': forms.DateInput(attrs={"type": "date"}),
        }
