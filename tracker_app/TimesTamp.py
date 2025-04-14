import datetime
import pytz
from django.utils import timezone

class TimeConstants:
    @staticmethod
    def now_timestamp_seconds():
        return int((timezone.now() - datetime.datetime(1970, 1, 1, tzinfo=pytz.utc)).total_seconds())
