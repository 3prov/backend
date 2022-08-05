from django.conf import settings
from django.db import transaction
from django.dispatch import receiver
from django.db.models import signals
from django.db.utils import IntegrityError

from api.form_url.models import EssayFormURL, EvaluationFormURL
from api.rus.models import Text, Essay
from api.management.models import WeekID, Stage
from api.work_distribution.models import WorkDistributionToEvaluate


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
def post_save_essay_form_url(sender, instance, created, **kwargs):
    """
    Привязывает url и week_id к модели FormURL после её создания.
    """
    if created:
        try:
            instance.url = instance._hash_string(
                settings.STRING_HASH_TEMPLATE.format(
                    user_id=instance.user.id,
                    week_id=WeekID.get_current().id,
                    hash_type='essay',
                    django_secret_key=settings.SECRET_KEY,
                )
            )
            instance.week_id = WeekID.get_current()
            instance.save()  # TODO: fix transaction!
        except IntegrityError:
            instance.delete()


@receiver(signals.post_save, sender=Stage)
def post_save_stage(sender, instance, created, **kwargs):
    """
    Отслеживает, если этап становится 'S3', то делает распределение работ по участникам.
    """
    if instance.stage == Stage.StagesEnum.EVALUATION_ACCEPTING:
        if Essay.objects.filter(task__week_id=WeekID.get_current()).count() > 0:
            print('Starting distribution...')  # TODO: to logger
            WorkDistributionToEvaluate.make_necessary_for_week_participants()
        else:
            print('No need for distribution.')  # TODO: to logger


@receiver(signals.post_save, sender=WorkDistributionToEvaluate)
def post_save_work_distribution_to_evaluate(sender, instance, created, **kwargs):
    """
    Создает ссылку EvaluationFormURL при сохранении распределения работ EvaluationFormURL.
    """
    if created:
        if instance.is_required:
            _user_evaluation_form_already_count = EvaluationFormURL.objects.filter(
                user=instance.evaluator, week_id=WeekID.get_current()
            ).count()
            EvaluationFormURL.objects.create(
                evaluation_work=instance.work,
                user=instance.evaluator,
                week_id=WeekID.get_current(),
                url=EvaluationFormURL._hash_string(
                    settings.STRING_HASH_TEMPLATE.format(
                        user_id=instance.evaluator.id,
                        week_id=WeekID.get_current().id,
                        hash_type=f'evaluation_{_user_evaluation_form_already_count}',
                        django_secret_key=settings.SECRET_KEY,
                    )
                ),
            )
