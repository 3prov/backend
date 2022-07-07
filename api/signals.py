from django.conf import settings
from django.db import transaction
from django.dispatch import receiver
from django.db.models import signals
from django.db.utils import IntegrityError

from api.models import FormURL
from api.rus.models import Text, Essay
from api.management.models import WeekID, Stage
from api.work_distribution.models import WorkDistributionToEvaluate


@receiver(signals.post_save, sender=Text)
def post_save_text(sender, instance, created, **kwargs):
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


@receiver(signals.post_save, sender=FormURL)
def post_save_form_url(sender, instance, created, **kwargs):
    if created:
        try:
            instance.url = instance._hash_string(settings.STRING_HASH_TEMPLATE.format(
                user_id=instance.user.id,
                week_id=WeekID.get_current().id,
                hash_type='essay',
                django_secret_key=settings.SECRET_KEY
            ))
            instance.week_id = WeekID.get_current()
            instance.save()  # TODO: fix transaction!
        except IntegrityError:
            instance.delete()


@receiver(signals.post_save, sender=Stage)
def post_save_stage(sender, instance, created, **kwargs):
    if instance.stage == Stage.StagesEnum.CHECK_ACCEPTING:
        if Essay.objects.filter(task__week_id=WeekID.get_current()).count() > 0:
            print('Starting distribution...')
            WorkDistributionToEvaluate.make_necessary_for_week_participants()
        else:
            print('No need for distribution.')
