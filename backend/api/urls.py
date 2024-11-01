from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import (
    CategoryViewSet,
    ProductViewSet,
    ShoppingCartViewSet,
    SubcategoryViewSet,
)


app_name = 'api'

router = DefaultRouter()
router.register(
    r'product',
    ProductViewSet,
    basename='product'
)
router.register(
    r'category',
    CategoryViewSet,
    basename='category'
)
router.register(
    r'subcategory',
    SubcategoryViewSet,
    basename='subcategory'
)
router.register(
    'shoppingcart',
    ShoppingCartViewSet,
    basename='shoppingcart'
)


urlpatterns = [
    path(
        '',
        include(router.urls)
    ),
    path(
        'auth/',
        include('djoser.urls.authtoken')
    ),
    path(
        'api-auth/',
        include('rest_framework.urls', namespace='rest_framework')
    ),
]
