from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
import json
import os

def home(request):
    base_dir = os.path.dirname(os.path.abspath(__file__))
    json_path = os.path.join(base_dir, "data", "songs.json")
    
    with open(json_path, "r") as f:
        data = json.load(f)
        
    songs = data.get("songs", [])
    
    return render(request, "testApp/home.html",{"songs": songs})
    
def about(request):
    return render(request,"testApp/about.html")
    
def profile(request):
    playlists = []

    if request.user.is_authenticated:

          base_dir = os.path.dirname(
            os.path.abspath(__file__)
          )

          json_path = os.path.join(
            base_dir,
            "data",
            "playlists.json"
        )

    try:
            with open(json_path, "r") as f:
                data = json.load(f)

    except (
            FileNotFoundError,
            json.JSONDecodeError
        ):
            data = {"playlists": []}

    all_playlists = data.get(
            "playlists",
            []
        )

    # Only playlists from current user
    playlists = [
            playlist
            for playlist in all_playlists
            if int(playlist["user_id"]) == request.user.id
        ]
    return render(request,"testApp/profile.html", {"playlists": playlists})


    
def signup(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()             
            return redirect('/accounts/login/')
    else:
        form = UserCreationForm()

    return render(request, 'registration/signup.html', {'form': form})

def playlists_api(request):
    data = {
        "playlists": [
            {"id": 1, "name": "My Favorites"},
            {"id": 2, "name": "Chill Vibes"},
        ]
    }
    return JsonResponse(data)
def add_song(request):
    if request.method == "POST":
        name = request.POST["name"]
        artist = request.POST["artist"]
        album = request.POST["album"]
        
        base_dir = os.path.dirname(os.path.abspath(__file__))
        json_path = os.path.join(base_dir, "data", "songs.json")
        
        with open(json_path, "r") as f:
            data = json.load(f)
            
        songs = data.get("songs", [])
        
        new_id = songs[-1]["id"] + 1 if songs else 1
        
        new_song = {
        "id": new_id,
        "name": name,
        "artist": artist,
        "album": album
        }
        
        songs.append(new_song)
        data["songs"] = songs
        with open(json_path, "w") as f:
            json.dump(data, f, indent = 4)
            
        return redirect("add_song")
        
    return render(request, "testApp/add_song.html")


def pedit(request):
    if request.method == "POST":
       playlist_name = request.POST["playlist_name"]
       user_id = request.user.id

       base_dir = os.path.dirname(os.path.abspath(__file__))
       json_path = os.path.join(base_dir, "data", "playlists.json")

       # Read existing data
       with open(json_path, "r") as f:
          data = json.load(f)

       playlists = data.get("playlists", [])

       # Generate new ID
       new_id = playlists[-1]["id"] + 1 if playlists else 1

       # Create new playlist object
       new_playlist = {
        "id": new_id,
        "playlist_name": playlist_name,
        "user_id": user_id,
        "songs":[],
    }

      # Append and save
       playlists.append(new_playlist)
       data["playlists"] = playlists

       with open(json_path, "w") as f:
          json.dump(data, f, indent=4)

       return redirect("profile")
    return render(request, "testApp/playlist_editor.html")

def playlist_page(request, playlist_id):

    base_dir = os.path.dirname(
        os.path.abspath(__file__)
    )

    json_path = os.path.join(
        base_dir,
        "data",
        "playlists.json"
    )

    try:
        with open(json_path, "r") as f:
            data = json.load(f)

    except (
        FileNotFoundError,
        json.JSONDecodeError
    ):
        data = {"playlists": []}

    playlists = data.get(
        "playlists",
        []
    )

    playlist = None

    for p in playlists:

        if p["id"] == playlist_id:
            playlist = p
            break

    return render(
        request,
        "testApp/playlist_page.html",
        {
            "playlist": playlist
        }
    )
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.path.join(BASE_DIR, "testApp", "data")

SONGS_FILE = os.path.join(DATA_DIR, "songs.json")
PLAYLISTS_FILE = os.path.join(DATA_DIR, "playlists.json")


def load_songs():
    with open(SONGS_FILE, 'r') as f:
        return json.load(f)


def load_playlists():
    with open(PLAYLISTS_FILE, 'r') as f:
        return json.load(f)


def save_playlists(playlists):
    with open(PLAYLISTS_FILE, 'w') as f:
        json.dump(playlists, f, indent=4)


def playlist_page(request, playlist_id):

    songs = load_songs()["songs"]
    playlists = load_playlists()["playlists"]

    playlist = next(
        (p for p in playlists if p["id"] == playlist_id),
        None
    )

    playlist_songs = []

    if playlist:

        for song_id in playlist["songs"]:

            song = next(
                (s for s in songs if s["id"] == song_id),
                None
            )

            if song:
                playlist_songs.append(song)

    context = {
        "playlist": playlist,
        "playlist_songs": playlist_songs,
        "all_songs": songs
    }

    return render(request, "testApp/playlist_page.html", context)

@csrf_exempt
def save_playlist(request, playlist_id):

    if request.method == "POST":

        data = json.loads(request.body)
        updated_song_ids = data.get("songs", [])

        # load file
        with open(PLAYLISTS_FILE, "r") as f:
            file_data = json.load(f)

        playlists = file_data["playlists"]

        playlist_id = int(playlist_id)

        found = False

        for playlist in playlists:
            if playlist["id"] == playlist_id:
                playlist["songs"] = updated_song_ids
                found = True

        if not found:
            return JsonResponse({
                "status": "error",
                "message": "Playlist not found"
            })

        # save back full structure
        with open(PLAYLISTS_FILE, "w") as f:
            json.dump(file_data, f, indent=4)

        
        return JsonResponse({
            "status": "success"
        })


