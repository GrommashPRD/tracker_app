import logging
import time

from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from tracker_app import repository
from tracker_app.serializers import VisitedLinksSerializer, ViewPeriodSerializer,ErrInvalidUrlList, ErrInvalidValueStartOrEnd
from tracker_app.tasks import add_data_in_database
from tracker_app.utils import linksParser
from tracker_app.swagger_files.swagger_schemas import get_user_urls_schema, post_user_urls_schema
from prometheus_client import Counter, generate_latest


# Create your views here.
REQUEST_COUNTER = Counter('http_requests_total', 'Total number of HTTP requests', ['method', 'path'])

logger = logging.getLogger('django')


class LinksView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    @post_user_urls_schema()
    def post(self, request):
        REQUEST_COUNTER.labels(method='POST', path=request.path).inc()
        user_id_from_request = request.data.get('user_id')

        if user_id_from_request is None:
            logger.warning('User ID is None')
            return Response({"message": "User ID can't be None", "code": "user_id_is_none"}, status=400)

        if not isinstance(user_id_from_request, int):
            logger.warning("Invalid user ID: Expected int %s.", user_id_from_request)
            return Response({'message': 'User ID must be a it', 'code': 'invalid_user_id'}, status=400)

        if user_id_from_request != request.user.id:
            logger.warning("Another user ID")
            return Response({"message": "Someone else's User ID", "code": "someone_elses_user_id"}, status=401)

        serializer = VisitedLinksSerializer(data=request.data)

        try:
            serializer.is_valid()
        except ErrInvalidUrlList as err:
            logger.warning("Invalid URLs %", err)
            return Response({"message": "Invalid URL list", "code": "invalid_url_list"}, status=400)

        urls = serializer.validated_data['urls']

        domains = linksParser.get_unique_domains(urls)

        add_data_in_database.delay(
            user_id_from_request,
            domains,
        )

        return Response({'status': 'ok'}, status=200)


class DomainsView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    @get_user_urls_schema()
    def get(self, request):

        REQUEST_COUNTER.labels(method='GET', path=request.path).inc()

        user_id_from_request = request.query_params.get('user_id')

        if user_id_from_request is None:
            logger.warning('User ID is None')
            return Response({"message": "User ID can't be None", "code": "user_id_is_none"}, status=400)

        if not user_id_from_request.isdigit():
            logger.warning("Invalid user ID: Expected int %s.", user_id_from_request)
            return Response({'message': 'User ID must be a int', 'code': 'invalid_user_id'}, status=400)

        if int(user_id_from_request) != request.user.id:
            logger.warning("Another user ID")
            return Response({"message": "Someone else's User ID", "code": "someone_elses_user_id"}, status=401)



        serializer = ViewPeriodSerializer(data=request.query_params)

        try:
            serializer.is_valid()
        except ErrInvalidValueStartOrEnd as err:
            logger.warning("Invalid 'start' or 'end' value: %s", err)
            return Response({'message': "Invalid 'start' or 'end' value", "code": 'invalid_value'}, status=400)

        start_period = serializer.validated_data.get('start')
        end_period = serializer.validated_data.get('end')

        try:
            user_domains_history = repository.DomainsInRange(
                user_id=user_id_from_request,
                start_period=start_period,
                end_period=end_period
            )
            user_domains_in_range = user_domains_history.get_user_domains_in_range()

        except ValueError as ve:
            logger.error(f"Value error: %s", ve)
            return Response({'message': 'Bad request', 'code': 'bad_request'}, status=400)
        except TypeError as te:
            logger.error(f"Type error during serialization: %s", te)
            return Response({'message': 'Serialization error', 'code': 'serialization_error'}, status=500)


        return Response(user_domains_in_range)