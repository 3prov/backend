from __future__ import annotations
import abc
import uuid

from random import randint

from django.conf import settings
from django.db import models, transaction
from django.contrib.auth.models import AbstractUser
from django.utils import timezone
from .management.models import Stage, WeekID
from rest_framework.authtoken.models import Token
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
    rating = models.PositiveIntegerField(
        default=50,
        verbose_name='Рейтинг',
    )

    @transaction.atomic
    def save(self, *args, **kwargs):
        if not self.pk:
            return
        Token.objects.get_or_create(user=self)
        return super(User, self).save(*args, **kwargs)

    @transaction.atomic
    def delete(self, using=None, keep_parents=False):
        Token.objects.get(user=self).delete()
        return super(User, self).delete(using, keep_parents)

    def increase_rating(self, value: int):
        self.rating += value
        self.save()

    def reduce_rating(self, value: int):
        if self.rating - value < 0:
            self.rating = 0
        else:
            self.rating -= value
        self.save()


class FormURL(models.Model, metaclass=AbstractModelMeta):
    class Meta:
        abstract = True
        verbose_name = 'Ссылка на форму'
        verbose_name_plural = 'Ссылки на формы'

    user = models.ForeignKey(
        to=User,
        on_delete=models.CASCADE,
        related_name='%(app_label)s_%(class)s_form_urls',
        verbose_name='Пользователь',
    )
    url = models.URLField(
        unique=True,
        null=True,  # signal handles it
        verbose_name='Ссылка на форму',
    )
    week_id = models.ForeignKey(
        to=WeekID,
        on_delete=models.CASCADE,
        related_name='%(app_label)s_%(class)s_form_urls',
        verbose_name='Номер недели',
        null=True,  # signal handles it
    )

    @staticmethod
    def _hash_string(string: str) -> str:
        return str(hashlib.sha1(bytes(string, "UTF-8")).hexdigest())[:16]

    @staticmethod
    @abc.abstractmethod
    def get_from_url(url: str) -> FormURL | None:
        pass

    def save(
        self, force_insert=False, force_update=False, using=None, update_fields=None
    ):
        from api.form_url.models import EvaluationFormURL

        _user_evaluation_form_already_count = EvaluationFormURL.objects.filter(
            user=self.user, week_id=WeekID.get_current()
        ).count()
        self.url = self._hash_string(
            settings.STRING_HASH_TEMPLATE.format(
                user_id=self.user.id,
                week_id=WeekID.get_current().id,
                hash_type=f'{type(self).__name__}{_user_evaluation_form_already_count}',
                django_secret_key=settings.SECRET_KEY,
            )
        )
        super().save(force_insert, force_update, using, update_fields)


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
        related_name='tasks',
    )
    created_at = models.DateTimeField(
        default=timezone.now, verbose_name='Дата создания'
    )
    week_id = models.OneToOneField(
        to=WeekID,
        on_delete=models.CASCADE,
        verbose_name='Идентификатор недели',
        related_name='task',
        null=True,  # signal handles it
    )

    @staticmethod
    @abc.abstractmethod
    def get_current() -> Task:
        pass


class Work(models.Model, metaclass=AbstractModelMeta):
    class Meta:
        abstract = True
        verbose_name = 'Работа Пользователя'
        verbose_name_plural = 'Работы Пользователя'

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    author = models.ForeignKey(
        to=User,
        on_delete=models.CASCADE,
        verbose_name='Автор работы',
        related_name='works',
    )
    created_at = models.DateTimeField(
        default=timezone.now, verbose_name='Дата создания'
    )

    @property
    @abc.abstractmethod
    def task(self):
        raise NotImplementedError('Необходимо создать связь с моделью Task.')

    @abc.abstractmethod
    def save(
        self, force_insert=False, force_update=False, using=None, update_fields=None
    ):
        """
        Необходимо переопределить метод save для изменения рейтинга пользователя.
        """
        return super(Work, self).save(force_insert, force_update, using, update_fields)


class Evaluation(models.Model, metaclass=AbstractModelMeta):
    class Meta:
        abstract = True
        verbose_name = 'Проверка'
        verbose_name_plural = 'Проверки'

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    evaluator = models.ForeignKey(
        to=User,
        on_delete=models.CASCADE,
        verbose_name='Проверяющий',
        related_name='evaluations',
    )
    created_at = models.DateTimeField(
        default=timezone.now, verbose_name='Дата создания'
    )

    @property
    @abc.abstractmethod
    def work(self):
        raise NotImplementedError('Необходимо создать связь с моделью Work.')

    @property
    @abc.abstractmethod
    def criteria(self):
        raise NotImplementedError(
            'Необходимо создать OneToOne связь с моделью Criteria.'
        )

    @abc.abstractmethod
    def save(
        self, force_insert=False, force_update=False, using=None, update_fields=None
    ):
        """
        Необходимо переопределить метод save для изменения рейтинга пользователя.
        """
        return super(Evaluation, self).save(
            force_insert, force_update, using, update_fields
        )


class Criteria(models.Model, metaclass=AbstractModelMeta):
    class Meta:
        abstract = True
        verbose_name = 'Критерий оценивая'
        verbose_name_plural = 'Критерии оценивания'

    @property
    @abc.abstractmethod
    def score(self):
        raise NotImplementedError(
            'Необходимо объявить свойство подсчета балла по критериям.'
        )
