from django import forms


class LocationForm(forms.Form):
    """
    Form for obtaining coordinates from the user
    """
    latitude = forms.CharField()
    longitude = forms.CharField()

    latitude.widget.attrs.update({'class': 'form-control'})
    longitude.widget.attrs.update({'class': 'form-control'})
