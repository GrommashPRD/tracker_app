import time
from django.utils.deprecation import MiddlewareMixin
from tracker_app.statsd_client import statsd_client  # Импорт вашего клиента StatsD

class StatsDMiddleware(MiddlewareMixin):
    def process_request(self, request):
        request.start_time = time.time()

    def process_response(self, request, response):
        duration = time.time() - request.start_time
        view_name = request.resolver_match.view_name if request.resolver_match else 'unknown'

        statsd_client.timing(f'tracker.views.{view_name}.time', duration * 1000)
        statsd_client.incr(f'tracker.views.{view_name}.count')

        return response