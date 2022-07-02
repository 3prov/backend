from .models import Stage


def init_stage():
    if not Stage.objects.all().exists():
        Stage.objects.create()


init_stage()
