# Generated by Django 3.1.5 on 2021-10-13 08:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('employees', '0003_auto_20211013_0751'),
    ]

    operations = [
        migrations.AlterField(
            model_name='employee',
            name='date_of_birth',
            field=models.DateField(db_column='BIRTH_DAY', null=True),
        ),
    ]
