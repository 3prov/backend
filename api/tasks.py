from api.form_url.models import ResultsFormURL
from api.control.models import WeekID
from api.models import User
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


class SendTelegramMessage(CeleryTasks):
    @staticmethod
    @app.task(bind=True)
    def send_message_to_active_users(self, message: str):
        users = User.objects.filter(is_active=True)
        users_count = users.count()
        i = 1
        for user in users:
            user.send_telegram_message(message=message)
            self.update_state(
                state='PROGRESS', meta={'current': i, 'total': users_count}
            )
            i += 1
