from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),

    #ex: /hangapp/vote/4
    path('vote/<int:decision_id>', views.vote, name='vote'),
    path('startUser/', views.userEntry, name='startUser'),
    path('makeUser/', views.makeUser, name='makeUser'),

    # User id will be POSTed but the session id is in the URL.
    path('enterSession/<int:session_id>', views.enterSession, name='enterSession'),
]