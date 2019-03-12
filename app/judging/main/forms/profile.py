from django import forms
from django.contrib.auth.forms import UserChangeForm

from ..models import User


class UpdateProfileForm(UserChangeForm):
    password = None

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'organization', )
