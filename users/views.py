from django.shortcuts import render, redirect,  get_object_or_404
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from .models import Profile


def home(request):
    if request.user.is_authenticated:
        return redirect('main')
    return render(request, "home.html")


@login_required
def main(request):
    profile, created = Profile.objects.get_or_create(user=request.user)
    
    return render(request, "main.html", {'user':request.user, 'profile' : profile})
   

def logout_view(request):
    logout(request)
    return redirect("home")
