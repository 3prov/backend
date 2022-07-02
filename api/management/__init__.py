def init_stage():
    from .models import Stage
    from django.db import utils
    try:
        if not Stage.objects.all().exists():
            Stage.objects.create()
            print('"Stage" initialized successfully')  # TODO: to logger
    except utils.OperationalError as e:
        print('EXCEPTION OperationalError:', e)  # TODO: to logger


init_stage()
