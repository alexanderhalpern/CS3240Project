import os
from django.shortcuts import render, redirect,  get_object_or_404, reverse
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required, user_passes_test
from .models import CIO, Announcement, Profile, Project, Event, RSVP
from .forms import ProfileUpdateForm, ProjectForm, FileForm, EventForm, CIOForm, SupportForm
import datetime
import calendar
from django.http import HttpResponse, HttpResponseForbidden, JsonResponse, HttpResponseNotAllowed
from django.contrib import messages
from django.contrib.auth.models import User
from .models import Notification, SupportMessage


def is_admin(user):
    return user.is_authenticated and hasattr(user, 'profile') and user.profile.is_pma_admin


# def home(request):
#     if request.user.is_authenticated:
#         return redirect('users:main')
#     return render(request, "home.html")


def home(request):
    if request.user.is_authenticated or request.session.get('is_guest', False):
        cios = CIO.objects.all().order_by('name')
        print(cios)
        slugs = [cio.slug for cio in cios]
        print(slugs)
        unread_count = Notification.objects.filter(user=request.user, is_read=False).count() #for mailbox button on dropdown
        return render(request, 'home.html', {'cios': cios, 'unread_count': unread_count})
    #return render(request, 'home.html')
    return render(request, 'user/login.html')

def continue_as_guest(request):
    request.session['is_guest'] = True
    return redirect('/')


@login_required
def cio_detail(request, slug):
    cio = get_object_or_404(CIO, slug=slug)
    announcements = cio.announcements.order_by('-created_at')
    user_projects = cio.projects.filter(members=request.user)
    other_projects = cio.projects.exclude(members=request.user)
    upcoming_events = cio.events.filter(
        date__gte=datetime.date.today()).order_by('date')[:5]

    is_admin = request.user in cio.admins.all()
    is_member = request.user in cio.members.all()

    context = {
        'cio': cio,
        'user_projects': user_projects,
        'other_projects': other_projects,
        'upcoming_events': upcoming_events,
        'is_admin': is_admin,
        'is_member': is_member,
        'admins': cio.admins.all(),
        'members': cio.members.all(),
        'announcements': announcements,
    }
    return render(request, 'cio/detail.html', context)


@login_required
def join_cio(request, slug):
    if request.method == 'POST':
        cio = get_object_or_404(CIO, slug=slug)
        if request.user not in cio.members.all():
            cio.members.add(request.user)
            messages.success(
                request, f'You have successfully joined {cio.name}!')
        return redirect('users:cio-dashboard', slug=slug)
    return redirect('users:cio-dashboard', slug=slug)


@login_required
def leave_cio(request, slug):
    if request.method == 'POST':
        cio = get_object_or_404(CIO, slug=slug)
        if request.user in cio.members.all():
            cio.members.remove(request.user)
            messages.success(
                request, f'You have left {cio.name}.')
        return redirect('users:cio-dashboard', slug=slug)
    return redirect('users:cio-dashboard', slug=slug)


@login_required
def add_cio(request):
    if request.method == 'POST':
        form = CIOForm(request.POST, request.FILES)
        if form.is_valid():
            cio = form.save(commit=False)
            cio.save()

            cio.admins.add(request.user)
            cio.members.add(request.user)

            messages.success(
                request, 'The student organization has been added successfully!')
            return redirect('users:cio-dashboard', slug=cio.slug)
    else:
        form = CIOForm()
    return render(request, 'cio/add.html', {'form': form})


@login_required
def add_cio_member(request, slug):
    cio = get_object_or_404(CIO, slug=slug)
    if request.user not in cio.admins.all():
        return HttpResponseForbidden("You are not allowed to add members.")
    if request.method == "POST":
        email = request.POST.get("email")
        user = get_object_or_404(User, email=email)
        if user not in cio.members.all():
            cio.members.add(user)
            messages.success(request, f"{email} has been added as a member.")
        else:
            messages.warning(request, f"{email} is already a member.")
        return redirect("users:cio-dashboard", slug=slug)


@login_required
def add_cio_admin(request, slug):
    cio = get_object_or_404(CIO, slug=slug)
    if request.user not in cio.admins.all():
        return HttpResponseForbidden("You are not allowed to add admins.")
    if request.method == "POST":
        email = request.POST.get("email")
        user = get_object_or_404(User, email=email)
        if user not in cio.admins.all():
            cio.admins.add(user)
            cio.members.add(user)
            messages.success(request, f"{email} has been added as an admin.")
        else:
            messages.warning(request, f"{email} is already an admin.")
        return redirect("users:cio-dashboard", slug=slug)


@login_required
def cio_members(request, slug):
    cio = get_object_or_404(CIO, slug=slug)
    is_admin = request.user in cio.admins.all()

    admins = cio.admins.all()
    members = cio.members.all()

    context = {
        "cio": cio,
        "admins": admins,
        "members": members,
        "is_admin": is_admin,
    }
    return render(request, "cio/members.html", context)

#@login_required
#def mailbox(request):
#    notifications = Notification.objects.filter(user=request.user).order_by('-created_at')
#    #note to self, need to fix URL
#    return render(request, 'cio/mailbox.html', {'notifications': notifications})

@login_required
def mailbox(request):
    unread_notifications = Notification.objects.filter(user=request.user, is_read=False).order_by('-created_at')
    read_notifications = Notification.objects.filter(user=request.user, is_read=True).order_by('-created_at')

    unread_count = unread_notifications.count()
    #testing correct URL hopefully
    return render(request, 'user/mailbox.html', {
        'unread_notifications': unread_notifications,
        'read_notifications': read_notifications,
        'unread_count': unread_count
    })

#mark as read feature hopefully
@login_required
def mark_as_read(request, notification_id):
    notification = get_object_or_404(Notification, id=notification_id, user=request.user)
    notification.is_read = True
    notification.save()
    return redirect('users:mailbox')

#mark all as read feature hopefully
@login_required
def mark_all_as_read(request):
    unread_notifications = Notification.objects.filter(user=request.user, is_read=False)
    unread_notifications.update(is_read=True)
    return redirect('users:mailbox')

def project_modal(request, project_id):
    project = Project.objects.get(id=project_id)
    context = {
        'project': project,
        'description': project.description,
    }
    return render(request, 'project/modal.html', context)

@login_required
def contact_support(request):
    if request.method == "POST":
        form = SupportForm(request.POST)
        if form.is_valid():
            support_message = form.save(commit=False)
            support_message.user = request.user
            support_message.save()
            messages.success(request, "Your message has been submitted. We'll get back to you soon!")
            return redirect('users:home')
    else:
        form = SupportForm()

    return render(request, 'user/contact-support.html', {'form': form})

@login_required
def support_messages(request):
    #note to self: MAKE SURE THAT THIS MOVES FROM USER TO ADMIN PERMISSION ASAP
    messages = SupportMessage.objects.all().order_by('-submitted_at')

    context = {
        'messages': messages
    }

    return render(request, 'user/support_messages.html', context)

@login_required
def cio_dashboard(request, slug):
    cio = get_object_or_404(CIO, slug=slug)
    profile, created = Profile.objects.get_or_create(user=request.user)

    if request.method == 'POST':
        form = ProjectForm(request.POST)
        if form.is_valid():
            project = form.save(commit=False)
            project.created_by = request.user
            project.cio = cio  # Set the CIO for the project
            project.save()
            project.members.add(request.user)
            project.save()
            return redirect('users:cio-dashboard', slug=slug)
    else:
        form = ProjectForm()

    user_projects = Project.objects.filter(
        cio=cio,
        members=request.user
    )
    other_projects = Project.objects.filter(
        cio=cio
    ).exclude(members=request.user)

    is_admin = request.user in cio.admins.all()

    context = {
        'user': request.user,
        'profile': profile,
        'form': form,
        'otherProjects': other_projects,
        'userProjects': user_projects,
        'cio': cio,
        'is_cio_admin': is_admin,
    }
    return render(request, "cio/dashboard.html", context)


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
            return redirect('users:home')
    else:
        form = ProfileUpdateForm(instance=profile)
    return render(request, 'user/update.html', {'form': form, 'first_name': request.user.first_name})


@login_required
def delete_project(request, project_id):
    if request.method == 'POST':
        project = get_object_or_404(Project, id=project_id)
        if request.user == project.created_by:
            project.delete()
            return redirect('users:cio-dashboard', slug=project.cio.slug)
    return redirect('users:cio-dashboard', slug=project.cio.slug)


def calendar_view(request, slug):
    cio = get_object_or_404(CIO, slug=slug)
    today = datetime.date.today()
    now = datetime.datetime.now().time()

    user_rsvps = RSVP.objects.filter(user=request.user, event__cio=cio).values_list(
        'event_id', flat=True
    ) if request.user.is_authenticated else []

    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        events = Event.objects.filter(date__gte=today, cio=cio)
        
        event_list = [
            {
                'id': event.id,
                'title': event.name,
                'start': f"{event.date}T{event.time}",
                'description': event.description,
                'rsvp': event.id in user_rsvps,
            }
            for event in events
        ]
        return JsonResponse(event_list, safe=False)

    upcoming_events = (
        Event.objects.filter(cio=cio, date__gte=today)
        .exclude(date=today, time__lt=now)
        .order_by('date', 'time')[:5]
    )

    context = {
        'today': today,
        'year': today.year,
        'cio': cio,
        'upcoming_events': upcoming_events,
        'user_rsvps': user_rsvps,
    }
    return render(request, 'cio/calendar.html', context)


def projectView(request, id):
    project = get_object_or_404(Project, id=id)
    return render(request, 'project/view.html', {'description': project.description, 'project': project})


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
        newFile.file_type = os.path.splitext(request.FILES['file'].name)[
            1][1:]  # Get extension without dot
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
        'form': form,
        'cio': project.cio,
    }
    return render(request, 'project/files.html', context)


@login_required
def membersView(request, id):
    project = get_object_or_404(Project, id=id)
    members = project.members.all()
    is_owner = project.created_by == request.user

    return render(request, 'project/members.html', {
        'project': project,
        'members': members,
        'cio': project.cio,
        'is_owner': is_owner
    })


@login_required
def rsvp_event(request, event_id):
    event = get_object_or_404(Event, id=event_id)

    if request.user not in event.cio.members.all():
        return HttpResponseForbidden("You must be a member of this organization to RSVP.")

    if request.method == 'POST':
        rsvp, created = RSVP.objects.get_or_create(event=event, user=request.user)
        if not created: 
            rsvp.delete()
            print(f"RSVP removed for user {request.user} and event {event.id}")
        else:
            print(f"RSVP added for user {request.user} and event {event.id}")

        return redirect('users:cio-calendar', slug=event.cio.slug)

    return HttpResponseForbidden("Invalid request method.")


@login_required
def view_rsvps(request, event_id):
    event = get_object_or_404(Event, id=event_id)

    rsvps = RSVP.objects.filter(event=event)
    context = {
        'event': event,
        'rsvps': rsvps,
    }
    return render(request, 'event/rsvp_list.html', context)


@login_required
def create_event(request, slug):
    cio = get_object_or_404(CIO, slug=slug)

    if request.user not in cio.admins.all():
        return HttpResponseForbidden("You do not have permission to create an event for this CIO.")

    if request.method == 'POST':
        form = EventForm(request.POST)
        if form.is_valid():
            event = form.save(commit=False)
            event.created_by = request.user
            event.cio = cio
            event.save()
            return redirect('users:cio-calendar', slug=cio.slug)
    else:
        form = EventForm()

    return render(request, 'event/create.html', {'form': form, 'cio': cio})



@login_required
def delete_event(request, event_id):
    event = get_object_or_404(Event, id=event_id)
    if request.method == 'POST':
        if request.user in event.cio.admins.all():
            event.delete()
            messages.success(request, 'Event deleted successfully.')
            return redirect('users:cio-calendar', slug=event.cio.slug)  # Corrected
        else:
            return HttpResponseForbidden('You are not authorized to delete this event.')
    return HttpResponseNotAllowed(['POST'])



def logout_view(request):
    logout(request)
    return redirect("home")


@login_required
def add_member(request, project_id):
    project = get_object_or_404(Project, id=project_id)
    if request.user != project.created_by:
        messages.error(request, "You don't have permission to add members.")
        return redirect('users:view-members', project_id)

    if request.method == 'POST':
        email = request.POST.get('email')
        try:
            user = User.objects.get(email=email)
            if user not in project.members.all():
                project.members.add(user)
                messages.success(
                    request, f'{user.email} has been added to the project.')
            else:
                messages.warning(request, f'{user.email} is already a member.')
        except User.DoesNotExist:
            messages.error(request, f'No user found with email {email}.')

    return redirect('users:view-members', project_id)


@login_required
def remove_member(request, project_id, user_id):
    project = get_object_or_404(Project, id=project_id)
    if request.user != project.created_by:
        messages.error(request, "You don't have permission to remove members.")
        return redirect('users:view-members', project_id)

    if request.method == 'POST':
        user_to_remove = get_object_or_404(User, id=user_id)
        if user_to_remove == project.created_by:
            messages.error(request, "Cannot remove the project owner.")
        else:
            project.members.remove(user_to_remove)
            messages.success(
                request, f'{user_to_remove.email} has been removed from the project.')

    return redirect('users:view-members', project_id)


@login_required
def join_project(request, project_id):
    project = get_object_or_404(Project, id=project_id)
    if request.method == 'POST':
        if request.user not in project.members.all():
            project.members.add(request.user)
            messages.success(request, 'You have joined the project.')
        else:
            messages.warning(
                request, 'You are already a member of this project.')

    return redirect('users:view-members', project_id)

@login_required
def create_announcement(request, slug):
    cio = get_object_or_404(CIO, slug=slug)
    if request.method == 'POST':
        if request.user in cio.admins.all():
            content = request.POST.get('content')
            if content:
                Announcement.objects.create(cio=cio, created_by=request.user, content=content)
            else:
                messages.error(request, "Announcement empty")
            return redirect('users:cio-dashboard', slug=slug)
        else:
            return HttpResponseForbidden('You are not admin')
    return HttpResponseNotAllowed(['POST'])