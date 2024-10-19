from django import forms
from .models import Profile, Project, File

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