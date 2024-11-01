from rest_framework import serializers
from django.shortcuts import get_object_or_404

from .constants import MIN_VALUE
from products.models import (
    Category,
    Subcategory,
    Product,
    ShoppingCart
)


class CategorySerializer(serializers.ModelSerializer):
    """Сериализатор категории."""

    class Meta:
        model = Category
        fields = '__all__'


class SubcategorySerializer(serializers.ModelSerializer):
    """Сериализатор подкатегории."""

    class Meta:
        model = Subcategory
        fields = '__all__'


class ShortSubcategorySerializer(serializers.ModelSerializer):
    """Сериализатор сокращенного отображения подкатегорий."""

    category = serializers.CharField(source='category.name')

    class Meta:
        model = Subcategory
        fields = (
            'id',
            'name',
            'category',
        )


class ProductSerializer(serializers.ModelSerializer):
    """Сериализатор подкатегории."""

    subcategory = SubcategorySerializer()

    class Meta:
        model = Product
        fields = '__all__'


class ShortProductSerializer(serializers.ModelSerializer):
    """Сериализатор сокращенного отображения продуктов."""

    subcategory = SubcategorySerializer()

    class Meta:
        model = Product
        fields = (
            'id',
            'name',
            'slug',
            'price',
        )


class ShopCartSerializer(serializers.ModelSerializer):
    """Сериализатор корзины."""

    product = serializers.CharField(source='product.name')
    price = serializers.IntegerField(source='product.price')
    amount = serializers.IntegerField(min_value=MIN_VALUE)

    class Meta:
        model = ShoppingCart
        fields = (
            'product',
            'price',
            'amount',
        )


class ShopCardCreateSerializer(serializers.ModelSerializer):
    """Сериализатор создания корзины."""

    user = serializers.ReadOnlyField()
    product = serializers.ReadOnlyField()

    class Meta:
        model = ShoppingCart
        fields = (
            'user',
            'product',
            'amount'
        )

    def validate(self, data):
        model = self.Meta.model
        product_id = self.context['product_id']
        if model.objects.filter(
            user=data['user'],
            product=product_id,
        ).exists():
            raise serializers.ValidationError(
                {f'{model._meta.verbose_name} error': 'Продукт уже добавлен'}
            )
        return data

    def create(self, validated_data):
        product = get_object_or_404(Product, pk=validated_data['id'])
        ShoppingCart.objects.create(
            user=self.context['request'].user,
            product=product,
            amount=validated_data['amount'],
        )
        serializer = ShortProductSerializer(product)
        return serializer.data
