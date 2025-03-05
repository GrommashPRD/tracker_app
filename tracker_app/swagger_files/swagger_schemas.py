from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

from tracker_app.serializers import VisitedLinksSerializer


def get_user_urls_schema():
    return swagger_auto_schema(
        operation_description="Получить домены пользователя в заданном временном диапазоне.",
        manual_parameters=[
            openapi.Parameter('start', openapi.IN_QUERY, description="Начало временного диапазона",
                              type=openapi.TYPE_STRING),
            openapi.Parameter('end', openapi.IN_QUERY, description="Конец временного диапазона",
                              type=openapi.TYPE_STRING),
            openapi.Parameter('X-User-ID', openapi.IN_HEADER, description="ID пользователя", type=openapi.TYPE_STRING)
        ],
        responses={
            200: openapi.Response(
                description="Успешный ответ",
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        'domains': openapi.Schema(type=openapi.TYPE_ARRAY,
                                                  items=openapi.Items(type=openapi.TYPE_STRING)),
                        'status': openapi.Schema(type=openapi.TYPE_STRING)
                    }
                )
            ),
            403: openapi.Response(
                description="Запрос не содержит X-User-ID"
            ),
            500: openapi.Response(
                description="Внутренняя ошибка сервера"
            )
        }
    )


def post_user_urls_schema():
    return swagger_auto_schema(
        operation_description="Создание пользователя и добавление url-адрессов либо обновление url-адрессов у имеющегося пользователя.",
        manual_parameters=[
            openapi.Parameter(
                'X-User-ID',
                openapi.IN_HEADER,
                description="ID пользователя, отправляемый в заголовке запроса.",
                type=openapi.TYPE_STRING,
                required=True
            )
        ],
        request_body=VisitedLinksSerializer,
        responses={
            200: openapi.Response(
                description="Успешное выполнение запроса.",
                schema=VisitedLinksSerializer
            ),
            403: openapi.Response(
                description="Отсутствует X-User-ID в заголовке."
            ),
            500: openapi.Response(
                description="Внутренняя ошибка сервера."
            )
        }
    )