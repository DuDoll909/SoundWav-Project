from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm

def home(request):
    return render(request,"home.html")
    
def about(request):
    return render(request,"about.html")
    
def signup(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()              # creates the user
            return redirect('/accounts/login/')
    else:
        form = UserCreationForm()

    return render(request, 'registration/signup.html', {'form': form})

