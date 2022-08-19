from api.management.models import Stage
from api.tasks import CeleryTasks
from triproverochki.celery import app


class CeleryBeatTasks(CeleryTasks):
    pass


class SwitchStage(CeleryBeatTasks):
    @staticmethod
    @app.task
    def set_stage(stage_str: str):
        stage = Stage._dict_of_stages[stage_str]
        print(f'Starting switch stage to {stage}...')  # TODO: to logger
        Stage.switch_stage(stage)
        print('Switch stage finished.')  # TODO: to logger
