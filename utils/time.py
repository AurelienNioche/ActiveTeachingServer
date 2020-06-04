from datetime import datetime
import pytz

FORMAT = '%Y-%m-%d %H:%M:%S.%f'


def string_to_datetime(string_time):
    return pytz.timezone('UTC').localize(datetime.strptime(string_time, FORMAT))


def datetime_to_sting(datetime_obj):
    return datetime_obj.astimezone(pytz.utc).strftime(FORMAT)
