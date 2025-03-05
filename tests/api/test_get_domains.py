import pytest
from rest_framework import status
from rest_framework.test import APIClient
from django.contrib.auth import get_user_model

from tracker_app.models import UserDomainsHistory

User = get_user_model()


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
    response = api_client.post('/api/auth/users/', user_data, format='json')
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

@pytest.mark.django_db
@pytest.mark.parametrize(
    ('start', 'end', 'expected_domains'),
    [
        pytest.param(
            122,
            125,
            {
                'ya.ru',
                'test.ru'
            },
            id='get-all-domains'
        ),
        pytest.param(
            122,
            124,
            {
                'ya.ru',
            },
            id='get-one-domain'
        ),
        pytest.param(
            125,
            128,
            set(),
            id='get-no-one-domain'
        ),
    ]
)
#Получение URL по заданным параметрам
def test_green_get_domains(api_client, start, end, expected_domains):
    user = create_and_login_user(api_client)

    UserDomainsHistory.objects.create(user_id=user.id, domain='ya.ru', created_at=123)
    UserDomainsHistory.objects.create(user_id=user.id, domain='ya.ru', created_at=124)
    UserDomainsHistory.objects.create(user_id=user.id, domain='test.ru', created_at=124)

    response = api_client.get('/visited_domains', {"user_id": user.id,"start": start, "end": end}, format='json')

    assert response.status_code == 200
    assert set(response.data['domains']) == expected_domains

#Юзер пытается посмотреть URL адреса другого ID
@pytest.mark.django_db
def test_alien_id():
    user = User.objects.create(username='test1', password='test2')

    client = APIClient()
    client.login(username='test1', password='test2')

    response = client.get('/visited_domains', {"user_id": 12, "start":1 , "end": 2}, format='json')

    assert response.status_code == 401

@pytest.mark.django_db
@pytest.mark.parametrize(
    ('start', 'end'),
    [
        pytest.param(
            'h',
            10,
            id='wrong-start'
        ),
        pytest.param(
            1,
            'h',
            id='wrong-end'
        ),
        pytest.param(
            None,
            'h',
            id='none-start'
        ),
        pytest.param(
            'h',
            None,
            id='none-end'
        ),
        pytest.param(
            None,
            None,
            id='none-all'
        ),
    ]
)
#Тесты с неверными форматами данных
def test_wrong_params(api_client, start, end):
    user = create_and_login_user(api_client)
    params = {}
    if start:
        params['start'] = start
    if end:
        params['end'] = end
    response = api_client.get('/visited_domains', params, HTTP_X_USER_ID='1')

    assert response.status_code == 400

