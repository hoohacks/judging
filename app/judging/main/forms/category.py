from django import forms

from ..models import Category


class CategoryUpdateForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ('name', 'organization', 'number_winners', 'min_judges', 'is_opt_in', 'judges')
