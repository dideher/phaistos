# Generated by Django 4.0.10 on 2023-06-26 06:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('employees', '0067_substituteemploymentannouncement_phase_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='substituteemploymentannouncement',
            name='workhour_type',
            field=models.CharField(default='A', max_length=32),
            preserve_default=False,
        ),
    ]