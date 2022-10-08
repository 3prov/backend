from logging import Handler

from telegram import TelegramHelper


class SendTelegramHandler(Handler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def emit(self, record):
        log_entry = self.format(record)
        TelegramHelper.send_message_to_admins(
            text=f'<b>[{record.levelname}]</b>: {log_entry}',
        )
