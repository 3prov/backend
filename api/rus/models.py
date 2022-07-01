from django.db import models
from ..models import Work, Task


class Essay(Work):
    def create_relation_to_task(self):
        task = models.ForeignKey(
            to=Text,
            on_delete=models.CASCADE,
            verbose_name='Текст, по которому написано сочинение'
        )
    body = models.TextField(verbose_name='Поле для сочинения')


class Text(Task):
    body = models.TextField(verbose_name='Поле для текста')
    author = models.CharField(max_length=75, verbose_name='Автор текста')
    author_description = models.TextField(verbose_name='Описание автора текста')


class TextKeys(models.Model):
    range_of_problems = models.TextField(verbose_name='Примерный круг проблем')
    authors_position = models.TextField(verbose_name='Авторская позиция')
    text = models.ForeignKey(to=Text, on_delete=models.CASCADE, verbose_name='Проблемы текста')

