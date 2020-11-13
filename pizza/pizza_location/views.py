from django.core.serializers import serialize
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.views import View
from django.views.generic import TemplateView

from pizza_location.models import Pizzeria


class IndexPageView(TemplateView):
    template_name = 'index.html'


def pizzeries_loc(request):
    pizzeries = serialize('geojson', Pizzeria.objects.all())
    return HttpResponse(pizzeries, content_type='json')
