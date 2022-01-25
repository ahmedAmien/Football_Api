from django.urls import path
from . import views

urlpatterns = [
    path("", views.index),
    path("add_player/<int:page>/", views.add_player),
    path("add_teams_to_player/", views.add_teams_to_player),
    path('top_leagues/',views.top_ten_leagues),
    path('leagues/',views.all_leagues),
    path('teams/',views.teams),
    path('leagues_teams/',views.leagues_teams),
    path('add_leagues_seasons_teams', views.add_leagues_seasons_teams),
    # path('player_static/', views.player_static)
]