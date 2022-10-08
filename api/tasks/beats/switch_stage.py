from api.control.models import Stage
from api.rus.models import Essay
from api.work_distribution.exceptions import UsersCountLessThenFour
from triproverochki.celery import app

import logging

logger = logging.getLogger('celery')


@app.task(bind=True, max_retries=20, default_retry_delay=30 * 60)
def set_stage(self, stage_str: str):
    stage = Stage._dict_of_stages[stage_str]
    if stage == Stage.StagesEnum.EVALUATION_ACCEPTING:
        if Essay.filter_by_current_task().count() < 4:
            logger.warning(
                f"Cannot set stage {Stage.StagesEnum.EVALUATION_ACCEPTING} "
                f"because of not enough essays."
            )
            raise self.retry(exc=UsersCountLessThenFour)
    logger.info(f'Starting switch stage to {stage}...')
    Stage.switch_stage(stage)
    logger.info('Switch stage finished.')
