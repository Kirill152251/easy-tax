from django.contrib.auth import get_user_model
from django.db import models
from django.core.validators import FileExtensionValidator, MinValueValidator

from core import const
from core.models import BaseModel


User = get_user_model()


class ProductCategory(BaseModel):
    name = models.CharField(
        'Наименование категории товара',
        max_length=500,
    )

    class Meta:
        verbose_name = 'Категория продукта'
        verbose_name_plural = 'Категории продуктов'

    def __str__(self):
        return self.name[:30]


class Product(BaseModel):
    name = models.CharField('Наименование товара', max_length=500)
    description = models.CharField('Описание товара', max_length=const.PRODUCT_DESCRIP_MAX_LEN)
    price = models.DecimalField('Стоимость товара', max_digits=10, decimal_places=2, validators=[MinValueValidator(0)])
    count = models.PositiveIntegerField(
        'Количество товара в наличии',
        null=True,
        blank=True
    )
    category = models.ForeignKey(ProductCategory, on_delete=models.CASCADE)
    seller = models.ForeignKey(User, on_delete=models.CASCADE)

    class Meta:
        verbose_name = 'Товар'
        verbose_name_plural = 'Товары'
        default_related_name = 'products'

    def __str__(self):
        return self.name[:30]


class ProductImage(BaseModel):
    photo = models.ImageField(upload_to='products_images', validators=[FileExtensionValidator(allowed_extensions=['jpg', 'jpeg', 'png'])])
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='images')
