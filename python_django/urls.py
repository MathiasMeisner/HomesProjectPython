# python_django/urls.py
from django.urls import path
from .views import get_homes, get_sqm_price, get_single_home_price
from .sellhome import create_home


urlpatterns = [
    path('homes/', get_homes, name='get_homes'),
    path('sqmprice/<path:municipality>/', get_sqm_price, name='get_sqm_price'),
    path('singlehome/<str:municipality>/<int:squaremeters>/<int:constructionyear>/<str:energylabel>/', get_single_home_price, name='get_single_home_price'),
    path('sellhome/', create_home, name='create_home'),
]