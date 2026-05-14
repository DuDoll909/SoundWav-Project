from django.urls import path
from . import views

urlpatterns = [
    path('', views.home),
    path('about/', views.about),
    path('signup/', views.signup),
    path('profile/',views.profile, name = "profile"),
    
    #APIs
    path("api/playlists/", views.playlists_api),

    
    #Form Pages
    path("add-song/", views.add_song,name = "add_song"),

    path('playlist_editor/',views.pedit), #short for playlist edit
    path('playlist_page/<int:playlist_id>/',views.playlist_page, name="playlist_page"), #allows for unique pages for each playlist

]