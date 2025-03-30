from django.shortcuts import render

# Create your views here.

from djoser.views import UserViewSet
from drf_yasg.utils import swagger_auto_schema
from djoser.views import UserViewSet
from rest_framework import permissions
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from rest_framework.response import Response

class CustomUserRegistrationView(UserViewSet):
    permission_classes = (permissions.AllowAny,)

    @swagger_auto_schema(
        operation_summary="Регистрация пользователя",
        operation_description="Создание нового пользователя и получение информации о нем после успеха.",
        responses={201: openapi.Response('Пользователь успешно зарегистрирован'), 400: 'Ошибка регистрации'},
    )
    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)

