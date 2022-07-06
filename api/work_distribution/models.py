from django.db import models

from .exceptions import UsersCountLessThenFour, WorkDistributionAlreadyExists
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

    @staticmethod
    def _check_before_make():
        if Essay.objects.filter(task__week_id=WeekID.get_current()).count() < 4:
            raise UsersCountLessThenFour('Невозможно сделать распределение работ. Число пользователей меньше четырех.')
        if WorkDistributionToEvaluate.objects.filter(week_id=WeekID.get_current()).count() > 0:
            raise WorkDistributionAlreadyExists('Распределение для текущей недели уже сделано.')

    @staticmethod
    def make_necessary_for_week_participants():
        WorkDistributionToEvaluate._check_before_make()
        # TODO: Hungarian algo here
        work_authors = set()
        for essay in Essay.objects.filter(task__week_id=WeekID.get_current()):
            work_authors.add(essay.author)

        # WorkDistributionToEvaluate.objects.create(week_id=WeekID.get_current(), evaluator=..., work=...)

    @staticmethod
    def make_optionally_for_volunteer(volunteer: User):
        pass

        work_authors = set()
        for essay in Essay.objects.filter(task__week_id=WeekID.get_current()):
            work_authors.add(essay.author)
