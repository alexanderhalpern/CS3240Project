from django import forms
from .models import Profile, Project, File, Event, RSVP

class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = Profile 
        fields = ['bio','profile_picture']

class ProjectForm(forms.ModelForm):
    class Meta:
        model = Project
        fields = ['name'] 

class FileForm(forms.ModelForm):
    class Meta:
        model=File
        fields = ['file']

class EventForm(forms.ModelForm):
    class Meta:
        model = Event
        fields = ['name', 'description', 'date', 'time']

class RSVPForm(forms.ModelForm):
    class Meta:
        model = RSVP
        fields = []