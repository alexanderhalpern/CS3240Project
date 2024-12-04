from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
from django.utils.text import slugify
from django.db.models.signals import pre_save

import os


class CIO(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True, blank=True)
    description = models.TextField()
    image = models.ImageField(upload_to='cios/', blank = True, null = True)
    admins = models.ManyToManyField(
        User, related_name='admin_cios', blank=True)
    members = models.ManyToManyField(
        User, related_name='member_cios', blank=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('users:cio-dashboard', kwargs={'slug': self.slug})


def generate_slug(sender, instance, **kwargs):
    if not instance.slug:
        instance.slug = slugify(instance.name)


pre_save.connect(generate_slug, sender=CIO)


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
    cio = models.ForeignKey(CIO, on_delete=models.CASCADE,
                            related_name='projects')  # New field

    def __str__(self):
        return self.name

# class File(models.Model):
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
    title = models.CharField(max_length=255, blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    keywords = models.TextField(blank=True, null=True)

    def save(self, *args, **kwargs):
        if self.file:
            self.file_name = self.file.name
            self.file_size = self.file.size
            self.file_type = os.path.splitext(self.file.name)[1][1:]

        super().save(*args, **kwargs)

    def __str__(self):
        return self.file_name
    

class AdminFile(models.Model):
    file = models.FileField(upload_to='admin_files/')
    uploaded_by = models.ForeignKey(User, on_delete=models.CASCADE)
    club = models.ForeignKey(CIO, on_delete=models.CASCADE)
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.file.name


class Event(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    date = models.DateField()
    time = models.TimeField()
    created_by = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='events_created')
    cio = models.ForeignKey(CIO, on_delete=models.CASCADE,
                            related_name='events')  # New field

    def __str__(self):
        return f"{self.name} on {self.date}"


class RSVP(models.Model):
    event = models.ForeignKey(
        Event, related_name='rsvps', on_delete=models.CASCADE)
    user = models.ForeignKey(User, related_name='rsvps',
                             on_delete=models.CASCADE)
    status = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.user.username} RSVP for {self.event.name}"

class Notification(models.Model):
    #model for notification
    #notification will be assigned to a specific user, each notification will have a time of creation, content
    #and a state of read or unread
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="notifications")
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)

    def __str__(self):
        return f"Notification for {self.user.username}: {self.content[:30]}"
    
class Announcement(models.Model):
    cio = models.ForeignKey(CIO, on_delete=models.CASCADE, related_name='announcements')
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Announcement by {self.created_by.username} in {self.cio.name}"
    
class SupportMessage(models.Model):
    #model for support message
    #support message will be associated with only one user
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="support_messages")
    message = models.TextField()
    submitted_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Message from {self.user.username} at {self.submitted_at}"