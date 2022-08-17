from __future__ import annotations

from rest_framework import permissions

from api.models import FormURL
from api.rus.models import Essay

from django.db import models


class EssayFormURL(FormURL):
    class Meta:
        verbose_name = 'Ссылка на форму сдачи сочинений'
        verbose_name_plural = 'Ссылки на формы сдачи сочинений'

    @classmethod
    def get_from_url_or_404(cls, url: str) -> EssayFormURL | None:
        try:
            return cls.objects.get(url=url)
        except cls.DoesNotExist:
            raise permissions.exceptions.ValidationError(
                {'detail': 'Ссылка недействительна.'}
            )


class EvaluationFormURL(FormURL):
    class Meta:
        verbose_name = 'Ссылка на форму сдачи проверок'
        verbose_name_plural = 'Ссылки на формы сдачи проверок'

    evaluation_work = models.ForeignKey(
        to=Essay,
        on_delete=models.CASCADE,
        related_name='evaluation_form_urls',
        verbose_name='Работа для проверки',
    )

    @classmethod
    def get_from_url_or_404(cls, url: str) -> EvaluationFormURL | None:
        try:
            return cls.objects.get(url=url)
        except cls.DoesNotExist:
            raise permissions.exceptions.ValidationError(
                {'detail': 'Ссылка недействительна.'}
            )


class ResultsFormURL(FormURL):
    class Meta:
        verbose_name = 'Ссылка на форму просмотра результата'
        verbose_name_plural = 'Ссылки на формы просмотра результатов'

    @classmethod
    def get_from_url_or_404(cls, url: str) -> ResultsFormURL | None:
        try:
            return cls.objects.get(url=url)
        except cls.DoesNotExist:
            raise permissions.exceptions.ValidationError(
                {'detail': 'Ссылка недействительна.'}
            )
