# Generated by Django 4.0.2 on 2022-09-16 11:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('employees', '0034_employee_fek_diorismou_employee_fek_diorismou_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='employee',
            name='fek_diorismou',
            field=models.CharField(db_column='FEK_DORISMOU', default=None, max_length=32, null=True),
        ),
    ]