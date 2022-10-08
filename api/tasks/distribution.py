from api.work_distribution.models import WorkDistributionToEvaluate
from triproverochki.celery import app


@app.task
def distribution_make_necessary_for_week_participants():
    print('Starting distribution...')  # TODO: to logger
    WorkDistributionToEvaluate.make_necessary_for_week_participants()
    print('Distribution finished.')  # TODO: to logger
    # TODO: send to admins distribution results
