from django.urls import path
from . import views


urlpatterns = [
    path('', views.api_overview, name='api_overview'),
    path('player/<str:pk>', views.player, name='player'),
    path('player/<str:pk>/matches/', views.player_matches, name='player_matches'),
    path('players/', views.players, name='players'),
    path('tourney/<str:pk>', views.tourney, name='tourney'),
    path('tourney/<str:pk>/matches/', views.tourney_matches, name='tourney_matches'),
    path('match/<str:pk>', views.match, name='match'),
    path('matches/', views.matches, name='matches'),
    path('tourneys/', views.tourneys, name='tourneys'),
]
