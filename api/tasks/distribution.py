from api.work_distribution.models import WorkDistributionToEvaluate
from triproverochki.celery import app

import logging

logger = logging.getLogger('celery')


@app.task
def distribution_make_necessary_for_week_participants():
    logger.info('Starting distribution...')
    WorkDistributionToEvaluate.make_necessary_for_week_participants()
    logger.info('Distribution finished.')
    # TODO: send to admins distribution results
