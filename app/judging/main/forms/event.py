from django import forms

from ..models import Event

class EventProfileForm(forms.ModelForm):
    class Meta:
        model = Event
        fields = ('name', 'organizers',)
