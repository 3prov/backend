from api.form_url.models import ResultsFormURL
from api.control.models import WeekID
from api.rus.models import Essay
from api.work_distribution.models import WorkDistributionToEvaluate
from triproverochki.celery import app


class CeleryTasks:
    pass


class DistributionTasks(CeleryTasks):
    @staticmethod
    @app.task
    def make_necessary_for_week_participants():
        print('Starting distribution...')  # TODO: to logger
        WorkDistributionToEvaluate.make_necessary_for_week_participants()
        print('Distribution finished.')  # TODO: to logger
        # TODO: send to admins distribution results


class FormURLTasks(CeleryTasks):
    @staticmethod
    @app.task
    def create_result_form_urls_for_essay_authors():
        current_week_id = WeekID.get_current()
        for essay in Essay.objects.filter(task__week_id=current_week_id).only('author'):
            ResultsFormURL.objects.create(user=essay.author, week_id=current_week_id)
