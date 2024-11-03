import os
from django.shortcuts import render, redirect,  get_object_or_404, reverse
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required, user_passes_test
from .models import Profile, Project, Event, RSVP
from .forms import ProfileUpdateForm, ProjectForm, FileForm, EventForm
import datetime
import calendar
from calendar import monthrange
from calendar import monthrange
from django.http import HttpResponse, HttpResponseRedirect


def is_admin(user):
    return user.is_authenticated and hasattr(user, 'profile') and user.profile.is_pma_admin


def home(request):
    if request.user.is_authenticated:
        return redirect('users:main')
    return render(request, "home.html")


@login_required
def main(request):
    profile, created = Profile.objects.get_or_create(user=request.user)

    # input for creating a project
    form = ProjectForm(request.POST or None)
    if request.method == 'POST':
        form = ProjectForm(request.POST)
        if form.is_valid():
            project = form.save(commit=False)
            project.created_by = request.user
            project.save()
            project.members.add(request.user)
            project.save()
            return redirect('users:main')
    else:
        form = ProjectForm()

    user_projects = profile.user.created_projects.all()
    other_projects = Project.objects.exclude(members=profile.user)
    return render(request, "main.html", {'user': request.user, 'profile': profile, 'form': form, 'otherProjects': other_projects, 'userProjects': user_projects})


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
            return redirect('users:main')
    else:
        form = ProfileUpdateForm(instance=profile)
    return render(request, 'update_profile.html', {'form': form, 'first_name': request.user.first_name})


def calendar_view(request):
    today = datetime.date.today()
    month = today.month
    year = today.year
    start_day, num_days = monthrange(year, month)
    blank_days = [None] * start_day

    # Get all events for the current month
    events = Event.objects.filter(date__year=year, date__month=month)
    user_rsvps = RSVP.objects.filter(user=request.user).values_list(
        'event_id', flat=True) if request.user.is_authenticated else []

    # Initialize calendar data for each day of the month
    calendar_data = []
    for day in range(1, num_days + 1):
        day_date = datetime.date(year, month, day)
        day_events = events.filter(date=day_date)
        calendar_data.append({'day': day, 'events': day_events})

    context = {
        'today': today,
        'year': year,
        'calendar_data': calendar_data,
        'blank_days': blank_days,
        'user_rsvps': user_rsvps,
    }
    return render(request, 'calendar.html', context)


def projectView(request, id):
    project = get_object_or_404(Project, id=id)
    return render(request, 'project.html', {'description': project.description, 'project': project})


@login_required
def filesView(request, id):
    project = get_object_or_404(Project, id=id)
    
    # Add authorization check
    if not request.user.is_authenticated or request.user not in project.members.all():
        return HttpResponse(status=403)
        
    form = FileForm(request.POST or None, request.FILES or None)

    if request.method == 'POST' and form.is_valid():
        newFile = form.save(commit=False)
        newFile.project = project
        newFile.file_name = request.FILES['file'].name
        newFile.file_size = request.FILES['file'].size
        newFile.file_type = os.path.splitext(request.FILES['file'].name)[1][1:]  # Get extension without dot
        newFile.title = form.cleaned_data.get('title')
        newFile.description = form.cleaned_data.get('description')
        newFile.keywords = form.cleaned_data.get('keywords')
        newFile.save()
        return redirect('users:project-files', id=project.id)

    keyword = request.GET.get('keyword')
    if keyword:
        files = project.files.filter(keywords__icontains=keyword)
    else:
        files = project.files.all()

    context = {
        'project': project,
        'files': files,
        'form': form
    }
    return render(request, 'files.html', context)


def membersView(request, id):
    project = get_object_or_404(Project, id=id)
    members = project.members.all()
    member_profiles = [member.profile for member in members]
    is_owner = project.created_by == request.user
    # owner = project.created_by.first_name

    return render(request, 'members.html', {'project': project,  'member_profiles': member_profiles, 'is_owner': is_owner})


@login_required
def rsvp_event(request, event_id):
    if request.user.profile.is_pma_admin:
        return redirect('users:calendar')  # or show a message
    event = get_object_or_404(Event, id=event_id)
    rsvp, created = RSVP.objects.get_or_create(event=event, user=request.user)
    if not created:
        rsvp.delete()
    return redirect('users:calendar')


@user_passes_test(is_admin)
def create_event(request):
    if request.method == 'POST':
        form = EventForm(request.POST)
        if form.is_valid():
            event = form.save(commit=False)
            event.created_by = request.user
            event.save()
            return redirect('users:calendar')
    else:
        form = EventForm()
    return render(request, 'create_event.html', {'form': form})


@user_passes_test(is_admin)
def delete_event(request, event_id):
    event = get_object_or_404(Event, id=event_id, created_by=request.user)
    event.delete()
    return redirect('users:calendar')


def logout_view(request):
    logout(request)
    return redirect("home")
