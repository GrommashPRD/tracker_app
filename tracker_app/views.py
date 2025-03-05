from django.db import IntegrityError, OperationalError
from django.http import HttpResponse
from django.shortcuts import render
from django.utils import timezone

from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.authentication import TokenAuthentication
from rest_framework.decorators import permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from tracker_app import serializers
from tracker_app.models import UserDomainsHistory
from tracker_app.serializers import VisitedLinksSerializer, DomainSerializer, ViewPeriodSerializer
from tracker_app.utils import linksParser, created_or_updated
from tracker_app.swagger_files.swagger_schemas import get_user_urls_schema, post_user_urls_schema

import logging
import datetime
import pytz

# Create your views here.
logger = logging.getLogger('django')

class LinksView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    @post_user_urls_schema()
    def post(self, request):
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

        try:
            created_or_updated.create_or_update(domains, user_id_from_request)
        except IntegrityError as e:
            logger.error(f"IntegrityError: {str(e)}")
            return Response({"error": "Conflict due to integrity violation."}, status=409)

        except OperationalError as e:
            logger.error(f"OperationalError: {str(e)}")
            return Response({"error": "Database operation error."}, status=503)

        except TypeError as e:
            logger.error(f"TypeError: {str(e)}")
            return Response({"error": "Invalid input data."}, status=400)

        except Exception as e:
            logger.error(f"Unexpected error: {str(e)}")
            return Response({"error": "An unexpected error occurred."}, status=500)

        return Response({'status': 'ok'}, status=200)


class DomainsView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    @get_user_urls_schema()
    def get(self, request):

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




