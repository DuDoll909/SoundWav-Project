from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.http import JsonResponse

def home(request):
    return render(request,"home.html")
    
def about(request):
    return render(request,"about.html")
    
def profile(request):
    return render(request,"profile.html")
    
def signup(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()              # creates the user
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
