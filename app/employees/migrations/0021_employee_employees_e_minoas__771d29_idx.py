# Generated by Django 4.0.2 on 2022-03-16 07:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('employees', '0020_employee_current_unit'),
    ]

    operations = [
        migrations.AddIndex(
            model_name='employee',
            index=models.Index(fields=['minoas_id'], name='employees_e_MINOAS__771d29_idx'),
        ),
    ]
