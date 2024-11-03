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
        model = File
        fields = ['file', 'title', 'description', 'keywords']
        # Make title required
        required = ['file', 'title']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['title'].required = True
        self.fields['description'].required = False
        self.fields['keywords'].required = False

class EventForm(forms.ModelForm):
    class Meta:
        model = Event
        fields = ['name', 'description', 'date', 'time']
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'time': forms.TimeInput(attrs={'type': 'time', 'class': 'form-control'}),
        }

class RSVPForm(forms.ModelForm):
    class Meta:
        model = RSVP
        fields = []