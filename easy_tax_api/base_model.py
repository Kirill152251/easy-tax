from uuid import uuid4

from django.db import models

class BaseModel(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    created_at = models.DateField(auto_now_add=True)

    class Meta:
        ordering = ('created_at',)
