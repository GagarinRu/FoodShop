from csv import DictReader

from django.contrib.auth import get_user_model
from django.core.management import BaseCommand
from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand
from django.utils.crypto import get_random_string

from products.models import Product, Category, Subcategory


User = get_user_model()

TABLES_DICT = {
    Category: 'category.csv',
    Subcategory: 'subcategory.csv',
    Product: 'products.csv',
}


class Command(BaseCommand):
    help = 'Загрузка данных из csv файлов'

    def handle(self, *args, **options):
        for model_name, file_name in TABLES_DICT.items():
            try:
                with open(
                    f'./data/{file_name}',
                    encoding='utf-8'
                ) as csv_file:
                    data_list = []
                    data = DictReader(csv_file)
                    for row_data in data:
                        data_list.append(model_name(**row_data))
                    model_name.objects.bulk_create(data_list)
            except Exception as error:
                self.stdout.write(self.style.ERROR(f'{error}'))
        username = 'admin'  
        email = 'admin@example.com'  
        try:  
            u = None  
            if not User.objects.filter(username=username).exists() and not User.objects.filter(  
                is_superuser=True).exists():  
                print("Суперюзер, создайте одного!")  
                new_password = get_random_string()
                u = User.objects.create_superuser(username, email, new_password)  
                print(f'Суперюзер "{username}" был создан с почтой "{email}" паролем "{new_password}"')  
            else:  
                print('Суперюзер найден, процедура создания пропущена!')  
        except Exception as e:  
            self.stdout.write(self.style.ERROR(f'Была вызвана ошибка: {e}'))
        self.stdout.write(self.style.SUCCESS('Загрузка данных завершена'))
