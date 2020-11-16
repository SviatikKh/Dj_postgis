from django.contrib.gis.geos import Point
from django.contrib.gis.db.models.functions import Distance
from django.contrib.gis.measure import D
from django.core.serializers import serialize
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.template import RequestContext
from django.views import View, generic
from django.views.generic import TemplateView

from pizza_location.forms import LocationForm
from pizza_location.models import Pizzeria


latitude = 48.922563
longitude = 24.710408

location = Point(longitude, latitude, srid=4326)


class IndexPageView(generic.ListView):
    context_object_name = "pizzeries"
    queryset = Pizzeria.objects.filter(location__distance_lte=(location, D(m=100000))).annotate(
        distance=Distance("location", location)).order_by("distance")
    template_name = 'index.html'


class FilterView(View):
    def get(self, request):
        form = LocationForm()
        return render(request, 'filter.html', context={'form': form})

    def post(self, request):
        search_form = LocationForm(request.POST)
        if search_form.is_valid():
            latitude = search_form.cleaned_data['latitude']
            longitude = search_form.cleaned_data['longitude']
            location = Point(float(longitude), float(latitude), srid=4326)
            context_object_name = "pizzeries"
            queryset = Pizzeria.objects.filter(location__distance_lte=(location, D(m=100000))).annotate(
                distance=Distance("location", location)).order_by("distance")
            context = {'queryset': queryset}
            return render(request, 'filter.html', context=context)



# class IndexPageView(generic.ListView):
#     context_object_name = "pizzeries"
#     queryset = Pizzeria.objects.filter(location__distance_lte=(location, D(m=100000))).annotate(
#         distance=Distance("location", location)).order_by("distance")
#     template_name = 'index.html'

#     def geocode_address(self, address):
#         address = address.encode('utf-8')
#         geocoder = Google()
#         try:
#             _, latlon = geocoder.geocode(address)
#         except (URLError, GQueryError, ValueError):
#             return None
#         else:
#             return latlon
#
# class IndexPageView(generic.ListView):
#     context_object_name = "pizzeries"
#
#     template_name = 'index.html'
#
#     def get_pizzeries(self, longitude, latitude):
#         location = geos.fromstr("POINT(%s %s)" % (longitude, latitude))
#         queryset = Pizzeria.objects.filter(location__distance_lte=(location, D(m=100000))).annotate(
#             distance=Distance("location", location)).order_by("distance")
#         return pizzeries.distance(current_point)
#
#     def home(self, request):
#         form = forms.LocationForm()
#         pizzeries = []
#         if request.POST:
#             form = forms.LocationForm(request.POST)
#             if form.is_valid():
#                 location = form.cleaned_data['location']
#                 location = geocode_address(address)
#                 if location:
#                     latitude, longitude = location
#                     pizzeries = get_pizzeries(longitude, latitude)
#
#         return render('index.html',
#                       {'form': form, 'pizzeries': pizzeries}, context_instance=RequestContext(request))

#class LatLongWidget(forms.MultiWidget):
#     """
#     A Widget that splits Point input into two latitude/longitude boxes.
#     """
#
#     def __init__(self, attrs=None, date_format=None, time_format=None):
#         widgets = (forms.TextInput(attrs=attrs),
#                    forms.TextInput(attrs=attrs))
#         super(LatLongWidget, self).__init__(widgets, attrs)
#
#     def decompress(self, value):
#         if value:
#             return tuple(reversed(value.coords))
#         return (None, None)
#
#
# class LatLongField(forms.MultiValueField):
#     widget = LatLongWidget
#     srid = 4326
#
#     default_error_messages = {
#         'invalid_latitude': ('Enter a valid latitude.'),
#         'invalid_longitude': ('Enter a valid longitude.'),
#     }
#
#     def __init__(self, *args, **kwargs):
#         fields = (forms.FloatField(min_value=-90, max_value=90),
#                   forms.FloatField(min_value=-180, max_value=180))
#         super(LatLongField, self).__init__(fields, *args, **kwargs)
#
#     def compress(self, data_list):
#         if data_list:
#             # Raise a validation error if latitude or longitude is empty
#             # (possible if LatLongField has required=False).
#             if data_list[0] in validators.EMPTY_VALUES:
#                 raise forms.ValidationError(self.error_messages['invalid_latitude'])
#             if data_list[1] in validators.EMPTY_VALUES:
#                 raise forms.ValidationError(self.error_messages['invalid_longitude'])
#             # SRID=4326;POINT(1.12345789 1.123456789)
#             srid_str = 'SRID=%d' % self.srid
#             point_str = 'POINT(%f %f)' % tuple(reversed(data_list))
#             return ';'.join([srid_str, point_str])
#         return None