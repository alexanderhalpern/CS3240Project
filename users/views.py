from django.shortcuts import render, redirect,  get_object_or_404, reverse
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from .models import Profile, Project
from .forms import ProfileUpdateForm, ProjectForm
import datetime
from calendar import monthrange
from django.http import HttpResponse, HttpResponseRedirect



def home(request):
    if request.user.is_authenticated:
        return redirect('main')
    return render(request, "home.html")


@login_required
def main(request):
    profile, created = Profile.objects.get_or_create(user=request.user)
    
    #input for creating a project
    form = ProjectForm(request.POST or None)
    if request.method == 'POST':
        if form.is_valid():
            newProject = form.save()
            newProject.save()  
            return HttpResponseRedirect(reverse("hello:home"))  # Redirect to the list view after saving
  
    projects = Project.objects.all()

    return render(request, "main.html", {'user':request.user, 'profile' : profile, 'form': form, 'projects': projects})

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
   

def calendar_view(request):
    today = datetime.date.today()
    month = today.month
    year = today.year
    start_day, num_days = monthrange(year, month)
    calendar_data = []
    for day in range(1, num_days + 1):
            day_info = {'day': day, 'events': []}
            calendar_data.append(day_info)
    context = {
        'today': today,
        'year': year,
        'calendar_data': calendar_data,
    }
    
    return render(request, 'calendar.html', context)



def logout_view(request):
    logout(request)
    return redirect("home")