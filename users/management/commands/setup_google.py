from allauth.socialaccount.models import SocialApp
from django.contrib.sites.models import Site
import os
from dotenv import load_dotenv
from django.core.management.base import BaseCommand

load_dotenv()


class Command(BaseCommand):
    help = "Create a SocialApp for Google"

    def handle(self, *args, **kwargs):
        site = Site.objects.get_current()

        app, created = SocialApp.objects.get_or_create(
            provider="google",
            name="Google App",
            defaults={
                "client_id": os.getenv("GOOGLE_CLIENT_ID"),
                "secret": os.getenv("GOOGLE_CLIENT_SECRET"),
            },
        )

        if created:
            app.sites.add(site)
            self.stdout.write(self.style.SUCCESS(
                "Google SocialApp created successfully!"))
        else:
            self.stdout.write(self.style.WARNING(
                "Google SocialApp already exists."))
