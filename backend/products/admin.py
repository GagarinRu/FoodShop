from django.contrib import admin
from django.contrib.auth.models import Group
from django.utils.safestring import mark_safe
from rest_framework.authtoken.models import TokenProxy


from .models import (
    Category,
    Subcategory,
    Product,
    ShoppingCart
)


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = (
        'name',
        'slug',
        'subcategory',
        'price',
    )
    list_display_links = (
        'name',
    )
    list_editable = (
        'subcategory',
    )
    search_fields = (
        'name',
    )
    list_filter = (
        'subcategory',
    )
    readonly_fields = ('products_photo',)

    @admin.display(description='Изображение')
    def products_photo(self, product):
        if product.image:
            return mark_safe(
                f'<img src={product.image.url} width="80" height="60">'
            )
        return 'Не задано'


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = (
        'name',
        'slug',
    )
    search_fields = ('name',)
    empty_value_display = 'Не задано'


@admin.register(Subcategory)
class SubcategoryAdmin(admin.ModelAdmin):
    list_display = (
        'name',
        'slug',
    )
    search_fields = ('name',)
    empty_value_display = 'Не задано'


@admin.register(ShoppingCart)
class ShoppingCartAdmin(admin.ModelAdmin):
    list_display = ('user', 'product')
    empty_value_display = 'Нет Информации'


admin.site.empty_value_display = 'Не задано'

admin.site.unregister(Group)
admin.site.unregister(TokenProxy)
admin.site.empty_value_display = 'Не задано'
