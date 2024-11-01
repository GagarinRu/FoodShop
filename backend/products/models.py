from django.contrib.auth import get_user_model
from django.db import models

from .constants import (DEICMAL_PLACES, MAX_DIGITALS, NAME_LEN,
                        SLUG_LEN, SLICE_LENGTH)


User = get_user_model()


class GeneralModel(models.Model):
    name = models.CharField(
        verbose_name='Название',
        max_length=NAME_LEN,
    )
    slug = models.SlugField(
        verbose_name='Идентификатор',
        max_length=SLUG_LEN,
        unique=True,
    )
    image = models.ImageField(
        verbose_name='Картинка',
        upload_to='shopfood/images/',
    )

    class Meta:
        abstract = True

    def __str__(self):
        return self.name[:SLICE_LENGTH]


class Category(GeneralModel):
    """Модель категории."""

    class Meta:
        ordering = ('name',)
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'

    def __str__(self):
        return self.name[:SLICE_LENGTH]


class Subcategory(GeneralModel):
    """Модель подкатегории."""

    category = models.ForeignKey(
        Category,
        verbose_name='Категория',
        on_delete=models.CASCADE,
    )

    class Meta:
        ordering = ('name',)
        verbose_name = 'Подкатегория'
        verbose_name_plural = 'Подкатегории'

    def __str__(self):
        return self.name[:SLICE_LENGTH]


class Product(GeneralModel):
    """Модель продукта."""

    price = models.DecimalField(
        verbose_name='Стоимость продукта',
        max_digits=MAX_DIGITALS,
        decimal_places=DEICMAL_PLACES
    )
    image_medium_size = models.ImageField(
        verbose_name='Средняя картинка продкукта',
        upload_to='shopfood/images/',
    )
    image_big_size = models.ImageField(
        verbose_name='Большая картинка продкукта',
        upload_to='shopfood/images/',
    )
    subcategory = models.ForeignKey(
        Subcategory,
        verbose_name='Подкатегория',
        on_delete=models.CASCADE,
    )

    class Meta:
        verbose_name = 'Продукт'
        verbose_name_plural = 'Продукты'
        ordering = ('name',)

    def __str__(self):
        return self.name[:SLICE_LENGTH]


class UserProduct(models.Model):
    user = models.ForeignKey(
        User,
        verbose_name='Пользователь',
        on_delete=models.CASCADE,
    )
    product = models.ForeignKey(
        Product,
        verbose_name='Продукт',
        on_delete=models.CASCADE,
    )

    class Meta:
        abstract = True
        constraints = (
            models.UniqueConstraint(
                fields=('user', 'product',),
                name='unique_%(class)s',
            ),
        )

    def __str__(self):
        return (
            f'{self.product}'
            f'{self.user}'
        )[:SLICE_LENGTH]


class ShoppingCart(UserProduct):
    """Модель для пользовательской корзины."""

    amount = models.PositiveIntegerField(
        verbose_name='Количество продуктов',
    )

    class Meta(UserProduct.Meta):
        verbose_name = 'Список Покупок'
        verbose_name_plural = 'Списки Покупок'
        default_related_name = 'shoppingcart_set'
