import pytest
from rest_framework import status
from rest_framework.test import APIClient
from django.contrib.auth import get_user_model
import logging
import subprocess
import time

User = get_user_model()

logger = logging.getLogger("tests")

@pytest.fixture
def api_client():
    return APIClient()

#Создаем юзера который будет автирозовываться для тестов.
def create_and_login_user(api_client, username='testuser', password='testpassword123'):
    #Создание тест-юзера
    user_data = {
        'username': username,
        'password': password,
    }
    response = api_client.post('/auth/register/', user_data, format='json')
    assert response.status_code == status.HTTP_201_CREATED

    #Авторизовываем тест-юзера
    login_data = {
        'username': username,
        'password': password
    }
    response = api_client.post('/auth/token/login/', login_data, format='json')
    assert response.status_code == status.HTTP_200_OK

    #Вытягиваем токен access
    token = response.data['auth_token']
    api_client.credentials(HTTP_AUTHORIZATION='Token ' + token)

    return User.objects.get(username=username)

#Тест что юзер авторизовался и запулил свои url
@pytest.mark.django_db
def test_user_auth_and_create_post(api_client):
    user = create_and_login_user(api_client)

    links_data = {
        "user_id": user.id,
        "urls": [
            "https://ya.ru/",
            "https://ya.ru/search/?text=мемы+с+котиками",
            "https://sber.ru",
            "https://stackoverflow.com/questions/65724760/how-it-is"
        ]
    }
    response = api_client.post('/visited_links', data=links_data, format='json')

    assert response.status_code == 200
    assert {'status': 'ok'} == response.data

#Тест что юзер взял чужой ID
@pytest.mark.django_db
def test_with_alien_id(api_client):
    user = create_and_login_user(api_client)

    links_data = {
        "user_id": 23,
        "urls": [
            "https://ya.ru/",
            "https://ya.ru/search/?text=мемы+с+котиками",
            "https://sber.ru",
            "https://stackoverflow.com/questions/65724760/how-it-is"
        ]
    }

    response = api_client.post('/visited_links', data=links_data, format='json')

    assert response.status_code == 401
    assert {"message": "Someone else's User ID", "code": "someone_elses_user_id"} == response.data


#Тест что юзер передает пустой список URL
@pytest.mark.django_db
def test_create_post_with_empty_urls(api_client):
    user = create_and_login_user(api_client)

    links_data = {
        "user_id": user.id,
        "urls": []
    }

    response = api_client.post('/visited_links', data=links_data, format='json')

    assert response.status_code == 400  # Ожидаем ошибку из-за пустого списка
    assert {"message": "Invalid URL list", "code": "invalid_url_list"} == response.data


#Тест, что юзер передает ID неверного формата str вместо int
@pytest.mark.django_db
def test_create_post_with_invalid_user_id(api_client):
    user = create_and_login_user(api_client)

    links_data = {
        "user_id": "asd",
        "urls": [
            "https://ya.ru/"
        ]
    }

    response = api_client.post('/visited_links', data=links_data, format='json')

    assert response.status_code == 400
    assert {'message': 'User ID must be a it', 'code': 'invalid_user_id'} == response.data