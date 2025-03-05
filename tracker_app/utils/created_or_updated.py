from tracker_app.models import UserDomainsHistory
from django.utils import timezone

import datetime
import pytz

def create_or_update(domains, user_id):

    now_timestamp_seconds = int((timezone.now() - datetime.datetime(1970, 1, 1, tzinfo=pytz.utc)).total_seconds())

    for domain in domains:
        obj, created = UserDomainsHistory.objects.get_or_create(user_id=user_id, domain=domain)
        if created:
            obj.created_at = now_timestamp_seconds
        obj.updated_at = now_timestamp_seconds
        obj.save()