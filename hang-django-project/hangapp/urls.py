from django.urls import path, include

from . import views

from rest_framework import routers

router = routers.DefaultRouter()
router.register(r'options', views.OptionViewSet)
router.register(r'decisionViewSet', views.DecisionViewSet)
router.register(r'hangoutViewSet', views.HangoutViewSet)

urlpatterns = [
    # path('', views.index, name='index'),

    path('api/', include(router.urls)),  # REST API URLs generated by the Router

    # *** REST API URLs made by me (Function-based) ***
    # TODO Refactor this whole URL scheme because it's a mess
    # Decisions
    # path('api/decision/<int:pk>/', views.decision_detail),
    path('api/decision-add/', views.add_decision),
    # Hangouts
    # path('api/hangout/<int:pk>/', views.get_hangout_detail),
    path('api/hangout/<int:pk>/decision/', views.get_decision_for_hangout),
    path('api/hangout/<int:hangout_pk>/is-ready/', views.are_homies_ready),
    # Options
    path('api/decision/<int:pk>/options/', views.get_options_for_decision),
    path('api/option-add/<int:decision_pk>/', views.add_option),
    path('api/option-vote/<int:pk>/', views.vote_on_option),
    path('api/results/<int:decision_pk>/', views.get_results),
    # Homies
    path('api/homie/ready-up/', views.ready_up_homie),
    path('api/join-hangout/', views.api_join_hangout),
    path('api/join-hangout/<int:hangout_id>', views.api_join_hangout),
    path('api/user-exit/', views.logout_view),
    #
    # path('start', views.user_entry, name='startUser'),
    # path('start/<int:session_id>', views.user_entry_with_session,
    #      name='startUserWithSession'),
    # path('join', views.new_user_new_session, name='newUserNewSession'),
    # path('join/<int:session_id>', views.new_user_join_session,
    #      name='newUserJoinSession'),
    # path('addDecision/<int:session_id>/<int:user_id>',
    #      views.add_decision, name='addDecision'),
    # path('suggest/<int:decision_id>/<int:user_id>', views.suggest, name='suggest'),
    # path('voteSession/<int:session_id>/<int:user_id>',
    #      views.vote_session, name='voteSession'),
    # path('vote/<int:option_id>/<int:user_id>', views.vote, name='vote'),
    # path('results/<int:decision_id>', views.results, name="results"),
]





