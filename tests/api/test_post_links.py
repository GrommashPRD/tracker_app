import pytest

from rest_framework.test import APIClient
from tracker_app.utils import linksParser

client = APIClient()

@pytest.mark.django_db
def test_add_links():
    links_data = {
        "urls": [
            "https://ya.ru/",
            "https://ya.ru/search/?text=мемы+с+котиками",
            "https://sber.ru",
            "https://stackoverflow.com/questions/65724760/how-it-is"
        ]
    }

    response = client.post('/visited_links', data=links_data, format='json', HTTP_X_USER_ID='1')
    assert {'status': 'ok'} == response.data
    assert response.status_code == 200

def test_with_no_user():
    links_data = {
        "urls": [
            "https://ya.ru/",
            "https://ya.ru/search/?text=мемы+с+котиками",
            "https://sber.ru",
            "https://stackoverflow.com/questions/65724760/how-it-is"
        ]
    }

    response = client.post('/visited_links', data=links_data, format='json')

    assert response.status_code == 403

def test_wrong_body():
    links_data = {
        "urlz": [
            "https://ya.ru/",
            "https://ya.ru/search/?text=мемы+с+котиками",
            "https://sber.ru",
            "https://stackoverflow.com/questions/65724760/how-it-is"
        ]
    }

    response = client.post('/visited_links', data=links_data, format='json', HTTP_X_USER_ID='1')

    assert response.status_code == 400

def test_unique_domains():
    expected_domains = {'ya.ru', 'sber.ru', 'stackoverflow.com'}
    urls =  [
        "https://ya.ru/",
        "https://ya.ru/search/?text=мемы+с+котиками",
        "https://sber.ru",
        "https://stackoverflow.com/questions/65724760/how-it-is"
    ]

    domains = linksParser.get_unique_domains(urls)
    assert set(domains) == expected_domains

