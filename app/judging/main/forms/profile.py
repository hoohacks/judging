from django import forms
from django.contrib.auth.forms import UserChangeForm

from ..models import User


class UpdateProfileForm(UserChangeForm):
    password = None

    def __init__(self, *args, **kwargs):
        super(UpdateProfileForm, self).__init__(*args, **kwargs)
        self.fields['username'].widget.attrs.update({'class' : 'form-control'})
        self.fields['first_name'].widget.attrs.update({'class' : 'form-control'})
        self.fields['last_name'].widget.attrs.update({'class' : 'form-control'})
        self.fields['organization'].widget.attrs.update({'class' : 'form-control'})

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'organization', )
