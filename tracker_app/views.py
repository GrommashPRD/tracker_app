import logging

from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from tracker_app.repository import get_user_domains_in_range
from tracker_app.serializers import VisitedLinksSerializer, ViewPeriodSerializer
from tracker_app.tasks import add_data_in_database
from tracker_app.utils import linksParser
from tracker_app.swagger_files.swagger_schemas import get_user_urls_schema, post_user_urls_schema

# Create your views here.


logger = logging.getLogger('django')


class LinksView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    @post_user_urls_schema()
    def post(self, request):
        user_id_from_request = request.data.get('user_id')

        if user_id_from_request is None:
            logger.warning('User ID is None')
            return Response({"error": "User ID не может быть пустым."}, status=400)

        if not isinstance(user_id_from_request, int):
            logger.warning("Invalid user ID: Expected int %s." % (user_id_from_request))
            return Response({'message': 'User ID должно быть числом', 'code': 'invalid_user_id'}, status=400)

        if user_id_from_request != request.user.id:
            logger.warning("Another user ID")
            return Response({"error": "Вы вводите не свой ID"}, status=401)

        serializer = VisitedLinksSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        urls = serializer.validated_data['urls']

        if not urls:
            logger.warning("Empty URL list")
            return Response({'message': 'Список URL не должен быть пустым', 'code': 'empty_url_list'}, status=400)
        try:
            domains = linksParser.get_unique_domains(urls)
        except ValueError as ve:
            logger.error("Value error: %s", ve)
            return Response({'message': 'Неправильный список URL', 'code': 'invalid_url_list'}, status=400)

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

        user_id_from_request = request.query_params.get('user_id')

        if user_id_from_request is None:
            logger.warning('User ID is None')
            return Response({"warning": "Введите Ваш ID"}, status=400)

        if int(user_id_from_request) != request.user.id:
            logger.warning("Another user ID")
            return Response({"warning": "Вы вводите не свой ID"}, status=401)

        serializer = ViewPeriodSerializer(data=request.query_params)
        serializer.is_valid(raise_exception=True)

        start_period = serializer.validated_data.get('start')
        end_period = serializer.validated_data.get('end')

        try:
            user_domains_in_range = get_user_domains_in_range(
                user_id=user_id_from_request,
                start_period=start_period,
                end_period=end_period,
            )
        except ValueError as ve:
            logger.error(f"Value error: %s", ve)
            return Response({'status': 'Bad request', 'code': 'bad_request'}, status=400)
        except TypeError as te:
            logger.error(f"Type error during serialization: %s", te)
            return Response({'status': 'Serialization error', 'code': 'serialization_error'}, status=500)

        return Response(user_domains_in_range)