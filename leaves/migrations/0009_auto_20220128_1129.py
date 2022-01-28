# Generated by Django 3.1.13 on 2022-01-28 09:29

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('leaves', '0008_auto_20211116_1036'),
    ]

    operations = [
        migrations.AlterField(
            model_name='leave',
            name='comment',
            field=models.TextField(blank=True, db_column='COMMENT', help_text='Εισάγεται τυχόν σχόλια που έχετε για την άδεια', max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='leave',
            name='date_from',
            field=models.DateField(db_column='DATE_FROM', help_text='Καταχωρίστε την ημ/νια έναρξης', verbose_name='Έναρξη Άδειας'),
        ),
        migrations.AlterField(
            model_name='leave',
            name='date_until',
            field=models.DateField(db_column='DATE_UNTIL', help_text='Καταχωρίστε την ημ/νια λήξης', verbose_name='Λήξη Άδειας'),
        ),
        migrations.AlterField(
            model_name='leave',
            name='effective_number_of_days',
            field=models.IntegerField(db_column='EFFECTIVE_DAYS_COUNT', help_text='Καταχωρίστε την πραγματική διάρκειας της άδειας', null=True, verbose_name='Έναρξη Άδειας'),
        ),
        migrations.AlterField(
            model_name='leave',
            name='leave_type',
            field=models.ForeignKey(db_column='EMPLOYEE_LEAVE_TYPE_ID', help_text='Επιλέξτε τον τύπος της άδειας', on_delete=django.db.models.deletion.PROTECT, to='leaves.leavetype', verbose_name='Τύπος Άδειας'),
        ),
        migrations.AlterField(
            model_name='leave',
            name='number_of_days',
            field=models.IntegerField(db_column='DAYS_COUNT', null=True, verbose_name='Έναρξη Άδειας'),
        ),
    ]
