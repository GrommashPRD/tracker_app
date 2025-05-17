from tracker_app.models import UserDomainsHistory
from tracker_app.serializers import DomainSerializer

import logging

logger = logging.getLogger(__name__)


class DomainsInRange:
    def __init__(self):
        self.dataProvider = UserDomainsHistory

    def get_user_domains_in_range(self, user_id, start_period, end_period) -> dict:
        user_domains_in_range = self.dataProvider.objects.filter(
            user_id=user_id,
            created_at__gte=start_period,
            created_at__lt=end_period
        )

        user_history = DomainSerializer(user_domains_in_range, many=True)

        user_domains_in_range = {'domains': set(), 'status': 'ok'}
        for d in list(user_history.data):
            user_domains_in_range['domains'].add(d.get('domain'))

        return user_domains_in_range


    def add_user_domain_history(self, user_id, domain, timestamp):
        obj, created = self.dataProvider.objects.get_or_create(user_id=user_id, domain=domain)
        if created:
            obj.created_at = timestamp
        obj.updated_at = timestamp
        obj.save()
