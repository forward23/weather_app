from django import forms

from weather.models import City


class CityForm(forms.Form):
    name = forms.CharField(max_length=50,
                           widget=forms.TextInput(attrs={'class': 'input', 'placeholder': 'City Name'}))
