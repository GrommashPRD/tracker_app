import logging
import datetime
import pytz
import time

from rest_framework import status
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from django.utils import timezone
from tracker_app.models import UserDomainsHistory
from tracker_app.serializers import VisitedLinksSerializer, DomainSerializer, ViewPeriodSerializer
from tracker_app.tasks import add_data_in_database
from tracker_app.utils import linksParser
from tracker_app.swagger_files.swagger_schemas import get_user_urls_schema, post_user_urls_schema
from prometheus_client import Counter, Histogram


# Create your views here.


logger = logging.getLogger('django')

# Счетчик для фиксирования количества запросов
REQUEST_COUNT_POST = Counter('post_view_requests_total', 'Total number of requests to Views')
REQUEST_COUNT_GET = Counter('get_view_requests_total', 'Total number of requests to Views')

# Гистограмма для измерения времени ответа
REQUEST_LATENCY_POST = Histogram('post_view_request_latency_seconds', 'Latency of requests to Views in seconds')
REQUEST_LATENCY_GET = Histogram('get_view_request_latency_seconds', 'Latency of requests to Views in seconds')


class LinksView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]


    @post_user_urls_schema()
    @REQUEST_LATENCY_POST.time()
    def post(self, request):

        REQUEST_COUNT_POST.inc()

        start_time = time.time()

        user_id_from_request = request.data.get('user_id')

        if user_id_from_request is None:
            logger.error('User ID is None')
            return Response({"error": "User ID cannot be None."}, status=status.HTTP_400_BAD_REQUEST)

        if not isinstance(user_id_from_request, int):
            logger.error(f"Invalid user ID: {user_id_from_request}. Expected int.")
            return Response({'message': 'user_id must be a int', 'code': 'invalid_user_id'}, status=400)

        if user_id_from_request != request.user.id:
            logger.error("Another user ID")
            return Response({"error": "You are not entering your ID."}, status=status.HTTP_401_UNAUTHORIZED)

        serializer = VisitedLinksSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        urls = serializer.validated_data['urls']

        if not urls:
            logger.error("Empty URL list")
            return Response({'message': 'URL list cannot be empty', 'code': 'empty_url_list'}, status=400)
        try:
            domains = linksParser.get_unique_domains(urls)
        except:
            logger.error("Invalid URL list")
            return Response({'message': 'Internal error', 'code': 'internal_error'}, status=500)

        now_timestamp_seconds = int((timezone.now() - datetime.datetime(1970, 1, 1, tzinfo=pytz.utc)).total_seconds())

        add_data_in_database.delay(
            user_id_from_request,
            domains,
            now_timestamp_seconds,
        )

        latency = time.time() - start_time

        return Response({'status': 'ok'}, status=200)


class DomainsView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    @get_user_urls_schema()
    @REQUEST_LATENCY_GET.time()
    def get(self, request):

        REQUEST_COUNT_GET.inc()

        start_time = time.time()

        user_id_from_request = request.query_params.get('user_id')

        if user_id_from_request is None:
            return Response({"error": "Введите Ваш ID"}, status=status.HTTP_400_BAD_REQUEST)

        if int(user_id_from_request) != request.user.id:
            return Response({"error": "Вы вводите не свой ID"}, status=status.HTTP_401_UNAUTHORIZED)

        serializer = ViewPeriodSerializer(data=request.query_params)
        serializer.is_valid(raise_exception=True)

        start_period = serializer.validated_data.get('start')
        end_period = serializer.validated_data.get('end')

        try:
            user_domains_in_range = self._get_user_domains_in_range(
                user_id=user_id_from_request,
                start_period=start_period,
                end_period=end_period,
            )
        except Exception as err:
            logger.error(err)
            return Response({'status': 'Internal error', 'code': 'internal_error'}, status=500)

        latency = time.time() - start_time

        return Response(user_domains_in_range)


    @staticmethod
    def _get_user_domains_in_range(user_id, start_period, end_period):
        user_domains_in_range = UserDomainsHistory.objects.filter(
            user_id=user_id, created_at__gte=start_period, created_at__lt=end_period
        )

        user_history = DomainSerializer(user_domains_in_range, many=True)

        user_domains_in_range = {'domains': set(), 'status': 'ok'}
        for d in list(user_history.data):
            user_domains_in_range['domains'].add(d.get('domain'))

        return user_domains_in_range




