# Generated by Django 4.0.7 on 2023-03-24 08:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('leaves', '0018_alter_leave_health_committee_protocol_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='leavetype',
            name='description',
            field=models.CharField(blank=True, db_column='DESCRIPTION', db_index=True, max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='leavetype',
            name='legacy_code',
            field=models.CharField(blank=True, db_column='LEGACY_CODE', db_index=True, max_length=32),
        ),
        migrations.AlterField(
            model_name='leavetype',
            name='minoas_id',
            field=models.IntegerField(db_column='MINOAS_ID', db_index=True, default=None, null=True),
        ),
    ]