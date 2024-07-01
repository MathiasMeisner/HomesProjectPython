# python_django/urls.py
from django.urls import path
from .views import set_csrf_token, get_homes, get_sqm_price, get_single_home_price, register_view, login_view, logout_view, home_view, user_info_view
from .sellhome import create_home
from . import views


urlpatterns = [
    path('csrf/', set_csrf_token, name='set_csrf_token'),
    path('homes/', get_homes, name='get_homes'),
    path('sqmprice/<path:municipality>/', get_sqm_price, name='get_sqm_price'),
    path('singlehome/<str:municipality>/<int:squaremeters>/<int:constructionyear>/<str:energylabel>/', get_single_home_price, name='get_single_home_price'),
    path('sellhome/', create_home, name='create_home'),
    path('register/', views.register_view, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('user/', views.get_user, name='get_user'),
    path('userinfo/', user_info_view, name='user_info'),
    path('', views.home_view, name='home'),
]