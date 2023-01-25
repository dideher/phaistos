# Generated by Django 4.0.2 on 2022-10-13 07:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('employees', '0042_employee_mobile_alter_employee_telephone'),
    ]

    operations = [
        migrations.AlterField(
            model_name='employee',
            name='amka',
            field=models.CharField(db_column='AMKA', default=None, max_length=12, null=True),
        ),
        migrations.AlterField(
            model_name='employee',
            name='registry_id',
            field=models.CharField(db_column='REGISTRY_ID', db_index=True, default=None, max_length=32, null=True),
        ),
        migrations.AlterField(
            model_name='employee',
            name='vat_number',
            field=models.CharField(db_column='VAT_NUMBER', db_index=True, default=None, max_length=10, null=True),
        ),
    ]