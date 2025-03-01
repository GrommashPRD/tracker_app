from django.http import HttpResponse
from django.shortcuts import render
from django.utils import timezone
import logging
import datetime
import pytz

from rest_framework.response import Response
from rest_framework.views import APIView

from tracker_app import serializers
from tracker_app.models import UserDomainsHistory
from tracker_app.serializers import VisitedLinksSerializer, DomainSerializer
from tracker_app.utils import linksParser

# Create your views here.
logger = logging.getLogger('main')

class LinksView(APIView):

    def post(self, request):
        user_id = request.META.get('HTTP_X_USER_ID')
        if not user_id:
            return Response(
                {'message': 'Request has not X-User-ID'},
                status=403
            )
        serializer = VisitedLinksSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        urls = serializer.validated_data['urls']

        try:
            domains = linksParser.get_unique_domains(urls)
        except Exception as err:
            logger.error(err)
            return Response({'message': 'Internal error', 'code': 'internal_error'}, status=500)

        now_timestamp_seconds = int((timezone.now() - datetime.datetime(1970, 1, 1, tzinfo=pytz.utc)).total_seconds())


        for domain in domains:
            obj, created = UserDomainsHistory.objects.get_or_create(user_id=user_id, domain=domain)
            if created:
                obj.created_at = now_timestamp_seconds
            obj.updated_at = now_timestamp_seconds
            obj.save()

        return Response({'status': 'ok'}, status=200)


class DomainsView(APIView):

    def get(self, request):
        user_id = request.META.get('HTTP_X_USER_ID')
        if not user_id:
            return Response(
                {'status': 'Request has not X-User-ID'},
                status=403
            )

        serializer = serializers.ViewPeriodSerializer(data=request.query_params)
        serializer.is_valid(raise_exception=True)

        start_period = serializer.validated_data.get('start')
        end_period = serializer.validated_data.get('end')

        try:
            user_domains_in_range = self._get_user_domains_in_range(
                user_id=user_id,
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




