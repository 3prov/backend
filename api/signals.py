from django.db import transaction
from django.dispatch import receiver
from django.db.models import signals
from api.rus.models import Text
from api.management.models import WeekID


@receiver(signals.post_save, sender=Text)
def post_save_text(sender, instance, created, **kwargs):

    def _create_week_id_model_and_make_relationship(model_instance):
        week_id = WeekID.increment_week_number()
        model_instance.week_id = week_id
        model_instance.save()

    if created:
        transaction.on_commit(lambda: _create_week_id_model_and_make_relationship(instance))
