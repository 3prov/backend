import uuid

from django.conf import settings
from django.core.validators import (
    MaxValueValidator,
    MaxLengthValidator,
    MinValueValidator,
)
from django.utils.translation import gettext_lazy as _

from api.models import Evaluation, Criteria, User, RateEvaluation
from django.db import models, transaction

from api.rus.models import Essay


class EssayCriteria(Criteria):
    class Meta:
        verbose_name = 'Критерий оценивая сочинения'
        verbose_name_plural = 'Критерии оценивания сочинения'

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    @property
    def score(self) -> int:
        score = 0
        for section in settings.ESSAY_EVALUATION_TABLE.keys():
            for criteria in settings.ESSAY_EVALUATION_TABLE[section].keys():
                score += self._meta.get_field(criteria).value_from_object(self)
        return score


class EssayEvaluation(Evaluation):
    class Meta:
        verbose_name = 'Проверка сочинений'
        verbose_name_plural = 'Проверки сочинений'

    work = models.ForeignKey(
        to=Essay,
        on_delete=models.CASCADE,
        verbose_name='Работа',
        related_name='evaluations',
    )
    criteria = models.OneToOneField(
        to=EssayCriteria,
        on_delete=models.CASCADE,
        verbose_name='Критерии',
        related_name='evaluation',
    )

    @transaction.atomic
    def save(
        self, force_insert=False, force_update=False, using=None, update_fields=None
    ):
        User.increase_rating(
            self.evaluator, settings.RATINGS_CONFIGURATION['increase_check_pass']
        )
        return super(EssayEvaluation, self).save(
            force_insert, force_update, using, update_fields
        )


for section in settings.ESSAY_EVALUATION_TABLE.keys():
    for criteria in settings.ESSAY_EVALUATION_TABLE[section].items():
        EssayCriteria.add_to_class(
            name=criteria[0],
            value=models.PositiveIntegerField(
                validators=[
                    MinValueValidator(0),
                    MaxValueValidator(criteria[1]['max_score']),
                ],
                verbose_name=criteria[1]['name'],
            ),
        )


class RateEssayEvaluation(RateEvaluation):
    class Meta:
        verbose_name = 'Рейтинг проверки сочинений'
        verbose_name_plural = 'Рейтинги проверок сочинений'

    evaluation_criteria = models.OneToOneField(
        to=EssayCriteria,
        on_delete=models.CASCADE,
        verbose_name='Проверка',
        related_name='rate',
    )


class EssaySelectionReview(models.Model):
    class Meta:
        verbose_name = 'Фрагмент сочинения'
        verbose_name_plural = 'Фрагменты сочинений'

    class MistakesEnum(models.TextChoices):
        K7 = 'K07', _('Орфографическая (К7)')
        K8 = 'K08', _('Пунктуационная (К8)')
        K9 = 'K09', _('Грамматическая (К9)')
        K10 = 'K10', _('Речевая (К10)')
        K11 = 'K11', _('Этическая (К11)')
        K12 = 'K12', _('Фактическая (К12)')

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    essay = models.ForeignKey(
        to=Essay, on_delete=models.CASCADE, verbose_name='Сочинение'
    )
    evaluator = models.ForeignKey(
        to=User, on_delete=models.CASCADE, verbose_name='Проверяющий'
    )

    start_selection_char_index = models.PositiveIntegerField(
        verbose_name='Индекс начального символа выделения',
        validators=[
            MinValueValidator(
                0,
                'Индекс начального символа выделения не может быть отрицательным числом.',
            )
        ],
    )
    selection_length = models.PositiveIntegerField(
        verbose_name='Длина выделения в символах',
        validators=[
            MinValueValidator(1, 'Длина выделения должна быть положительным числом.')
        ],
    )

    evaluator_comment = models.CharField(
        max_length=1000,
        validators=[
            MaxLengthValidator(1000, 'Комментарий не может быть длиннее 1000 символов.')
        ],
        verbose_name='Комментарий проверяющего',
    )
    mistake_type = models.CharField(
        max_length=3, choices=MistakesEnum.choices, verbose_name='Тип ошибки'
    )
