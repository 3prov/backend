import functools

from api.models import User
from api.services import filter_objects
from telegram import TelegramHelper
from triproverochki.celery import app


def mailing_decorator(func: callable):
    @functools.wraps(func)
    def mailing_wrapper(*args, **kwargs):
        TelegramHelper.send_message_to_admins('Начало рассылки')
        func_result = func(*args, **kwargs)
        TelegramHelper.send_message_to_admins('Конец рассылки')
        return func_result

    return mailing_wrapper


@mailing_decorator
def __process(
    app_self, users: set, message: str, users_count: int, users_count_from: int = 1
):
    i = users_count_from
    for user in users:
        user.send_telegram_message(message=message)
        app_self.update_state(
            state='PROGRESS', meta={'current': i, 'total': users_count}
        )
        print(f'{i}/{users_count}: {user.username}')  # TODO: to logger
        i += 1


@app.task(bind=True)
def send_work_accepting_stage_start(self):
    message = 'Начался прием работ. Пора писать!'
    users = filter_objects(User.objects, is_active=True)
    users_count = users.count()
    __process(self, set(users), message, users_count)


@app.task(bind=True)
def send_evaluation_accepting_stage_start(self):
    message_week_participants = (
        '[Участник недели] Начался прием оценок. Пора смотреть и оценивать!'
    )
    message_volunteer = '[Волонтер] Начался прием оценок. Пора смотреть и оценивать!'
    users_week_participants = set()
    users_volunteer = set()

    for user in filter_objects(User.objects, is_active=True):
        if user.is_week_participant:
            users_week_participants.add(user)
        else:
            users_volunteer.add(user)

    users_count = len(users_week_participants) + len(users_volunteer)
    __process(self, users_week_participants, message_week_participants, users_count)
    __process(
        self,
        users_volunteer,
        message_volunteer,
        users_count,
        users_count_from=len(users_week_participants) + 1,
    )


@app.task(bind=True)
def send_closed_accept_stage(self):
    message_week_participants = (
        '[Участник недели] Прием оценок закончен. Пора смотреть результаты'
    )
    message_volunteer = '[Волонтер] Прием оценок закончен. Пора смотреть результаты'
    users_week_participants = set()
    users_volunteer = set()

    for user in filter_objects(User.objects, is_active=True):
        if user.is_week_participant:
            users_week_participants.add(user)
        else:
            users_volunteer.add(user)

    users_count = len(users_week_participants) + len(users_volunteer)
    __process(self, users_week_participants, message_week_participants, users_count)
    __process(
        self,
        users_volunteer,
        message_volunteer,
        users_count,
        users_count_from=len(users_week_participants) + 1,
    )
