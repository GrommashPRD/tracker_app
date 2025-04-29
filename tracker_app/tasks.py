import logging
from typing import List

from celery import shared_task
from django.db import IntegrityError

from tracker_app.serializers import DomainSerializer
from tracker_app.TimesTamp import TimeConstants
from .repository import DomainsInRange
from prometheus_client import Counter

DB_ERRORS_TOTAL = Counter('db_errors_total', 'Total number of database errors')
DB_SPECIFIC_ERRORS_TOTAL = Counter('db_specific_errors_total', 'Total number of specific DatabaseErrors')

logger = logging.getLogger(__name__)

repo = DomainsInRange()

@shared_task
def add_data_in_database(user_id:int , domains: List[str], repo=repo) -> None:
    logger.info('Adding data to database')

    current_timestamp = TimeConstants.now_timestamp_seconds()


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
            DB_SPECIFIC_ERRORS_TOTAL.inc()
            DB_ERRORS_TOTAL.inc()
            continue

        try:
            repo.add_user_domain_history(user_id=user_id, domain=domain, timestamp=current_timestamp)
        except IntegrityError as exc:
            logger.error('Error during saving data; user_id: %s; domain: %s; created_at: %s; err: %s', )
            DB_SPECIFIC_ERRORS_TOTAL.inc()
            DB_ERRORS_TOTAL.inc()
            raise exc
    logger.info('Finished adding data to database')

