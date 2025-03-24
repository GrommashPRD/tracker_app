from tracker_app.models import UserDomainsHistory
from tracker_app.serializers import DomainSerializer


def get_user_domains_in_range(user_id: int, start_period: int, end_period: int) -> dict:
    user_domains_in_range = UserDomainsHistory.objects.filter(
        user_id=user_id,
        created_at__gte=start_period,
        created_at__lt=end_period
    )

    user_history = DomainSerializer(user_domains_in_range, many=True)

    user_domains_in_range = {'domains': set(), 'status': 'ok'}
    for d in list(user_history.data):
        user_domains_in_range['domains'].add(d.get('domain'))

    return user_domains_in_range