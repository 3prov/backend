from __future__ import annotations
from api.models import FormURL
from api.rus.models import Essay

from django.db import models


class EssayFormURL(FormURL):
    class Meta:
        verbose_name = 'Ссылка на форму сдачи сочинений'
        verbose_name_plural = 'Ссылки на формы сдачи сочинений'

    @staticmethod
    def get_from_url(url: str) -> EssayFormURL | None:
        try:
            return EssayFormURL.objects.get(url=url)
        except EssayFormURL.DoesNotExist:
            return None


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

    @staticmethod
    def get_from_url(url: str) -> EvaluationFormURL | None:
        try:
            return EvaluationFormURL.objects.get(url=url)
        except EvaluationFormURL.DoesNotExist:
            return None


class ResultsFormURL(FormURL):
    class Meta:
        verbose_name = 'Ссылка на форму просмотра результата'
        verbose_name_plural = 'Ссылки на формы просмотра результатов'

    @staticmethod
    def get_from_url(url: str) -> ResultsFormURL | None:
        try:
            return ResultsFormURL.objects.get(url=url)
        except ResultsFormURL.DoesNotExist:
            return None
