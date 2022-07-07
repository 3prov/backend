from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from django.core.validators import MaxValueValidator, MinValueValidator
from django.conf import settings

# from api.rus.models import Essay
# from api.work_distribution.models import WorkDistributionToEvaluate


class Configuration(models.Model):
    """Модель с единственной строкой"""
    class Meta:
        abstract = True
        verbose_name = 'Настройка'
        verbose_name_plural = 'Настройки'

    @classmethod
    def object(cls):
        return cls._default_manager.all().first()

    def save(self, *args, **kwargs):
        self.pk = self.id = 1
        return super().save(*args, **kwargs)


class Stage(Configuration):
    class Meta:
        verbose_name = 'Этап'
        verbose_name_plural = verbose_name

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


class WeekID(models.Model):
    class Meta:
        verbose_name = 'Номер недели'
        verbose_name_plural = verbose_name

    study_year_from = models.PositiveIntegerField(
        validators=[MinValueValidator(1970), MaxValueValidator(2999)],
        default=int(settings.STUDY_YEAR.split('-')[0]),
        verbose_name='Начало учебного года'
    )
    study_year_to = models.PositiveIntegerField(
        validators=[MinValueValidator(1970), MaxValueValidator(2999)],
        default=int(settings.STUDY_YEAR.split('-')[1]),
        verbose_name='Конец учебного года'
    )
    week_number = models.PositiveIntegerField(
        validators=[MinValueValidator(0), MaxValueValidator(250)],
        default=0,
        verbose_name='Номер учебной недели',
    )
    created_at = models.DateTimeField(default=timezone.now, verbose_name='Дата создания', editable=False)

    def __str__(self):
        """
        Пример формата: 2022-2023_07, где 2022 - это начало учебного года, 2023 - конец, 07 - номер недели.
        """
        return f"{self.study_year_from}-{self.study_year_to}_{self.week_number:02d}"

    @staticmethod
    def get_current():
        return WeekID.objects.order_by('-created_at').first()

    @staticmethod
    def increment_week_number():
        return WeekID.objects.create(week_number=WeekID.get_current().week_number+1)
