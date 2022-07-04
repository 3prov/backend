import uuid

from django.db import models, transaction
from api.models import Work, Task
from api.management.models import WeekID


class Text(Task):
    class Meta:
        verbose_name = 'Текст'
        verbose_name_plural = 'Тексты'

    body = models.TextField(verbose_name='Поле для текста')
    author = models.CharField(max_length=75, verbose_name='Автор текста')
    author_description = models.TextField(verbose_name='Описание автора текста')

    @staticmethod
    def get_current():
        return Text.objects.order_by('-created_at').first()

    @transaction.atomic
    def save(self, *args, **kwargs):
        return super(Text, self).save(*args, **kwargs)


class Essay(Work):
    class Meta:
        verbose_name = 'Сочинение'
        verbose_name_plural = 'Сочинения'

    task = models.ForeignKey(
        to=Text,
        on_delete=models.CASCADE,
        verbose_name='Текст, по которому написано сочинение',
        related_name='essays'
    )
    body = models.TextField(verbose_name='Поле для сочинения')


class TextKey(models.Model):
    class Meta:
        verbose_name = 'Ключ к тексту'
        verbose_name_plural = 'Ключи к тексту'

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    range_of_problems = models.TextField(verbose_name='Примерный круг проблем')
    authors_position = models.TextField(verbose_name='Авторская позиция')
    text = models.ForeignKey(to=Text, on_delete=models.CASCADE, verbose_name='Текст', related_name='keys')

