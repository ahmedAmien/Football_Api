from django.urls import path
from . import views

urlpatterns = [
    path("", views.index),
    path('top_leagues/',views.top_ten_leagues),
]