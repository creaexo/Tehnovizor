from django.contrib.auth import get_user_model
from django.db import models
from django.urls import reverse
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey
from django.utils import timezone

User = get_user_model()
# Create your models here.
def get_product_url(obj):
    return f"{obj.category.slug}/{obj.slug}"
class Category(models.Model):
    slug = models.SlugField(max_length=100, auto_created=True)
    name = models.CharField(max_length=100, verbose_name='Название категории')

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = ' Категории'

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('category_detail', kwargs={'slug': self.slug})


class Dish(models.Model):


    category = models.ForeignKey(Category, verbose_name='Категория', on_delete=models.CASCADE)
    title = models.CharField(max_length=255, verbose_name='Наименование')
    slug = models.SlugField(unique=True)
    image1 = models.ImageField(verbose_name='Изображение 1', blank=True)
    image2 = models.ImageField(verbose_name='Изображение 2', blank=True)
    image3 = models.ImageField(verbose_name='Изображение 3', blank=True)
    vegan = models.BooleanField(verbose_name="Веган-блюдо", default=False)
    in_stock = models.BooleanField(verbose_name="В наличии", default=True)
    weight = models.DecimalField(verbose_name='Вес',max_digits=5, decimal_places=2, blank=True)
    calories = models.DecimalField(verbose_name='Калории',max_digits=5, decimal_places=1, blank=True)
    proteins = models.DecimalField(verbose_name='Белки',max_digits=5, decimal_places=1, blank=True)
    fats = models.DecimalField(verbose_name='Жиры',max_digits=5, decimal_places=1, blank=True)
    carb = models.DecimalField(verbose_name='Углеводы',max_digits=5, decimal_places=1, blank=True)
    description = models.TextField(verbose_name='Описание', blank=True)
    price = models.DecimalField(verbose_name='Цена',max_digits=5, decimal_places=2)

    def get_product_url(obj):
        return f"{obj.category.slug}/{obj.slug}"
    def __str__(self):
        return self.title

    def get_model_name(self):
        return self.__class__.__name__.lower()

    class Meta:
        verbose_name = 'Блюдо'
        verbose_name_plural = ' Блюда'

class Employee(models.Model):
    user = models.ForeignKey(User, verbose_name='Пользователь', on_delete=models.CASCADE)
    phone = models.CharField(max_length=20, verbose_name='Номер телефона', null=True, blank=True)
    orders = models.ManyToManyField('Order', verbose_name='Заказы покупателя', related_name='related_order')
    USERNAME_FIELD = "username"

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

    def __str__(self):
        return f"Покупатель: {self.user.first_name} {self.user.last_name}"


class CartDish(models.Model):
    user = models.ForeignKey(Employee, on_delete=models.CASCADE, verbose_name="Покупатель")
    cart = models.ForeignKey('Cart', on_delete=models.CASCADE, verbose_name="Корзина", related_name='related_products')
    dish = models.ForeignKey(Dish, verbose_name='Блюдо', related_name="dishes", on_delete=models.CASCADE, default=1)
    # content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE, verbose_name='Пренадлежность к категориям')
    object_id = models.PositiveIntegerField(verbose_name='ID товара')
    # content_object = GenericForeignKey('content_type', 'object_id')
    qty = models.PositiveIntegerField(default=1, verbose_name='Количество единиц товара')
    final_price = models.DecimalField(max_digits=9, decimal_places=2, verbose_name='Общая цена')
    glist = models.TextField(verbose_name="Параметры", default='')
    in_order = models.BooleanField(verbose_name="В заказе", default=False)
    class Meta:
        verbose_name = 'Продукт в корзине'
        verbose_name_plural = 'Продукты в корзине'

    def __str__(self):
        return "Продукт: {} (для корзины)".format(self.dish.title)

    def save(self, *args, **kwargs):
        self.final_price = self.qty * self.dish.price
        super().save(*args, **kwargs)


class Cart(models.Model):

    owner = models.ForeignKey(Employee, null=True, verbose_name='Владелец', on_delete=models.CASCADE)
    products = models.ManyToManyField(CartDish, blank=True, related_name='related_cart', verbose_name='Продукты')
    total_products = models.PositiveIntegerField(default=0, verbose_name='Количество продуктов')
    final_price = models.DecimalField(max_digits=9, default=0, decimal_places=2, verbose_name='Общая цена')
    in_order = models.BooleanField(default=False, verbose_name='Заказан')
    # for_anonymous_user = models.BooleanField(default=False, verbose_name='От анонимного покупателя')

    class Meta:
        verbose_name = 'Корзина'
        verbose_name_plural = 'Корзины'

    def __str__(self):
        return str(self.id)
    # print(products.id)
    # def get_nominations(self):
    #     nomination_list = self.products
    #     nominations_str = ''
    #     for nomination in nomination_list:
    #         nominations_str += ', ' + nomination.title
    #     return nominations_str.lstrip(', ')
class Order(models.Model):

    STATUS_CANSEL = 'cansel'
    STATUS_IN_PROGRESS = 'in_progress'
    STATUS_READY = 'is_ready'

    BUYING_TYPE_SELF = 'self'
    BUYING_TYPE_DELIVERY = 'delivery'

    STATUS_CHOICES = (
        (STATUS_CANSEL, 'Отмена'),
        (STATUS_IN_PROGRESS, 'Заказ в обработке'),
        (STATUS_READY, 'Заказ готов')
    )

    BUYING_TYPE_CHOICES = (
        (BUYING_TYPE_SELF, 'В столовой'),
        (BUYING_TYPE_DELIVERY, 'Доставить на рабочее место')
    )

    employee = models.ForeignKey(Employee, verbose_name='Покупатель', related_name='related_orders', on_delete=models.CASCADE)
    cart = models.ForeignKey(Cart, verbose_name='Корзина', on_delete=models.CASCADE, null=True, blank=True)
    # final_price = models.DecimalField(max_digits=9, default=0, decimal_places=2, verbose_name='Общая цена')
    status = models.CharField(
        max_length=100,
        verbose_name='Статус заказ',
        choices=STATUS_CHOICES,
        default=STATUS_IN_PROGRESS
    )
    buying_type = models.CharField(
        max_length=100,
        verbose_name='Тип заказа',
        choices=BUYING_TYPE_CHOICES,
        default=BUYING_TYPE_SELF
    )
    comment = models.TextField(verbose_name='Комментарий к заказу', null=True, blank=True)
    products_information = models.TextField(verbose_name='Информация о товарах', null=True, blank=True)
    created_at = models.DateTimeField(auto_now=True, verbose_name='Дата создания заказа')
    order_date = models.DateField(verbose_name='Дата получения заказа', default=timezone.now, null=True, blank=True)
    order_time = models.TimeField(verbose_name='Дата получения заказа', default=timezone.now, null=True, blank=True)

    def __str__(self):
        return str(self.id)


    class Meta:
        verbose_name = '    Заказ'
        verbose_name_plural = '         Заказы'