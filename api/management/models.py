from django.db import models
from django.utils.translation import gettext_lazy as _


class Stage(models.Model):
    """Модель с единственной строкой"""
    class Meta:
        verbose_name = 'Этап'
        verbose_name_plural = 'Этап'

    class StagesEnum(models.TextChoices):
        NO_TASK = 'S1', _('Нет задания')
        WORK_ACCEPTING = 'S2', _('Приём работ')
        CHECK_ACCEPTING = 'S3', _('Приём проверок')
        CLOSED_ACCEPT = 'S4', _('Нет приёма работ')

    _dict_of_stages = {
        'S1': StagesEnum.NO_TASK,
        'S2': StagesEnum.WORK_ACCEPTING,
        'S3': StagesEnum.CHECK_ACCEPTING,
        'S4': StagesEnum.CLOSED_ACCEPT
    }

    stage = models.CharField(
        max_length=2,
        choices=StagesEnum.choices,
        default=StagesEnum.NO_TASK,
        verbose_name='Этап'
    )

    @classmethod
    def object(cls):
        return cls._default_manager.all().first()  # Since only one item

    def save(self, *args, **kwargs):
        self.pk = self.id = 1
        return super().save(*args, **kwargs)

    @staticmethod
    def get_stage() -> StagesEnum:
        current_stage = Stage._dict_of_stages[Stage.object().stage]
        for possible_stage in Stage.StagesEnum.choices:
            if Stage._dict_of_stages[possible_stage[0]] == current_stage:
                return current_stage

    @staticmethod
    def switch_stage_to_next() -> StagesEnum:
        current_stage = Stage.object().stage
        iterator = iter(Stage.StagesEnum.choices * 2)
        while next(iterator)[0] != current_stage:
            continue
        next_stage = next(iterator)
        Stage(stage=next_stage[0]).save()
        return Stage.get_stage()


