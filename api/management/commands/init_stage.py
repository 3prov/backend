from django.db import utils
from django.core.management import BaseCommand

from api.control.models import Stage, WeekID
from api.services import all_objects


class Command(BaseCommand):
    """Django command to initialize Stage model."""

    def handle(self, *args, **options):
        try:
            if not all_objects(Stage.objects).exists():
                Stage.objects.create()
                self.style.SUCCESS('`Stage` initialized successfully')
        except utils.OperationalError as e:
            self.stdout.write(self.style.ERROR('Exception: %s' % e))

        try:
            if not all_objects(WeekID.objects).exists():
                WeekID.objects.create()
                self.style.SUCCESS('`WeekID` initialized successfully')
        except utils.OperationalError as e:
            self.stdout.write(self.style.ERROR('Exception: %s' % e))
