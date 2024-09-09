import uuid
from django.contrib.auth import get_user_model
from django.db import models

from products.models import Product

User = get_user_model()


class Order(models.Model):

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    created_at = models.DateField(auto_now_add=True)

    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name='orders'
    )
    buyer = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='orders_to_buy'
    )
    seller = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='orders_to_sell'
    )
    count = models.PositiveIntegerField()

    class Meta:
        ordering = ('created_at',)
