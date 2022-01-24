from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('start', views.userEntry, name='startUser'),
    path('start/<int:sessionId>', views.userEntryWithSession,
         name='startUserWithSession'),
    path('join', views.newUserNewSession, name='newUserNewSession'),
    path('join/<int:sessionId>', views.newUserJoinSession,
         name='newUserJoinSession'),
    path('addDecision/<int:sessionId>/<int:userId>',
         views.addDecision, name='addDecision'),
    path('suggest/<int:decisionId>/<int:userId>', views.suggest, name='suggest'),
    path('voteSession/<int:sessionId>/<int:userId>',
         views.voteSession, name='voteSession'),
    path('vote/<int:optionId>/<int:userId>', views.vote, name='vote'),
    path('results/<int:decisionId>', views.results, name="results"),
]
