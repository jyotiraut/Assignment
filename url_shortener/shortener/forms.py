from django import forms
from .models import ShortURL
from django.contrib.auth.models import User

class ShortURLForm(forms.ModelForm):
    custom_key = forms.CharField(required=False)
    expires_at = forms.DateTimeField(required=False, widget=forms.DateTimeInput(attrs={'type': 'datetime-local'}))

    class Meta:
        model = ShortURL
        fields = ['original_url']
