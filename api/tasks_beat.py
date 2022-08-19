from api.management.models import Stage
from api.rus.models import Essay
from api.tasks import CeleryTasks
from api.work_distribution.exceptions import UsersCountLessThenFour
from triproverochki.celery import app


class CeleryBeatTasks(CeleryTasks):
    pass


class SwitchStage(CeleryBeatTasks):
    @staticmethod
    @app.task(bind=True, max_retries=20, default_retry_delay=30 * 60)
    def set_stage(self, stage_str: str):
        stage = Stage._dict_of_stages[stage_str]
        if stage == Stage.StagesEnum.EVALUATION_ACCEPTING:
            if Essay.filter_by_current_task().count() < 4:
                print(
                    f"Cannot set stage {Stage.StagesEnum.EVALUATION_ACCEPTING} "
                    f"because of not enough essays."
                )  # TODO: to logger warning
                raise self.retry(exc=UsersCountLessThenFour)
        print(f'Starting switch stage to {stage}...')  # TODO: to logger
        Stage.switch_stage(stage)
        print('Switch stage finished.')  # TODO: to logger
