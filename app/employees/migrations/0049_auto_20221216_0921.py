# Generated by Django 4.0.7 on 2022-12-16 07:21

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('employees', '0048_auto_20221216_0921'),
    ]

    operations = [
        migrations.AlterField(
            model_name='employee',
            name='public_id',
            field=models.UUIDField(default=uuid.uuid4, editable=False, unique=True),
        ),
    ]
