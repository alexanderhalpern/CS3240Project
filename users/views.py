from django.shortcuts import render, redirect,  get_object_or_404
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from .models import Profile
from .forms import ProfileUpdateForm


def home(request):
    if request.user.is_authenticated:
        return redirect('main')
    return render(request, "home.html")


@login_required
def main(request):
    profile, created = Profile.objects.get_or_create(user=request.user)
    return render(request, "main.html", {'user':request.user, 'profile' : profile})

@login_required
def update_profile(request):
    profile = Profile.objects.get(user=request.user)
   
    if request.method == 'POST':
        form = ProfileUpdateForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            profile = form.save(commit=False)
            first_name = request.POST.get('first_name')
            if first_name: 
                request.user.first_name = first_name
                request.user.save() 
            profile.save() 
            return redirect('main')  
    else:
        form = ProfileUpdateForm(instance=profile)  
    return render(request, 'update_profile.html', {'form': form, 'first_name': request.user.first_name}) 
   

def logout_view(request):
    logout(request)
    return redirect("home")