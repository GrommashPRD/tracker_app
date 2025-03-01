import pytest

from tracker_app.models import UserDomainsHistory
from rest_framework.test import APIClient

client = APIClient()


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

def test_green_test(start,
               end,
               expected_domains
):
    domain_test_1 = UserDomainsHistory.objects.create(user_id='1', domain='ya.ru', created_at=123)
    domain_test_2 = UserDomainsHistory.objects.create(user_id='1', domain='ya.ru', created_at=124)
    domain_test_3 = UserDomainsHistory.objects.create(user_id='1', domain='test.ru', created_at=124)

    response = client.get('/visited_domains', {'start': start, 'end': end}, HTTP_X_USER_ID='1')

    assert response.status_code == 200
    assert set(response.data['domains']) == expected_domains

def test_no_domains():
    response = client.get('/visited_domains', {'start': 1, 'end': 2})

    assert response.status_code == 403


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

def test_wrong_params(
        start,
        end
):
    params = {}
    if start:
        params['start'] = start
    if end:
        params['end'] = end
    response = client.get('/visited_domains', params, HTTP_X_USER_ID='1')

    assert response.status_code == 400