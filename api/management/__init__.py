def init_stage():
    from django.db import utils
    from .models import Stage, WeekID

    try:
        if not Stage.objects.all().exists():
            Stage.objects.create()
            print('"Stage" initialized successfully')  # TODO: to logger
    except utils.OperationalError as e:
        print('EXCEPTION OperationalError:', e)  # TODO: to logger

    try:
        if not WeekID.objects.all().exists():
            WeekID.objects.create()
            print('"WeekID" initialized successfully')  # TODO: to logger
    except utils.OperationalError as e:
        print('EXCEPTION OperationalError:', e)  # TODO: to logger


init_stage()
