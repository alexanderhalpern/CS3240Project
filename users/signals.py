from allauth.account.signals import user_logged_in
from django.dispatch import receiver
from .models import Profile

@receiver(user_logged_in)
def assign_role_on_login(sender, request, user, **args):
    admin_emails = ['karukavina@gmail.com'] #admin emails

    profile, created = Profile.objects.get_or_create(user=user)

    if user.email in admin_emails:
        profile.is_pma_admin = True
    else:
        profile.is_pma_admin = False

    profile.save()


