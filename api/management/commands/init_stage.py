from django.db import utils
from django.core.management import BaseCommand

from api.control.models import Stage, WeekID


class Command(BaseCommand):
    """Django command to initialize Stage model."""

    def handle(self, *args, **options):
        try:
            if not Stage.objects.all().exists():
                Stage.objects.create()
                self.style.SUCCESS('`Stage` initialized successfully')
        except utils.OperationalError as e:
            self.stdout.write(self.style.ERROR('Exception: %s' % e))

        try:
            if not WeekID.objects.all().exists():
                WeekID.objects.create()
                self.style.SUCCESS('`WeekID` initialized successfully')
        except utils.OperationalError as e:
            self.stdout.write(self.style.ERROR('Exception: %s' % e))
