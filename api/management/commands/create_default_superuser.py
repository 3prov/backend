from django.db import utils
from django.core.management import BaseCommand

from api.models import User
from triproverochki import settings


class Command(BaseCommand):
    """Django command to create default (admin-admin) superuser in DEBUG mode."""

    def handle(self, *args, **options):
        try:
            if settings.DEBUG and not User.objects.filter(username='admin').exists():
                User.objects.create_superuser(username='admin', password='admin')
                self.stdout.write(
                    self.style.SUCCESS('Superuser `admin` created successfully!')
                )
        except utils.OperationalError as e:
            self.stdout.write(
                self.style.ERROR('Exception: %s' % e)
            )

