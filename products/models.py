from django.db import models
from django.db.models import CASCADE, Model

# Create your models here.
'''
Brand 
Комп'ютери (
ноутбуки, 
пк, 
планшети
)
Телефони (
смартфони
) 
Побутова техніка (
навушники
холодильники, 
морозильні камери, 
витяжки, 
пралка, 
посудомийка
)
ТВ (
Телевізори, 
аудіосистема, 
тюнери проектори
)
'''


class Category(Model):
    name = models.CharField(verbose_name="Назва категорії", max_length=250)
    slug = models.CharField(verbose_name="Посилання", max_length=250)

    def __str__(self):
        return self.name


class SubCategory(Model):
    fk = models.ForeignKey(Category, verbose_name="Категорія", on_delete=CASCADE)
    name = models.CharField(verbose_name="Назва підкатегорії", max_length=250)
    slug = models.CharField(verbose_name="Посилання", max_length=250)

    def __str__(self):
        return self.name


class Brand(Model):
    name = models.CharField(verbose_name="Назва бренду", max_length=15)

    def __str__(self):
        return self.name


class Product(models.Model):
    class Meta:
        abstract = True

    category = models.ForeignKey(SubCategory, verbose_name='Категорія', on_delete=models.CASCADE, null=True)
    fk_brand = models.ForeignKey(Brand, verbose_name="Бренд", on_delete=CASCADE)
    model = models.CharField(verbose_name="Модель", max_length=25)
    slug = models.SlugField(unique=True, null=True)
    img = models.ImageField(verbose_name="Зображення")
    description = models.TextField(verbose_name='Опис', null=True)
    price = models.DecimalField(max_digits=9, decimal_places=2, verbose_name='Ціна', null=True)

    def __str__(self):
        return self.model

    def get_model_name(self):
        return self.__class__.__name__.lower()


class Notebook(Product):
    display = models.CharField(verbose_name="Діагональ", max_length=5)
    rom_types = (
        ('HDD', 'HDD'),
        ('SSD', 'SSD'),
        ('HSD', 'HDD + SSD'),
    )
    rom = models.CharField(choices=rom_types, verbose_name="Тип пам'яті", max_length=10)
    rom_capacity = models.PositiveSmallIntegerField(verbose_name="Об'єм пам'яті, Гб")
    ram_types = (
        ('DDR2', 'DDR2'),
        ('DDR3', 'DDR3'),
        ('DDR4', 'DDR4'),
    )
    ram = models.CharField(choices=ram_types, verbose_name="Тип оперативної пам'яті", max_length=10)
    ram_capacity = models.PositiveSmallIntegerField(verbose_name="Об'єм оперативної пам'яті, Гб")

    def __str__(self):
        return "{} {}".format(self.fk_brand, self.model)
