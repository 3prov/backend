import uuid

from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone
from .management.models import Stage
from rest_framework.authtoken.models import Token
from django.db import transaction


class User(AbstractUser):
    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    vkontakte_id = models.PositiveIntegerField(null=True, blank=True)
    telegram_id = models.PositiveIntegerField(null=True, blank=True)

    @transaction.atomic
    def save(self, *args, **kwargs):
        if not self.pk:
            return
        Token.objects.get_or_create(user=self)
        return super(User, self).save(*args, **kwargs)


class Task(models.Model):
    class Meta:
        abstract = True
        verbose_name = 'Задание для Пользователей'
        verbose_name_plural = 'Задания для Пользователей'

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    teacher = models.ForeignKey(
        to=User,
        on_delete=models.CASCADE,
        verbose_name='Учитель, который дал работу',
        related_name='tasks'
    )
    created_at = models.DateTimeField(default=timezone.now, verbose_name='Дата создания')
    stage = models.ForeignKey(to=Stage, on_delete=models.CASCADE, verbose_name='Неделя', related_name='tasks')


class Work(models.Model):
    class Meta:
        abstract = True
        verbose_name = 'Работа Пользователя'
        verbose_name_plural = 'Работы Пользователя'

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    author = models.ForeignKey(to=User, on_delete=models.CASCADE, verbose_name='Автор работы', related_name='works')
    created_at = models.DateTimeField(default=timezone.now, verbose_name='Дата создания')

    def create_relation_to_task(self):
        raise NotImplementedError('Необходимо создать связь с моделью Task')
