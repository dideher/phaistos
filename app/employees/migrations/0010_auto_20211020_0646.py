# Generated by Django 3.1.5 on 2021-10-20 06:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('employees', '0009_employee_specialization'),
    ]

    operations = [
        migrations.AlterField(
            model_name='employee',
            name='minoas_id',
            field=models.IntegerField(db_column='MINOAS_ID', default=None, unique=True),
        ),
    ]