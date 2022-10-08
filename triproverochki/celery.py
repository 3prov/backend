import os

from celery import Celery
from celery.schedules import crontab


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'triproverochki.settings')

app = Celery('triproverochki')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks(['api.tasks', 'api.tasks.beats.switch_stage'])


# celery beat tasks
app.conf.beat_schedule = {
    'switch_stage_to_S1': {  # At 00:00 on Monday to NO_TASK
        'task': 'api.tasks_beat.set_stage',
        'description': 'Изменяет этап на NO_TASK',
        'schedule': crontab(minute=0, hour=0, day_of_week=1),
        'args': ('S1',),
    },
    'switch_stage_to_S2': {  # At 09:00 on Monday to WORK_ACCEPTING
        'task': 'api.tasks_beat.set_stage',
        'description': 'Изменяет этап на WORK_ACCEPTING',
        'schedule': crontab(minute=0, hour=9, day_of_week=1),
        'args': ('S2',),
    },
    'switch_stage_to_S3': {  # At 00:00 on Thursday to EVALUATION_ACCEPTING
        'task': 'api.tasks_beat.set_stage',
        'description': 'Изменяет этап на EVALUATION_ACCEPTING',
        'schedule': crontab(minute=0, hour=0, day_of_week=4),
        'args': ('S3',),
    },
    'switch_stage_to_S4': {  # At 00:00 on Sunday to CLOSED_ACCEPT
        'task': 'api.tasks_beat.set_stage',
        'description': 'Изменяет этап на CLOSED_ACCEPT',
        'schedule': crontab(minute=0, hour=0, day_of_week=0),
        'args': ('S4',),
    },
}
