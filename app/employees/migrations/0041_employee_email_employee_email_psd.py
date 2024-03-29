# Generated by Django 4.0.2 on 2022-10-12 08:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('employees', '0040_remove_employee_email'),
    ]

    operations = [
        migrations.AddField(
            model_name='employee',
            name='email',
            field=models.EmailField(blank=True, db_column='EMAIL', default=None, max_length=64, null=True),
        ),
        migrations.AddField(
            model_name='employee',
            name='email_psd',
            field=models.EmailField(blank=True, db_column='EMAIL_PSD', default=None, max_length=64, null=True),
        ),
    ]
