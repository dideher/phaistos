# Generated by Django 4.0.10 on 2023-03-29 09:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('employees', '0052_remove_employeetype_code_employeetype_athina_code_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='employeetype',
            name='athina_code',
            field=models.PositiveSmallIntegerField(blank=True, db_index=True, null=True),
        ),
        migrations.AlterField(
            model_name='employeetype',
            name='title',
            field=models.CharField(db_index=True, max_length=128),
        ),
    ]