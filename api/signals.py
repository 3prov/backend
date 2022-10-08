from django.db import transaction
from django.dispatch import receiver
from django.db.models import signals
from django.db.utils import IntegrityError

from api.form_url.models import EssayFormURL, EvaluationFormURL, ResultsFormURL
from api.rus.models import Text, Essay
from api.control.models import WeekID, Stage
from api.services import filter_objects
from api.tasks import form_url, telegram_message, distribution
from api.work_distribution.models import WorkDistributionToEvaluate

import logging

logger = logging.getLogger('django')


@receiver(signals.post_save, sender=Text)
def post_save_text(sender, instance, created, **kwargs):
    """
    Увеличивает счётчик WeekID при создании модели Text.
    """
    if created:
        try:  # TODO: fix transaction!
            week_id = WeekID.increment_week_number()
        except IntegrityError:
            instance.delete()
            return
        try:
            instance.week_id = week_id
            instance.save()
        except IntegrityError:
            week_id.delete()


@receiver(signals.post_save, sender=EssayFormURL)
@receiver(signals.post_save, sender=ResultsFormURL)
def post_save_essay_form_url(sender, instance, created, **kwargs):
    """
    Привязывает week_id к модели FormURL после её создания.
    """
    if created:
        try:
            instance.week_id = WeekID.get_current()
            instance.save()  # TODO: fix transaction!
        except IntegrityError:
            instance.delete()


@receiver(signals.post_save, sender=Stage)
def post_save_stage(sender, instance, created, **kwargs):
    """
    Отслеживает, если этап становится 'S3', то делает распределение работ по участникам.
    Отслеживает, если этап становится 'S4', то создаёт ссылки на формы просмотра
    проверок.
    Также отправляет уведомления.
    """
    match instance.stage:
        case Stage.StagesEnum.WORK_ACCEPTING:
            task_message = telegram_message.send_work_accepting_stage_start
            task = None  # TODO: is it ok?

        case Stage.StagesEnum.EVALUATION_ACCEPTING:
            if (
                filter_objects(
                    Essay.objects, task__week_id=WeekID.get_current()
                ).count()
                > 0
            ):
                task_message = telegram_message.send_evaluation_accepting_stage_start
                task = distribution.distribution_make_necessary_for_week_participants
            else:
                logger.warning('No need for distribution.')
                return

        case Stage.StagesEnum.CLOSED_ACCEPT:
            task_message = telegram_message.send_closed_accept_stage
            task = form_url.create_result_form_urls_for_essay_authors
        case _:
            return

    with transaction.atomic():
        if task:
            return task.apply_async(link=task_message.si())  # TODO: check it!
        return task_message.delay()


@receiver(signals.post_save, sender=WorkDistributionToEvaluate)
def post_save_work_distribution_to_evaluate(sender, instance, created, **kwargs):
    """
    Создает ссылку EvaluationFormURL при сохранении распределения работ
    EvaluationFormURL.
    """
    if created:
        if instance.is_required:
            EvaluationFormURL.objects.create(  # TODO: make transaction
                evaluation_work=instance.work,
                user=instance.evaluator,
                week_id=instance.work.task.week_id,
            )
