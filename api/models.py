import uuid

from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone


class AuthSocialID(models.Model):
    vkontakte = models.PositiveIntegerField(null=True, blank=True)
    telegram = models.PositiveIntegerField(null=True, blank=True)


class User(AbstractUser):
    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    social_network = models.OneToOneField(
        to=AuthSocialID,
        on_delete=models.CASCADE,
        verbose_name='Социальная сеть',
        null=True
    )


class Week(models.Model):
    class Meta:
        verbose_name = 'Неделя'
        verbose_name_plural = 'Недели'

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)


class Task(models.Model):
    class Meta:
        abstract = True
        verbose_name = 'Задание для Пользователей'
        verbose_name_plural = 'Задания для Пользователей'

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    teacher = models.ForeignKey(to=User, on_delete=models.CASCADE, verbose_name='Учитель, который дал работу')
    created_at = models.DateTimeField(default=timezone.now, verbose_name='Дата создания')
    week = models.ForeignKey(to=Week, on_delete=models.CASCADE, verbose_name='Неделя')


class Work(models.Model):
    class Meta:
        abstract = True
        verbose_name = 'Работа Пользователя'
        verbose_name_plural = 'Работы Пользователя'

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    author = models.ForeignKey(to=User, on_delete=models.CASCADE, verbose_name='Автор работы')
    created_at = models.DateTimeField(default=timezone.now, verbose_name='Дата создания')

    def create_relation_to_task(self):
        raise NotImplementedError('Необходимо создать связь с моделью Task')
