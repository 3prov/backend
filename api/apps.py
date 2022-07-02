from django.apps import AppConfig


class ApiConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'api'

    def ready(self):
        from django.conf import settings
        from .models import User
        from django.db import utils

        try:
            if settings.DEBUG and not User.objects.filter(username='admin').exists():
                User.objects.create_superuser(username='admin', password='admin')
                print('Superuser "admin" created successfully')  # TODO: to logger
        except utils.OperationalError as e:
            print('EXCEPTION OperationalError:', e)  # TODO: to logger
