from django.shortcuts import render, redirect
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required


def home(request):
    if request.user.is_authenticated:
        return redirect('main')
    return render(request, "home.html")


@login_required
def main(request):
    return render(request, "main.html")


def logout_view(request):
    logout(request)
    return redirect("home")
