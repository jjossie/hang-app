from django.urls import path
from . import views

urlpatterns = [
    path('frontend', views.index, name='index')
]
