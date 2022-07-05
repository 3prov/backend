import abc
import uuid

from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone
from .management.models import Stage, WeekID
from rest_framework.authtoken.models import Token
from django.db import transaction
import hashlib


class AbstractModelMeta(abc.ABCMeta, type(models.Model)):
    pass


class User(AbstractUser, metaclass=AbstractModelMeta):
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


class FormURL(models.Model):
    class Meta:
        verbose_name = 'Ссылка на форму'
        verbose_name_plural = 'Ссылки на формы'

    user = models.ForeignKey(to=User, on_delete=models.CASCADE, related_name='form_urls', verbose_name='Пользователь')
    url = models.URLField(
        unique=True,
        null=True,  # signal handles it
        verbose_name='Ссылка на форму',
    )
    week_id = models.ForeignKey(
        to=WeekID,
        on_delete=models.CASCADE,
        related_name='form_urls',
        verbose_name='Номер недели',
        null=True,  # signal handles it
    )
    # TODO: add null=True field, referenced to required checks

    @staticmethod
    def _hash_string(string: str) -> str:
        return str(hashlib.sha1(bytes(string, "UTF-8")).hexdigest())[:16]


class Task(models.Model, metaclass=AbstractModelMeta):
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
    week_id = models.OneToOneField(
        to=WeekID,
        on_delete=models.CASCADE,
        verbose_name='Идентификатор недели',
        related_name='task',
        null=True,  # signal handles it
    )

    @staticmethod
    @abc.abstractmethod
    def get_current():
        pass


class Work(models.Model, metaclass=AbstractModelMeta):
    class Meta:
        abstract = True
        verbose_name = 'Работа Пользователя'
        verbose_name_plural = 'Работы Пользователя'

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    author = models.ForeignKey(to=User, on_delete=models.CASCADE, verbose_name='Автор работы', related_name='works')
    created_at = models.DateTimeField(default=timezone.now, verbose_name='Дата создания')

    def __init__(self, *args, **kwargs):
        super(Work, self).__init__(*args, **kwargs)
        self.task

    @property
    def task(self):
        raise NotImplementedError('Необходимо создать связь с моделью Task.')
