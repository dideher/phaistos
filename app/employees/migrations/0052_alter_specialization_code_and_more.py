# Generated by Django 4.0.10 on 2023-03-30 10:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('employees', '0051_alter_employee_deleted_comment_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='specialization',
            name='code',
            field=models.CharField(db_column='CODE', max_length=20, unique=True),
        ),
        migrations.AlterField(
            model_name='specialization',
            name='public_code',
            field=models.CharField(db_column='PUBLIC_CODE', max_length=20, null=True),
        ),
    ]
