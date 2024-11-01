from datetime import datetime, timedelta

from _pytest.fixtures import fixture
from django.conf import settings
from django.test.client import Client
from django.urls import reverse

from products.models import Subcategory, Category


@fixture
def category():
    return Category.objects.create(
        name=f'Наптики',
        slug=f'drinks',
        image=f'store',
    )

@fixture
def subcategory_list(category):
    return Subcategory.objects.bulk_create(
        Subcategory(
            name=f'Кофе-{index}',
            slug=f'coffee-{index}',
            image=f'file-{index}',
            category_id=category.id,
        ) for index in range(settings.COUNT_ON_HOME_PAGE + 1)
    )

@fixture
def subcategory_url():
    return reverse('api:subcategory-list')

@fixture
def category_url():
    return reverse('api:category-list')

@fixture
def product_url():
    return reverse('api:product-list')
