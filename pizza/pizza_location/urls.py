from django.urls import path

from . import views
from .views import *

urlpatterns = [
    path('', IndexPageView.as_view(), name='index'),
    path('pizzeries/', views.pizzeries_loc, name='pizzeries'),
]