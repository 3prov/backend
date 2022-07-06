from django.conf import settings
from django.core.validators import MaxValueValidator

from api.models import Evaluation, Criteria, User
from django.db import models, transaction

from api.rus.models import Essay


class EssayCriteria(Criteria):
    class Meta:
        verbose_name = 'Критерий оценивая сочинения'
        verbose_name_plural = 'Критерии оценивания сочинения'

    @property
    def score(self) -> int:
        return 0  # TODO: sum it


class EssayEvaluation(Evaluation):
    class Meta:
        verbose_name = 'Проверка сочинений'
        verbose_name_plural = 'Проверки сочинений'

    work = models.ForeignKey(to=Essay, on_delete=models.CASCADE, verbose_name='Работа', related_name='evaluations')

    criteria = models.OneToOneField(
        to=EssayCriteria,
        on_delete=models.CASCADE,
        verbose_name='Критерии',
        related_name='evaluation',
    )

    @transaction.atomic
    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
        User.increase_rating(self.checker, settings.RATINGS_CONFIGURATION['increase_check_pass'])
        return super(EssayEvaluation, self).save(force_insert, force_update, using, update_fields)


for section in settings.ESSAY_EVALUATION_TABLE.keys():
    for criteria in settings.ESSAY_EVALUATION_TABLE[section].items():
        EssayCriteria.add_to_class(
            name=criteria[0],
            value=models.PositiveIntegerField(
                validators=[MaxValueValidator(criteria[1]['max_ball'])],
                verbose_name=criteria[1]['name']
            )
        )
