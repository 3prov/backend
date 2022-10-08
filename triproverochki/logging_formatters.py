from datetime import datetime

from pythonjsonlogger import jsonlogger


class CustomJsonFormatter(jsonlogger.JsonFormatter):
    def add_fields(self, log_record, record, message_dict):
        super(CustomJsonFormatter, self).add_fields(log_record, record, message_dict)
        if not log_record.get('timestamp'):
            log_record['timestamp'] = datetime.utcnow().strftime(
                '%Y-%m-%dT%H:%M:%S.%fZ'
            )
        if log_record.get('level'):
            log_record['level'] = log_record['level'].upper()
        else:
            log_record['level'] = record.levelname

        if not log_record.get('pathname'):
            log_record['pathname'] = record.pathname

        if not log_record.get('lineno'):
            log_record['lineno'] = record.lineno


formatter = CustomJsonFormatter('%(timestamp)s %(level)s %(name)s %(message)s')
