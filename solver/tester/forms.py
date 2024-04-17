from django import forms

from .models import Test


class AddTestForm(forms.ModelForm):
    class Meta:
        model = Test
        fields = ['title', 'status']
