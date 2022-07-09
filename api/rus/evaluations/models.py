import uuid

from django.conf import settings
from django.core.validators import MaxValueValidator, MaxLengthValidator, MinValueValidator
from django.utils.translation import gettext_lazy as _

from api.models import Evaluation, Criteria, User
from django.db import models, transaction

from api.rus.models import Essay


class EssayCriteria(Criteria):
    class Meta:
        verbose_name = 'Критерий оценивая сочинения'
        verbose_name_plural = 'Критерии оценивания сочинения'

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

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
        User.increase_rating(self.evaluator, settings.RATINGS_CONFIGURATION['increase_check_pass'])
        return super(EssayEvaluation, self).save(force_insert, force_update, using, update_fields)


for section in settings.ESSAY_EVALUATION_TABLE.keys():
    for criteria in settings.ESSAY_EVALUATION_TABLE[section].items():
        EssayCriteria.add_to_class(
            name=criteria[0],
            value=models.PositiveIntegerField(
                validators=[MinValueValidator(0), MaxValueValidator(criteria[1]['max_ball'])],
                verbose_name=criteria[1]['name']
            )
        )


class EssaySentenceReview(models.Model):
    class Meta:
        verbose_name = 'Предложение сочинения'
        verbose_name_plural = 'Предложения сочинения'

    class MistakesEnum(models.TextChoices):
        K7 = 'K07', _('Орфографическая (К7)')
        K8 = 'K08', _('Пунктуационная (К8)')
        K9 = 'K09', _('Грамматическая (К9)')
        K10 = 'K10', _('Речевая (К10)')
        K11 = 'K11', _('Этическая (К11)')
        K12 = 'K12', _('Фактическая (К12)')

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    essay = models.ForeignKey(to=Essay, on_delete=models.CASCADE, verbose_name='Сочинение')
    evaluator = models.ForeignKey(to=User, on_delete=models.CASCADE, verbose_name='Проверяющий')

    sentence_number = models.PositiveIntegerField(
        verbose_name='Номер предложения сочинения',
        validators=[MinValueValidator(1, 'Номер предложения должен быть положительным числом.')]
    )
    evaluator_comment = models.CharField(
        max_length=1000,
        validators=[MaxLengthValidator(1000, 'Комментарий не может быть длиннее 1000 символов.')],
        verbose_name='Комментарий проверяющего'
    )
    mistake_type = models.CharField(
        max_length=3,
        choices=MistakesEnum.choices,
        verbose_name='Тип ошибки'
    )
