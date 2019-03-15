from django import forms

from ..models import Event

class EventProfileForm(forms.ModelForm):
    class Meta:
        model = Event
        fields = ('name', 'organizers',)


class DemoConfigurationForm(forms.ModelForm):
    class Meta:
        model = Event
        fields = ('est_time_per_demo', 'time_limit', 'min_judges_per_team', 'max_judges_per_sponsor_category',)
        labels = {
            'est_time_per_demo': 'Estimated time per demo (minutes)',
            'min_judges_per_team': 'Min. judges per team',
            'max_judges_per_sponsor_category': 'Max. judges per sponsor category',
            'time_limit': 'Time Limit (minutes)'
        }