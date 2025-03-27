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
            openapi.Parameter('user_id', openapi.IN_QUERY, description="ID пользователя", type=openapi.TYPE_STRING)
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
                description="Запрос не содержит user_id"
            ),
            500: openapi.Response(
                description="Внутренняя ошибка сервера"
            )
        }
    )


def post_user_urls_schema():
    return swagger_auto_schema(
        operation_description="Добавление / Обновление url-адресов для user_id.",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'user_id': openapi.Schema(type=openapi.TYPE_INTEGER, description="ID пользователя (целое число)"),
                'urls': openapi.Schema(
                    type=openapi.TYPE_ARRAY,
                    items=openapi.Schema(type=openapi.TYPE_STRING, description="Список URL для обработки")
                ),
            },
            required=['user_id', 'urls'],  # Укажите обязательные поля
        ),
        responses={
            200: openapi.Response('Успешный ответ', openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties={
                    'status': openapi.Schema(type=openapi.TYPE_STRING, example='ok')
                }
            )),
            400: openapi.Response('Ошибка 400', openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties={
                    'error': openapi.Schema(type=openapi.TYPE_STRING),
                    'message': openapi.Schema(type=openapi.TYPE_STRING),
                    'code': openapi.Schema(type=openapi.TYPE_STRING),
                }
            )),
            401: openapi.Response('Ошибка 401', openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties={
                    'error': openapi.Schema(type=openapi.TYPE_STRING)
                }
            )),
        }
    )