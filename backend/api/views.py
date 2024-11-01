from django.db.models import Sum
from django.shortcuts import get_object_or_404
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from products.models import (
    Category,
    Subcategory,
    Product,
    ShoppingCart
)
from .serializers import (
    CategorySerializer,
    SubcategorySerializer,
    ProductSerializer,
    ShopCardCreateSerializer,
    ShopCartSerializer
)


class CategoryViewSet(viewsets.ReadOnlyModelViewSet):
    """Вьюсет для отображения категорий."""

    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class SubcategoryViewSet(viewsets.ReadOnlyModelViewSet):
    """Вьюсет для отображения подкатегорий."""

    queryset = Subcategory.objects.all().select_related('category')
    serializer_class = SubcategorySerializer


class ProductViewSet(viewsets.ReadOnlyModelViewSet):
    """Вьюсет для отображения продуктов."""

    queryset = Product.objects.all().select_related('subcategory')
    serializer_class = ProductSerializer

    @action(
        detail=True,
        methods=('post',),
        serializer_class=ShopCardCreateSerializer,
        permission_classes=(IsAuthenticated,)
    )
    def shopping_cart(self, request, pk=None):
        serializer = self.get_serializer(
            data=request.data,
            context={'request': request, 'product_id': pk}
        )
        serializer.is_valid(raise_exception=True)
        serializer.save(id=pk)
        return Response(
            serializer.data,
            status=status.HTTP_201_CREATED
        )

    @shopping_cart.mapping.delete
    def delete_shopping_cart(self, request, pk=None):
        delete_status, _ = ShoppingCart.objects.filter(
            user=request.user,
            product=get_object_or_404(Product, pk=pk).pk
        ).delete()
        return Response(
            'Продукт удален',
            status=status.HTTP_204_NO_CONTENT
            if delete_status
            else status.HTTP_400_BAD_REQUEST
        )


class ShoppingCartViewSet(viewsets.ReadOnlyModelViewSet):
    """Вьюсет для отображения корзины с продуктами."""

    permission_classes = (IsAuthenticated,)
    serializer_class = ShopCartSerializer

    def get_queryset(self):
        return ShoppingCart.objects.filter(
            user=self.request.user,
        ).select_related(
            'user',
            'product',
        )

    def list_shopping_cart(self, request):
        queryset = self.filter_queryset(self.get_queryset())
        serializer = self.get_serializer(queryset, many=True)
        data = serializer.data
        total_products = len(data)
        total_sum = Sum(
            item.get('price', 0) * item.get('amount', 0) for item in data
        )
        return Response(
            data={
                'total_products': total_products,
                'total_sum': total_sum,
                'products': data
            },
            status=status.HTTP_200_OK,
        )

    @action(
        methods=('post',),
        detail=False,
        url_name='clear_shopping_cart',
    )
    def clear_shopping_cart(self, request):
        ShoppingCart.objects.filter(
            user==request.user
        ).delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
