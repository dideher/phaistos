# Generated by Django 4.0.7 on 2022-12-16 07:15

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('employees', '0046_alter_employee_amka_alter_employee_big_family_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='employee',
            name='public_id',
            field=models.UUIDField(default=uuid.uuid4, editable=False, null=True),
        ),
    ]
