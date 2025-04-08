import datetime
import pytz
from django.utils import timezone

class TimeConstants:
    @property
    def now_timestamp_seconds(self):
        return int((timezone.now() - datetime.datetime(1970, 1, 1, tzinfo=pytz.utc)).total_seconds())

time_constants = TimeConstants()