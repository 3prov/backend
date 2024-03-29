from datetime import datetime, timedelta, date
import enum


class ControlUtils:
    class Weekdays(enum.Enum):
        Monday = 1
        Tuesday = 2
        Wednesday = 3
        Thursday = 4
        Friday = 5
        Saturday = 6
        Sunday = 7

    @staticmethod
    def get_current_time() -> datetime:
        return datetime.now()

    @staticmethod
    def _get_current_week_start_time() -> datetime:
        today = datetime(date.today().year, date.today().month, date.today().day)
        return today - timedelta(days=today.weekday())

    @staticmethod
    def get_current_week() -> Weekdays:
        _weekdays = {
            1: ControlUtils.Weekdays.Monday,
            2: ControlUtils.Weekdays.Tuesday,
            3: ControlUtils.Weekdays.Wednesday,
            4: ControlUtils.Weekdays.Thursday,
            5: ControlUtils.Weekdays.Friday,
            6: ControlUtils.Weekdays.Saturday,
            7: ControlUtils.Weekdays.Sunday,
        }
        return _weekdays[datetime.now().isoweekday()]

    @staticmethod
    def get_next_weekday_time(weekday: Weekdays) -> datetime:
        """
        Returns the date of the next given weekday after
        the current date. For example, the date of next Monday.
        """

        week_start = ControlUtils._get_current_week_start_time()
        days = (weekday.value - week_start.isoweekday() + 7) % 7
        days = 7 if days == 0 else days
        return week_start + timedelta(days=days)
