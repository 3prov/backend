from __future__ import annotations
import uuid

from django.conf import settings
from django.db import models, transaction
from django.db.models import QuerySet

from api.models import Work, Task, User
from api.services import filter_objects


class Text(Task):
    class Meta:
        verbose_name = 'Текст'
        verbose_name_plural = 'Тексты'

    body = models.TextField(verbose_name='Поле для текста')
    author = models.CharField(max_length=75, verbose_name='Автор текста')
    author_description = models.TextField(verbose_name='Описание автора текста')

    @staticmethod
    def get_current() -> Text:
        return Text.objects.order_by('-created_at').first()


class Essay(Work):
    class Meta:
        verbose_name = 'Сочинение'
        verbose_name_plural = 'Сочинения'

    task = models.ForeignKey(
        to=Text,
        on_delete=models.CASCADE,
        verbose_name='Текст, по которому написано сочинение',
        related_name='essays',
    )
    body = models.TextField(verbose_name='Поле для сочинения')

    @transaction.atomic
    def save(
        self, force_insert=False, force_update=False, using=None, update_fields=None
    ):
        User.increase_rating(
            self.author, settings.RATINGS_CONFIGURATION['increase_essay_pass']
        )
        return super(Essay, self).save(force_insert, force_update, using, update_fields)

    @property
    def chars_count(self) -> int:
        return len(self.body)

    @classmethod
    def filter_by_current_task(cls) -> QuerySet:
        return filter_objects(cls.objects, task=Text.get_current())


class TextKey(models.Model):
    class Meta:
        verbose_name = 'Ключ к тексту'
        verbose_name_plural = 'Ключи к тексту'

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    range_of_problems = models.TextField(verbose_name='Примерный круг проблем')
    authors_position = models.TextField(verbose_name='Авторская позиция')
    text = models.ForeignKey(
        to=Text, on_delete=models.CASCADE, verbose_name='Текст', related_name='keys'
    )
