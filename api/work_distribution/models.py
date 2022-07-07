from django.db import models

from .algorithm.HungarianCPPHandler import HungarianCPPAlgorithm
from .algorithm.SortByRating import SortByRatingAlgorithm
from .algorithm.structures import ResultPair
from .exceptions import UsersCountLessThenFour, WorkDistributionAlreadyExists
from ..models import WeekID, User
from ..rus.evaluations.models import EssayEvaluation
from ..rus.models import Essay


class WorkDistributionToEvaluate(models.Model):
    class Meta:
        verbose_name = 'Распределение работ'
        verbose_name_plural = 'Распределения работ'

    week_id = models.ForeignKey(
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
    is_required = models.BooleanField(verbose_name='Является ли обязательной проверкой')

    @staticmethod
    def _check_before_make():
        if Essay.objects.filter(task__week_id=WeekID.get_current()).count() < 4:
            raise UsersCountLessThenFour('Невозможно сделать распределение работ. Число пользователей меньше четырех.')
        if WorkDistributionToEvaluate.objects.filter(week_id=WeekID.get_current()).count() > 0:
            raise WorkDistributionAlreadyExists('Распределение для текущей недели уже сделано.')

    @staticmethod
    def _save_pairs_from_algos_results(
            algo_result: list[ResultPair],
            current_week: WeekID,
            need_first_three_set_required: bool = True
    ):
        for pair in algo_result:
            _is_evaluator_have_three_required = WorkDistributionToEvaluate.objects.filter(
                week_id=current_week,
                evaluator=pair.evaluator,
                is_required=True
            ).count() >= 3
            WorkDistributionToEvaluate.objects.create(
                week_id=current_week,
                evaluator=pair.evaluator,
                work=Essay.objects.filter(author=pair.work_author, task__week_id=current_week).first(),
                is_required=True if need_first_three_set_required and not _is_evaluator_have_three_required else False
            )

    @staticmethod
    def make_necessary_for_week_participants():
        WorkDistributionToEvaluate._check_before_make()
        work_authors = set()
        current_week = WeekID.get_current()
        for work in Essay.objects.filter(task__week_id=current_week):
            work_authors.add(work.author)

        pairs = HungarianCPPAlgorithm().make_necessary_distribution_for_week_participants(
            participants=list(work_authors)
        )
        WorkDistributionToEvaluate._save_pairs_from_algos_results(
            pairs,
            current_week,
            need_first_three_set_required=True
        )

    @staticmethod
    def make_optionally_for_volunteer(volunteer: User):
        work_authors = set()
        current_week = WeekID.get_current()
        week_works = Essay.objects.filter(task__week_id=current_week)
        for work in week_works:
            work_authors.add(work.author)

        pairs = SortByRatingAlgorithm.make_optionally_distribution_for_volunteer(
            volunteer=volunteer,
            participants=list(work_authors),
            existing_evaluations_of_works=EssayEvaluation.objects.filter(work__task__week_id=current_week)
        )
        WorkDistributionToEvaluate._save_pairs_from_algos_results(
            pairs,
            current_week,
            need_first_three_set_required=False
        )

