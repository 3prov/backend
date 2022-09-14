import requests
from django.conf import settings


class TelegramHelper:
    @staticmethod
    def send_message(
        chat_id: int,
        text: str,
        parse_mod: str = 'HTML',
        disable_notification: str = 'false',
    ) -> None:
        url = 'https://api.telegram.org/bot{bot_secret}/sendMessage'.format(
            bot_secret=settings.TELEGRAM_BOT_TOKEN
        )
        params = {
            'chat_id': chat_id,
            'text': text,
            'disable_notification': disable_notification,
            'parse_mode': parse_mod,
        }

        response = requests.get(url, params=params)
        print(response.text)
