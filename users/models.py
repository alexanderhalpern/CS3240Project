from django.db import models
from django.contrib.auth.models import User


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField(blank=True, null=True)
    profile_picture = models.ImageField(upload_to='profile_pics/', blank=True, null=True)
    is_pma_admin = models.BooleanField(default=False)
   
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
