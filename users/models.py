from uuid import uuid4

from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager
from django.db import models

from users.const import (PAYER_ACCOUNT_NUMBER_MAX_LEN, FIRST_NAME_MAX_LEN,
                         LAST_NAME_MAX_LEN, PATRONYMIC_MAX_LEN)
from decimal import Decimal


class UserProfileManager(BaseUserManager):

    def create_user(self, email, password, **kwargs):
        if not email:
            raise ValueError('Email not provided')
        user = self.model(email=self.normalize_email(email), **kwargs)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email, password):
        user = self.model(email=email, password=password)
        user.is_superuser = True
        user.is_staff = True
        user.save()
        return user


class UserProfile(AbstractBaseUser, PermissionsMixin):
    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    email = models.EmailField('Адрес электронной почты', unique=True)
    first_name = models.CharField('Имя', max_length=FIRST_NAME_MAX_LEN)
    last_name = models.CharField('Фамилия', max_length=LAST_NAME_MAX_LEN)
    patronymic = models.CharField(
        'Отчество',
        max_length=PATRONYMIC_MAX_LEN,
        blank=True,
        null=True
    )
    payer_account_number = models.CharField(
        'Учетный номер плательщика',
        max_length=PAYER_ACCOUNT_NUMBER_MAX_LEN,
        blank=True,
        null=True
    )
    secret_word = models.CharField(blank=True)
    created_at = models.DateField(auto_now_add=True)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'
    objects = UserProfileManager()

    class Meta:
        ordering = ('email',)

    def __str__(self):
        return f'User(id={self.id}, email={self.email}, is_active={self.is_active})'


class SignupSession(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    email = models.EmailField()
    confirm_code = models.PositiveIntegerField()
    expiration_time = models.DateTimeField()

    def __str__(self):
        return f'SighupSession(email={self.email}, confirm_code={self.confirm_code})'


class User(models.Model):
    email = models.ForeignKey(UserProfile, on_delete=models.CASCADE, verbose_name="Email")
    first_name = models.ForeignKey(UserProfile, on_delete=models.CASCADE, verbose_name="Имя")
    last_name = models.ForeignKey(UserProfile, on_delete=models.CASCADE, verbose_name="Фамилия")
    patronymic = models.ForeignKey(UserProfile, on_delete=models.CASCADE, verbose_name="Отчество")
    personal_number = models.CharField(max_length=14, unique=True)
    registration_address = models.TextField(max_length=1000, verbose_name="Адрес регистрации", default="DEFAULT VALUE")
    residential_address = models.TextField(max_length=1000, verbose_name="Адрес проживания", default="DEFAULT VALUE")
    photo = models.ImageField(upload_to="users_photos/", null=True, blank=True)
    payer_account_number = models.ForeignKey(UserProfile, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.last_name} {self.first_name} {self.patronymic}"

    class Meta:
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"


class ProductCategory(models.Model):
    name = models.CharField(max_length=100, verbose_name="Наименование категории товара")

    def __str__(self):
        return self.name


class Product(models.Model):
    name = models.CharField(max_length=100, verbose_name="Наименование товара")
    product_description = models.TextField(max_length=1000, verbose_name="Описание товара")
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Стоимость товара")
    count = models.PositiveIntegerField(verbose_name="Количество товара в наличии")
    category = models.ForeignKey(ProductCategory, on_delete=models.CASCADE)
    reviews = models.ManyToManyField(Review, related_name="products")

    def __str__(self):
        return self.name


class ServiceCategory(models.Model):
    name = models.CharField(max_length=100, verbose_name="Наименование категории сервиса")

    def __str__(self):
        return self.name


class Service(models.Model):
    name = models.CharField(max_length=100, verbose_name="Наименование услуги")
    service_description = models.TextField(max_length=1000, verbose_name="Описание услуги")
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Стоимость услуги")
    category = models.ForeignKey(ServiceCategory, on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class Activities(models.Model):
    name = models.CharField(max_length=255, verbose_name="Вид деятельности")
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    service = models.ForeignKey(Service, on_delete=models.CASCADE)

    def __str__(self):
        return self.name


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
