import logging

from celery import shared_task
from django.db import IntegrityError

from tracker_app.models import UserDomainsHistory
from tracker_app.serializers import DomainSerializer

logger = logging.getLogger(__name__)

@shared_task
def add_data_in_database(user_id, domains, now):
    logger.info('Adding data to database')

    for domain in domains:
        data = {
            'user_id': user_id,
            'domain': domain,
            'created_at': now,
        }
        serializer_row_database = DomainSerializer(data=data)

        if not serializer_row_database.is_valid():
            logger.info(
                'Error during saving data; user_id: %s; domain: %s; created_at: %s; err: %s',
                user_id,
                domain,
                now,
                serializer_row_database.errors
            )
            continue
        try:
            UserDomainsHistory.objects.create(**serializer_row_database.validated_data)
        except IntegrityError as exc:
            logger.error('Error during saving data; user_id: %s; domain: %s; created_at: %s; err: %s',)
            raise exc
    logger.info('Finished adding data to database')

