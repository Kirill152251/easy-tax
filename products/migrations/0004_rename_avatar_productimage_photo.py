# Generated by Django 5.0.6 on 2024-07-29 20:39

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("products", "0003_alter_product_price_alter_productimage_avatar"),
    ]

    operations = [
        migrations.RenameField(
            model_name="productimage",
            old_name="avatar",
            new_name="photo",
        ),
    ]