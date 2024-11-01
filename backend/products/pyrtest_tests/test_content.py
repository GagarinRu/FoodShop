import json
from http import HTTPStatus

from pytest import mark
from django.conf import settings
from pytest_lazyfixture import lazy_fixture


pytestmark = mark.django_db

SUBCATEGORY_URL = lazy_fixture('subcategory_url')
CATEGORY_URL = lazy_fixture('category_url')
PRODUCT_URL = lazy_fixture('product_url')
CLIENT = lazy_fixture('client')


@mark.parametrize(
    'url, parametrized_client, expected_status',
    (
        (
            SUBCATEGORY_URL,
            CLIENT,
            HTTPStatus.OK
        ),
        (
            CATEGORY_URL,
            CLIENT,
            HTTPStatus.OK
        ),
        (
            PRODUCT_URL,
            CLIENT,
            HTTPStatus.OK
        ),
    )
)
@mark.django_db
def test_pages_availability_for_anonymous_user(
    parametrized_client,
    url,
    expected_status
):
    """Доступность страниц для различных пользователей."""
    assert parametrized_client.get(url).status_code == expected_status


def test_subcategory_in_list(subcategory_list, client, subcategory_url):
    """Количество новостей на странице подкатегорий — не более 10."""
    response = client.get(subcategory_url)
    assert response.status_code == HTTPStatus.OK
    object_list = response.context['object_list']
    subcategory_count = len(object_list)
    assert subcategory_count == settings.COUNT_ON_HOME_PAGE

