from django.db import models
from ..models import Work, Task


class Text(Task):
    body = models.TextField(verbose_name='Поле для текста')
    author = models.CharField(max_length=75, verbose_name='Автор текста')
    author_description = models.TextField(verbose_name='Описание автора текста')


class Essay(Work):
    task = models.ForeignKey(
        to=Text,
        on_delete=models.CASCADE,
        verbose_name='Текст, по которому написано сочинение',
        related_name='essays'
    )
    body = models.TextField(verbose_name='Поле для сочинения')


class TextKeys(models.Model):
    range_of_problems = models.TextField(verbose_name='Примерный круг проблем')
    authors_position = models.TextField(verbose_name='Авторская позиция')
    text = models.ForeignKey(to=Text, on_delete=models.CASCADE, verbose_name='Проблемы текста', related_name='keys')

