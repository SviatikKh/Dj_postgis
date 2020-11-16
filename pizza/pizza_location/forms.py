from django import forms
from django.core import validators
from django.forms import ModelForm, widgets
from .models import Pizzeria
from django.forms import fields


class LocationForm(forms.Form):
    latitude = forms.CharField()
    longitude = forms.CharField()

    latitude.widget.attrs.update({'class': 'form-control'})
    longitude.widget.attrs.update({'class': 'form-control'})
