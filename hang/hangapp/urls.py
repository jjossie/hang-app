from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('vote/<int:decision_id>', views.vote, name='vote'),
]