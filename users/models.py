from uuid import uuid4

from django.contrib.auth import get_user
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager
from django.db import models

from users.base_model import BaseModel
from users import const 
from decimal import Decimal


User = get_user()


class UserProfileManager(BaseUserManager):

    def create_user(self, email, password, **kwargs):
        if not email:
            raise ValueError('Email not provided')
        user = self.model(email=self.normalize_email(email), **kwargs)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email, password):
        user = self.create_user(email=email, password=password)
        user.is_superuser = True
        user.is_staff = True
        user.is_active = True
        user.save()
        return user


class UserProfile(AbstractBaseUser, PermissionsMixin):
    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    email = models.EmailField('Адрес электронной почты', unique=True)
    first_name = models.CharField('Имя', max_length=const.FIRST_NAME_MAX_LEN)
    last_name = models.CharField('Фамилия', max_length=const.LAST_NAME_MAX_LEN)
    patronymic = models.CharField(
        'Отчество',
        max_length=const.PATRONYMIC_MAX_LEN,
        blank=True,
        null=True
    )
    unp = models.CharField(
        'Учетный номер плательщика',
        max_length=const.PAYER_ACCOUNT_NUMBER_MAX_LEN,
        blank=True,
        null=True
    )
    registration_address = models.CharField(
        'Адрес регистрации',
        max_length=const.ADDRESS_MAX_LEN,
        blank=True,
        null=True
    )
    residential_address = models.CharField(
        'Адрес проживания',
        max_length=const.ADDRESS_MAX_LEN,
        blank=True,
        null=True
    )
    avatar = models.ImageField(upload_to='users_avatars', null=True, blank=True)
    date_of_birth = models.DateField(blank=True, null=True)
    secret_word = models.CharField(blank=True, null=True)
    created_at = models.DateField(auto_now_add=True)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=False)
    is_admin = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'
    objects = UserProfileManager()

    @property
    def is_npd_payer(self):
        return bool(self.unp)

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

    def __str__(self):
        return f'User(email={self.email}, is_active={self.is_active})'


class SignupSession(BaseModel):
    email = models.EmailField()
    confirm_code = models.PositiveIntegerField()
    expiration_time = models.DateTimeField()

    def __str__(self):
        return f'SighupSession(email={self.email}, confirm_code={self.confirm_code})'


class ProductCategory(BaseModel):
    name = models.CharField(
        'Наименование категории товара',
        max_length=const.CATEGOTY_NAME_MAX_LEN
    )

    class Meta:
        verbose_name = 'Категория продукта'
        verbose_name_plural = 'Категории продуктов'

    def __str__(self):
        return self.name[:30]


class Product(BaseModel):
    name = models.CharField('Наименование товара', max_length=const.PRODUCT_NAME_MAX_LEN)
    description = models.CharField('Описание товара', max_length=const.PRODUCT_DESCRIP_MAX_LEN)
    price = models.DecimalField('Стоимость товара', max_digits=10, decimal_places=2)
    count = models.PositiveIntegerField(
        'Количество товара в наличии',
        null=True,
        blank=True
    )
    #TODO not sure: 1 to many or many to many?
    category = models.ForeignKey(ProductCategory, on_delete=models.CASCADE)
    seller = models.ForeignKey(User, on_delete=models.CASCADE)

    class Meta:
        verbose_name = 'Товар'
        verbose_name_plural = 'Товары'
        default_related_name = 'products'

    def __str__(self):
        return self.name[:30]


class ServiceCategory(BaseModel):
    name = models.CharField(
        'Наименование категории услуги',
        max_length=const.CATEGOTY_NAME_MAX_LEN
    )

    def __str__(self):
        return self.name[:30]


class Service(BaseModel):
    name = models.CharField('Наименование услуги', max_length=const.SERVICE_NAME_MAX_LEN)
    service_description = models.CharField('Описание услуги', max_length=const.SERVICE_DESCRIP_MAX_LEN)
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Стоимость услуги')
    #TODO not sure: 1 to many or many to many?
    category = models.ForeignKey(ProductCategory, on_delete=models.CASCADE)
    seller = models.ForeignKey(User, on_delete=models.CASCADE)

    class Meta:
        verbose_name = 'Услуга'
        verbose_name_plural = 'Услуги'
        default_related_name = 'services'

    def __str__(self):
        return self.name


#class Activities(models.Model):
#    name = models.CharField(max_length=255, verbose_name="Вид деятельности")
#    product = models.ForeignKey(Product, on_delete=models.CASCADE)
#    service = models.ForeignKey(Service, on_delete=models.CASCADE)
#
#    def __str__(self):
#        return self.name


class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.PROTECT)
    products = models.ManyToManyField(Product, through="OrderItem")
    order_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Заказ {self.id}"

    def get_total_cost(self):
        total_cost = sum(item.get_cost() for item in self.items.all())
        return total_cost - total_cost * (self.discount / Decimal('100'))


class OrderItem(models.Model):
    order = models.ForeignKey(Order, related_name="items", on_delete=models.CASCADE)
    product = models.ForeignKey(Product, related_name="order_items", on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(verbose_name="Количество", default=1)
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Стоимость товара")
    service = models.ForeignKey(Service, on_delete=models.CASCADE)

    def __str__(self):
        return f"Заказ {self.order.id}, товар {self.product}"


class Review(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="reviews")
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField(verbose_name="Текст отзыва")
    rating = models.PositiveIntegerField(verbose_name="Рейтинг")

    def __str__(self):
        return f"Отзыв на товар {self.product.name}"
