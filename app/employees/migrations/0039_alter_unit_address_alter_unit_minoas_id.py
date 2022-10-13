# Generated by Django 4.0.2 on 2022-10-12 07:40

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('employees', '0038_unit_myschool_title_alter_unit_ministry_code'),
    ]

    operations = [
        migrations.AlterField(
            model_name='unit',
            name='address',
            field=models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.CASCADE, to='employees.address'),
        ),
        migrations.AlterField(
            model_name='unit',
            name='minoas_id',
            field=models.IntegerField(blank=True, db_column='MINOAS_ID', db_index=True, default=None, null=True),
        ),
    ]
