# Generated by Django 3.1.5 on 2021-10-15 06:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('employees', '0007_auto_20211015_0628'),
    ]

    operations = [
        migrations.RemoveIndex(
            model_name='specialization',
            name='employees_s_DISABLE_0e9f80_idx',
        ),
        migrations.RenameField(
            model_name='specialization',
            old_name='disabled',
            new_name='is_disabled',
        ),
        migrations.AddIndex(
            model_name='specialization',
            index=models.Index(fields=['is_disabled'], name='employees_s_DISABLE_0e9f80_idx'),
        ),
    ]
