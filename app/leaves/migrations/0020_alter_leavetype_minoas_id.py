# Generated by Django 4.0.7 on 2023-03-24 08:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('leaves', '0019_alter_leavetype_description_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='leavetype',
            name='minoas_id',
            field=models.IntegerField(blank=True, db_column='MINOAS_ID', db_index=True, default=None, null=True),
        ),
    ]
