from django.db import models

from .exceptions import UsersCountLessThenFour
from ..models import WeekID, User
from ..rus.models import Essay


class WorkDistributionToEvaluate(models.Model):
    class Meta:
        verbose_name = 'Распределение работ'
        verbose_name_plural = 'Распределения работ'

    week_id = models.OneToOneField(
        to=WeekID,
        on_delete=models.CASCADE,
        verbose_name='Идентификатор недели',
        related_name='work_distribution'
    )
    evaluator = models.ForeignKey(
        to=User,
        on_delete=models.CASCADE,
        verbose_name='Проверяющий',
        related_name='work_distributions'
    )
    work = models.ForeignKey(
        to=Essay,
        on_delete=models.CASCADE,
        verbose_name='Работа',
        related_name='work_distributions'
    )

    def _check_before_make(self):
        if Essay.objects.filter(task__week_id=self.week_id.get_current()).count() < 4:
            raise UsersCountLessThenFour('Невозможно сделать распределение работ. Число пользователей меньше четырех.')

    def make(self):
        self._check_before_make()
        # TODO: Hungarian algo here
