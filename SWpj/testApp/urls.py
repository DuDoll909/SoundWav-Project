from django.urls import path
from . import views

urlpatterns = [
    path('', views.home),
    path('about/', views.about),
    path('signup/', views.signup),
    path("api/playlists/", views.playlists_api),
    path('profile/',views.profile),
]