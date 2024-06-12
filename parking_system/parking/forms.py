from django import forms
from .models import Car
from django.contrib.auth.models import User


class CarForm(forms.ModelForm):

    class Meta:
        model = Car
        fields = ['reg_mark', 'model', 'color', "fare", "confirmed", "user"]
