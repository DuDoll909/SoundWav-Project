from django.urls import path
from . import views

urlpatterns = [
    path('', views.home),
    path('about/', views.about),
    path('signup/', views.signup),
    path('profile/',views.profile),
    
    #APIs
    path("api/playlists/", views.playlists_api),

    
    #Form Pages
    path("add-song/", views.add_song,name = "add_song"),
]