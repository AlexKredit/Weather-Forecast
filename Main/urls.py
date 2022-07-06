from django.urls import path
from . import views


urlpatterns = [
    path('', views.first_search, name='search'),
    path('searched/', views.index, name='index')
]
