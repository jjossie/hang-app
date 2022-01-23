from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('start', views.userEntry, name='startUser'),
    path('join', views.newUserNewSession, name='newUserNewSession'),
    path('join/<int:sessionId>', views.newUserJoinSession, name='newUserJoinSession'),
    path('addDecision/<int:sessionId>/<int:userId>', views.addDecision, name='addDecision'),
    path('vote/<int:decisionId>/<int:userId>', views.vote, name='vote'),
    path('voteSession/<int:sessionId>/<int:userId>', views.voteSession, name='voteSession'),
]