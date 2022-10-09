from dataclasses import dataclass

import functools

from api.control.models import WeekID
from api.form_url.models import EssayFormURL, EvaluationFormURL, ResultsFormURL
from api.models import User
from api.services import filter_objects
from telegram import TelegramHelper
from triproverochki.celery import app

import logging

logger = logging.getLogger('celery')


@dataclass
class Message:
    receiver: User
    text: str


def mailing_status_decorator(func: callable):
    @functools.wraps(func)
    def mailing_wrapper(*args, **kwargs):
        TelegramHelper.send_message_to_admins('[✉️]: Начало рассылки')
        func_result = func(*args, **kwargs)
        TelegramHelper.send_message_to_admins('[✉️]: Конец рассылки')
        return func_result

    return mailing_wrapper


@mailing_status_decorator
def __process(
    app_self, messages: list[Message], users_count: int, users_count_from: int = 1
):
    i = users_count_from

    for message in messages:
        message.receiver.send_telegram_message(message=message.text)
        logger.info(f'{i}/{users_count}: {message.receiver.username} - {message.text}')
        app_self.update_state(
            state='PROGRESS', meta={'current': i, 'total': users_count}
        )
        i += 1


@app.task(bind=True)
def send_work_accepting_stage_start(self):
    text = 'Начался прием работ. Пора писать!'
    active_users = filter_objects(User.objects, is_active=True)
    users_count = active_users.count()
    messages = []
    for user in active_users:
        form_url, _ = EssayFormURL.objects.get_or_create(user=user)
        messages.append(
            Message(
                receiver=user,
                text=f'{text}\nВаша ссылка: {form_url.url}',
            )
        )

    __process(self, messages, users_count)


@app.task(bind=True)
def send_evaluation_accepting_stage_start(self):
    text_week_participants = (
        '[Участник недели] Начался прием оценок. Пора смотреть и оценивать!'
    )
    text_volunteer = '[Волонтер] Начался прием оценок. Пора смотреть и оценивать!'
    messages = []

    active_users = filter_objects(User.objects, is_active=True)
    for user in active_users:
        if user.is_week_participant:
            required_evaluations = filter_objects(
                EvaluationFormURL.objects,
                user=user,
                week_id=WeekID.get_current(),
                only=('url',),
            )

            messages.append(
                Message(
                    receiver=user,
                    text=f'{text_week_participants}\nВаши ссылки: {[x.url for x in required_evaluations]}',
                )
            )
        else:
            messages.append(
                Message(
                    receiver=user,
                    text=f'{text_volunteer}\nВы можете принять участие: /volunteer_evaluation',
                )
            )

    __process(self, messages, active_users.count())


@app.task(bind=True)
def send_closed_accept_stage(self):
    text_week_participants = (
        '[Участник недели] Прием оценок закончен. Пора смотреть результаты'
    )
    text_volunteer = '[Волонтер] Прием оценок закончен. Пора смотреть результаты'
    messages = []

    active_users = filter_objects(User.objects, is_active=True)
    for user in active_users:
        if user.is_week_participant:
            result_evaluations = filter_objects(
                ResultsFormURL.objects,
                user=user,
                week_id=WeekID.get_current(),
                only=('url',),
            )

            messages.append(
                Message(
                    receiver=user,
                    text=f'{text_week_participants}\nВаши ссылки: {[x.url for x in result_evaluations]}\nВсе работы недели: /week_results',
                )
            )

        else:
            messages.append(
                Message(
                    receiver=user,
                    text=f'{text_volunteer}\nВы можете посмотреть все работы неледи: /week_results',
                )
            )

    __process(self, messages, active_users.count())
