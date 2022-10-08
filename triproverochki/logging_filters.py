from logging import Filter, LogRecord


class NotInTestingFilter(Filter):
    def filter(self, record: LogRecord) -> bool:
        from django.conf import settings

        return not settings.TESTING_MODE
