from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    #ex: /hangapp/vote/4
    path('vote/<int:decision_id>', views.vote, name='vote'),
    path('startUser/', views.userEntry, name='startUser'),
    path('startSession/<int:session_id>', views.startSession, name='startSession'),
]