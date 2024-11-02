from django.db import models
from django.contrib.auth.models import User
import os

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField(blank=True, null=True)
    is_pma_admin = models.BooleanField(default=False)
    profile_picture = models.ImageField(
        upload_to='profile_pics/', blank=True, null=True)

    def __str__(self):
        return f"{self.user.username}'s profile"


class Project(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='created_projects')
    members = models.ManyToManyField(User, related_name='joined_projects')

    def __str__(self):
        return self.name


#class File(models.Model):
#    project = models.ForeignKey(
#        Project, related_name='files', on_delete=models.CASCADE)
#    file = models.FileField(upload_to='project_files/')
#    upload_date = models.DateTimeField(auto_now_add=True)
#
#    def __str__(self):
#        return self.file.name
    
class File(models.Model):
    project = models.ForeignKey(
        'Project', related_name='files', on_delete=models.CASCADE)
    file = models.FileField(upload_to='project_files/')
    upload_date = models.DateTimeField(auto_now_add=True)
    file_name = models.CharField(max_length=255, blank=True)
    file_size = models.PositiveIntegerField(blank=True, null=True)
    file_type = models.CharField(max_length=50, blank=True)

    def save(self, *args, **kwargs):
        if self.file:
            self.file_name = self.file.name
            self.file_size = self.file.size
            self.file_type = os.path.splitext(self.file.name)[1][1:]

        super().save(*args, **kwargs)

    def __str__(self):
        return self.file_name

class Event(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    date = models.DateField()
    time = models.TimeField()
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name ='events_created')
    def __str__(self):
        return f"{self.name} on {self.date}"
    
class RSVP(models.Model):
    event = models.ForeignKey(Event, related_name='rsvps', on_delete=models.CASCADE)
    user = models.ForeignKey(User, related_name='rsvps', on_delete=models.CASCADE)
    status = models.BooleanField(default=True)
    def __str__(self):
        return f"{self.user.username} RSVP for {self.event.name}"