import logging
from typing import List

from celery import shared_task
from django.db import IntegrityError

from tracker_app.models import UserDomainsHistory
from tracker_app.serializers import DomainSerializer
from tracker_app.actualTimestamp import time_constants
logger = logging.getLogger(__name__)


@shared_task
def add_data_in_database(user_id:int , domains: List[str]) -> None:
    logger.info('Adding data to database')

    current_timestamp = time_constants.now_timestamp_seconds

    for domain in domains:
        data = {
            'user_id': user_id,
            'domain': domain,
            'created_at': current_timestamp,
        }
        serializer_row_database = DomainSerializer(data=data)

        if not serializer_row_database.is_valid():
            logger.error(
                'Error during saving data; user_id: %s; domain: %s; created_at: %s; err: %s',
                user_id,
                domain,
                current_timestamp,
                serializer_row_database.errors
            )
            continue

        try:
            obj, created = UserDomainsHistory.objects.get_or_create(user_id=user_id, domain=domain)
            if created:
                obj.created_at = current_timestamp
            obj.updated_at = current_timestamp
            obj.save()
        except IntegrityError as exc:
            logger.error('Error during saving data; user_id: %s; domain: %s; created_at: %s; err: %s', )
            raise exc
    logger.info('Finished adding data to database')

