from tracker_app.models import UserDomainsHistory
from tracker_app.serializers import DomainSerializer

class DomainsInRange:
    def __init__(self, user_id: int, start_period: int, end_period: int):
        self.user_id = user_id
        self.start_period = start_period
        self.end_period = end_period

    def get_user_domains_in_range(self) -> dict:
        user_domains_in_range = UserDomainsHistory.objects.filter(
            user_id=self.user_id,
            created_at__gte=self.start_period,
            created_at__lt=self.end_period
        )

        user_history = DomainSerializer(user_domains_in_range, many=True)

        user_domains_in_range = {'domains': set(), 'status': 'ok'}
        for d in list(user_history.data):
            user_domains_in_range['domains'].add(d.get('domain'))

        return user_domains_in_range
