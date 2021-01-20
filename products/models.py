from django.utils import timezone
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.db import models
from django.db.models import CASCADE, Model
from django.contrib.auth import get_user_model
from django.urls import reverse

User = get_user_model()

# Create your models here.
'''
ТВ (
Телевізори, 
аудіосистема, 
тюнери проектори
)
'''


def get_models_for_count(*model_names):
    return [models.Count(model_name) for model_name in model_names]


def get_product_url(obj, viewname):
    ct_model = obj.__class__._meta.model_name
    return reverse(viewname, kwargs={'ct_model': ct_model, 'slug': obj.slug})


class CartProduct(models.Model):
    user = models.ForeignKey('Customer', verbose_name='Покупець', on_delete=models.CASCADE)
    cart = models.ForeignKey('Cart', verbose_name='Корзина', on_delete=models.CASCADE, related_name='related_products')
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')
    qty = models.PositiveIntegerField(default=1)
    final_price = models.DecimalField(max_digits=9, decimal_places=2, verbose_name='Загальна ціна')

    def __str__(self):
        return "Продукт: {} (для корзини)".format(self.content_object.title)

    def save(self, *args, **kwargs):
        self.final_price = self.qty * self.content_object.price
        super().save(*args, **kwargs)


class Cart(models.Model):
    owner = models.ForeignKey('Customer', null=True, verbose_name='Власник', on_delete=models.CASCADE)
    products = models.ManyToManyField(CartProduct, blank=True, related_name='related_cart')
    total_products = models.PositiveIntegerField(default=0)
    final_price = models.DecimalField(max_digits=9, default=0, decimal_places=2, verbose_name='Загальна ціна')
    in_order = models.BooleanField(default=False)
    for_anonymous_user = models.BooleanField(default=False)

    def __str__(self):
        return str(self.id)


class Customer(models.Model):
    user = models.ForeignKey(User, verbose_name='Користувач', on_delete=models.CASCADE)
    phone = models.CharField(max_length=20, verbose_name='Номер телефону', null=True, blank=True)
    address = models.CharField(max_length=255, verbose_name='Адреса', null=True, blank=True)
    orders = models.ManyToManyField('Order', verbose_name='Замовлення покупця', related_name='related_order')

    def __str__(self):
        return "Покупець: {} {}".format(self.user.first_name, self.user.last_name)


class LatestProductsManager:

    @staticmethod
    def get_products_for_main_page(*args, **kwargs):
        with_respect_to = kwargs.get('with_respect_to')
        products = []
        ct_models = ContentType.objects.filter(model__in=args)
        for ct_model in ct_models:
            model_products = ct_model.model_class()._base_manager.all().order_by('-id')[:5]
            products.extend(model_products)
        if with_respect_to:
            ct_model = ContentType.objects.filter(model=with_respect_to)
            if ct_model.exists():
                if with_respect_to in args:
                    return sorted(
                        products, key=lambda x: x.__class__._meta.model_name.startswith(with_respect_to), reverse=True
                    )
        return products


class LatestProducts:
    objects = LatestProductsManager()


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
    battery_lifetime = models.PositiveSmallIntegerField(verbose_name="Час автономної роботи, години", null=True)
    battery_capacity = models.PositiveSmallIntegerField(verbose_name="Ємність батареї, mAh", null=True)

    def __str__(self):
        return "{} {}".format(self.fk_brand, self.model)


class PersonalComputer(Product):
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


class Tablet(Product):
    display = models.CharField(verbose_name="Діагональ", max_length=5)
    rom_capacity = models.PositiveSmallIntegerField(verbose_name="Об'єм пам'яті, Гб")
    ram_capacity = models.PositiveSmallIntegerField(verbose_name="Об'єм оперативної пам'яті, Гб")
    is_front_cam = models.BooleanField(verbose_name="Наявність фронтальної камери")
    front_cam = models.PositiveSmallIntegerField(verbose_name="МП", null=True)
    is_back_cam = models.BooleanField(verbose_name="Наявність задня камери")
    back_cam = models.PositiveSmallIntegerField(verbose_name="МП", null=True)
    is_sd = models.BooleanField(verbose_name="Підтримка SD карт")
    sd = models.PositiveSmallIntegerField(verbose_name="Максимальний обсяг SD карти", null=True)
    battery_lifetime = models.PositiveSmallIntegerField(verbose_name="Час автономної роботи, години", null=True)
    battery_capacity = models.PositiveSmallIntegerField(verbose_name="Ємність батареї, mAh", null=True)

    def __str__(self):
        return "{} {}".format(self.fk_brand, self.model)


class Smartphone(Product):
    display = models.CharField(verbose_name="Діагональ", max_length=5)
    rom_capacity = models.PositiveSmallIntegerField(verbose_name="Об'єм пам'яті, Гб")
    ram_capacity = models.PositiveSmallIntegerField(verbose_name="Об'єм оперативної пам'яті, Гб")
    is_front_cam = models.BooleanField(verbose_name="Наявність фронтальної камери")
    front_cam = models.PositiveSmallIntegerField(verbose_name="МП", null=True)
    is_back_cam = models.BooleanField(verbose_name="Наявність задня камери")
    back_cam = models.PositiveSmallIntegerField(verbose_name="МП", null=True)
    is_sd = models.BooleanField(verbose_name="Підтримка SD карт")
    sd = models.PositiveSmallIntegerField(verbose_name="Максимальний обсяг SD карти", null=True)
    battery_lifetime = models.PositiveSmallIntegerField(verbose_name="Час автономної роботи, години", null=True)
    battery_capacity = models.PositiveSmallIntegerField(verbose_name="Ємність батареї, mAh", null=True)

    def __str__(self):
        return "{} {}".format(self.fk_brand, self.model)


class TVset(Product):
    pass


class Order(models.Model):
    STATUS_NEW = 'new'
    STATUS_IN_PROGRESS = 'in_progress'
    STATUS_READY = 'is_ready'
    STATUS_COMPLETED = 'completed'

    BUYING_TYPE_SELF = 'self'
    BUYING_TYPE_DELIVERY = 'delivery'

    STATUS_CHOICES = (
        (STATUS_NEW, 'Нове замовлення'),
        (STATUS_IN_PROGRESS, 'Замовлення обробляється'),
        (STATUS_READY, 'Замовлення готове'),
        (STATUS_COMPLETED, 'Замовлення виконане')
    )

    BUYING_TYPE_CHOICES = (
        (BUYING_TYPE_SELF, 'Самовивіз'),
        (BUYING_TYPE_DELIVERY, 'Доставка')
    )

    customer = models.ForeignKey(Customer, verbose_name='Покупець', related_name='related_orders', on_delete=CASCADE)
    first_name = models.CharField(max_length=255, verbose_name="Ім'я")
    last_name = models.CharField(max_length=255, verbose_name='Прізвище')
    phone = models.CharField(max_length=20, verbose_name='Телефон')
    cart = models.ForeignKey(Cart, verbose_name='Корзина', on_delete=models.CASCADE, null=True, blank=True)
    address = models.CharField(max_length=1024, verbose_name='Адреса', null=True, blank=True)
    status = models.CharField(
        max_length=100,
        verbose_name='Статус замовлення',
        choices=STATUS_CHOICES,
        default=STATUS_NEW
    )
    buying_type = models.CharField(
        max_length=100,
        verbose_name='Тип замовлення',
        choices=BUYING_TYPE_CHOICES,
        default=BUYING_TYPE_SELF
    )
    comment = models.TextField(verbose_name='Коментарій для замовлення', null=True, blank=True)
    created_at = models.DateTimeField(auto_now=True, verbose_name='Дата создания заказа')
    order_date = models.DateField(verbose_name='Дата получения заказа', default=timezone.now)

    def __str__(self):
        return str(self.id)
