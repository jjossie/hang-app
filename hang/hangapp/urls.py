from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),

    #ex: /hangapp/vote/4
    path('vote/<int:decisionId>/<int:userId>', views.vote, name='vote'),
    path('startUser/', views.userEntry, name='startUser'),
    path('makeUser/', views.joinSessionNewUser, name='makeUser'),
    path('addDecision/<int:sessionId>/<int:userId>', views.addDecision, name='addDecision'),
    path('voteSession/<int:sessionId>/<int:userId>', views.voteSession, name='voteSession'),
    # User id will be POSTed but the session id is in the URL.
    # path('enterSession/<int:session_id>', views.enterSession, name='enterSession'),
]