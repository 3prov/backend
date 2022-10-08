import requests
from django.conf import settings

from telegram.exceptions import ChatNotFound, BotBlocked


def skip_send_while_testing_decorator(func):
    def skip_send_while_testing_wrapper(*args, **kwargs):
        if settings.TESTING_MODE:
            return
        return func(*args, **kwargs)

    return skip_send_while_testing_wrapper


class TelegramHelper:
    @staticmethod
    @skip_send_while_testing_decorator
    def send_message(
        chat_id: int,
        text: str,
        parse_mod: str = 'HTML',
        disable_notification: str = 'false',
        bot_secret: str = settings.TELEGRAM_BOT_TOKEN,
    ) -> None:
        url = 'https://api.telegram.org/bot{bot_secret}/sendMessage'.format(
            bot_secret=bot_secret
        )
        params = {
            'chat_id': chat_id,
            'text': text,
            'disable_notification': disable_notification,
            'parse_mode': parse_mod,
        }

        response = requests.get(url, params=params)
        response_json = response.json()

        if not response_json['ok']:
            match response_json['error_code']:
                case 400:
                    raise ChatNotFound
                case 403:
                    raise BotBlocked
                case _:
                    raise Exception(response_json['description'])

    @staticmethod
    @skip_send_while_testing_decorator
    def send_message_to_admins(text: str) -> None:
        return TelegramHelper.send_message(
            chat_id=settings.TELEGRAM_LOGS_CHAT_ID,
            text=text,
            bot_secret=settings.TELEGRAM_LOGS_BOT_TOKEN,
        )
