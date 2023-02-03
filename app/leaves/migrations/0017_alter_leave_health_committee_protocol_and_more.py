# Generated by Django 4.0.7 on 2023-02-02 08:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('leaves', '0016_leave_health_committee_protocol_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='leave',
            name='health_committee_protocol',
            field=models.CharField(blank=True, db_column='HEALTH_COMMITTEE_PROTOCOL', default='', help_text='Καταχωρίστε το Πρωτόκολλο Υγειονομικής Επιτροπής', max_length=128, verbose_name='Πρωτόκολλο Υγειονομικής Επιτροπής'),
        ),
        migrations.AlterField(
            model_name='leave',
            name='incoming_protocol',
            field=models.CharField(blank=True, db_column='INCOMING_PROTOCOL', default='', help_text='Καταχωρίστε τον αριθμό του εισερχόμενου πρωτοκόλλου', max_length=64, verbose_name='Αριθμός Εισερχόμενου Πρωτοκόλλου'),
        ),
    ]
