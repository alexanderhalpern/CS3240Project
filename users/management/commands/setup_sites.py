from django.core.management.base import BaseCommand
from django.contrib.sites.models import Site
from django.db import IntegrityError


class Command(BaseCommand):
    help = 'Set up Site objects for local development and Heroku'

    def handle(self, *args, **options):
        self.setup_site(1, 'localhost:8000', 'Local Development')
        self.setup_site(2, 'cs3240-b0c65a32d363.herokuapp.com',
                        'Heroku Production')

    def setup_site(self, site_id, domain, name):
        try:
            site, created = Site.objects.update_or_create(
                id=site_id,
                defaults={'domain': domain, 'name': name}
            )
            if created:
                self.stdout.write(self.style.SUCCESS(
                    f'Created new site: {domain}'))
            else:
                self.stdout.write(self.style.SUCCESS(
                    f'Updated existing site: {domain}'))
        except IntegrityError:
            # If there's a conflict, delete the existing site and create a new one
            Site.objects.filter(domain=domain).delete()
            Site.objects.create(id=site_id, domain=domain, name=name)
            self.stdout.write(self.style.SUCCESS(
                f'Replaced existing site: {domain}'))
        except Exception as e:
            self.stdout.write(self.style.ERROR(
                f'Error setting up site {domain}: {str(e)}'))
