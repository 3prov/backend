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
    @app.task(bind=True)
    def create_result_form_urls_for_essay_authors(self):
        current_week_id = WeekID.get_current()
        form_urls_count = Essay.objects.filter(task__week_id=current_week_id).count()
        i = 1
        for essay in Essay.objects.filter(task__week_id=current_week_id).only('author'):
            ResultsFormURL.objects.create(user=essay.author, week_id=current_week_id)
            self.update_state(
                state='PROGRESS', meta={'current': i, 'total': form_urls_count}
            )
            i += 1
