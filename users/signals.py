from allauth.account.signals import user_logged_in
from django.dispatch import receiver
from .models import Announcement, Profile
from django.db.models.signals import m2m_changed, post_save
from django.contrib.auth.models import User
from .models import CIO, Event, Notification

@receiver(user_logged_in)
def assign_role_on_login(sender, request, user, **args):
    admin_emails = ['karukavina@gmail.com', 'lkrill14@gmail.com'] #admin emails

    profile, created = Profile.objects.get_or_create(user=user)

    if user.email in admin_emails:
        profile.is_pma_admin = True
    else:
        profile.is_pma_admin = False

    profile.save()

@receiver(m2m_changed, sender=CIO.members.through)
#signal for when a member is added to the club
def notify_member_added(sender, instance, action, reverse, pk_set, **kwargs):
    if action == "post_add":
        for user_id in pk_set:
            user = User.objects.get(pk=user_id)
            Notification.objects.create(
                user=user,
                content=f"You have been added as a member to the club: {instance.name}"
            )

@receiver(m2m_changed, sender=CIO.admins.through)
#signal for when a new club admin is added
def notify_admin_added(sender, instance, action, reverse, pk_set, **kwargs):
    if action == "post_add":
        for user_id in pk_set:
            user = User.objects.get(pk=user_id)
            Notification.objects.create(
                user=user,
                content=f"You have been made an admin of the club: {instance.name}"
            )

@receiver(post_save, sender=Event)
#signal for when a new event is created in a club that the user is a member of
def notify_event_created(sender, instance, created, **kwargs):
    if created:
        members = instance.cio.members.all()
        for member in members:
            Notification.objects.create(
                user=member,
                content=f"A new event has been scheduled in the club {instance.cio.name}: {instance.name} on {instance.date} at {instance.time}."
            )

@receiver(post_save, sender=Announcement)
def create_notifications_for_announcement(sender, instance, created, **kwargs):
    if created:
        members = instance.cio.members.all()
        for member in members:
            Notification.objects.create(
                user=member,
                content=f"New announcement in {instance.cio.name} by {instance.created_by.username}: {instance.content}"
            )