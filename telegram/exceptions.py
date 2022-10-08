class BotBlocked(Exception):
    __doc__ = 'Forbidden: bot was blocked by the user'


class ChatNotFound(Exception):
    __doc__ = 'Bad Request: chat not found'
