from django.contrib.gis.geos import Point
from django.contrib.gis.db.models.functions import Distance
from django.contrib.gis.measure import D
from django.core.serializers import serialize
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.views import View, generic
from django.views.generic import TemplateView

from pizza_location.models import Pizzeria

latitude = 48.922563
longitude = 24.710408

location = Point(longitude, latitude, srid=4326)


class IndexPageView(generic.ListView):
    context_object_name = "pizzeries"
    queryset = Pizzeria.objects.filter(location__distance_lte=(location, D(m=100000))).annotate(
        distance=Distance("location", location)).order_by("distance")
    template_name = 'index.html'

# def pizzeries_loc(request):
#     pizzeries = serialize('geojson', Pizzeria.objects.all())
#     return HttpResponse(pizzeries, content_type='json')
