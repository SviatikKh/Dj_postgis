from django.db import models
from django.contrib.gis.db import models


class Pizzeria(models.Model):
    city = models.CharField(max_length=75)
    street = models.CharField(max_length=100)
    build_number = models.CharField(max_length=50)
    location = models.PointField(null=True, blank=True, srid=4326)

    def __str__(self):
        return self.city
