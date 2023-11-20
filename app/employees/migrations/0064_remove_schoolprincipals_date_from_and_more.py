# Generated by Django 4.0.10 on 2023-11-16 08:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('employees', '0063_employee_is_school_principal_schoolprincipals_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='schoolprincipals',
            name='date_from',
        ),
        migrations.RemoveField(
            model_name='schoolprincipals',
            name='date_until',
        ),
        migrations.AlterField(
            model_name='employee',
            name='is_school_principal',
            field=models.BooleanField(db_column='IS_PRINCIPAL', default=False, help_text='Είναι Διευθυντής ;'),
        ),
    ]