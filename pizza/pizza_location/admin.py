from django.contrib import admin
from .models import Pizzeria
from leaflet.admin import LeafletGeoAdmin


class PizzeriaAdmin(LeafletGeoAdmin):
    list_display = ('city', 'coordinates')


admin.site.register(Pizzeria, PizzeriaAdmin)

