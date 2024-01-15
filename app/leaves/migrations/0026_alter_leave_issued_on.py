# Generated by Django 4.0.10 on 2024-01-15 12:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('leaves', '0025_leave_issued_on'),
    ]

    operations = [
        migrations.AlterField(
            model_name='leave',
            name='issued_on',
            field=models.DateField(blank=True, db_column='ISSUED_ON', default=None, help_text='Καταχωρίστε την ημ/νια έκδοσης της απόφασης της άδειας', null=True, verbose_name='Ημ/νια έκδοσης της απόφασης'),
        ),
    ]
