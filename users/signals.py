from allauth.account.signals import user_logged_in
from django.dispatch import receiver
from .models import Profile
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
def notify_member_added(sender, instance, action, reverse, pk_set, **kwargs):
    if action == "post_add":
        for user_id in pk_set:
            user = User.objects.get(pk=user_id)
            Notification.objects.create(
                user=user,
                content=f"You have been added as a member to the club: {instance.name}"
            )