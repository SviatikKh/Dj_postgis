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

#Coordinates for the map (may be change to user location (geocoder google)
latitude = 48.922563
longitude = 24.710408

location = Point(longitude, latitude, srid=4326)


class IndexPageView(generic.ListView):
    """
        Map with points of pizzeries, and list of coordinates

    """
    context_object_name = "pizzeries"
    queryset = Pizzeria.objects.filter(location__distance_lte=(location, D(m=100000))).annotate(
        distance=Distance("location", location)).order_by("distance")
    template_name = 'index.html'


class FilterView(View):
    """
        To get from user his coordinates
    """
    def get(self, request):
        form = LocationForm()
        return render(request, 'filter.html', context={'form': form})

    def post(self, request):
        """
        Return user filtered coordinates of pizzeries
        """
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



