# Generated by Django 4.0.2 on 2022-12-14 11:16

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('employees', '0044_alter_employee_created_on_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='employee',
            name='address_city',
            field=models.CharField(blank=True, db_column='ADDRESS_CITY', default=None, max_length=64, null=True),
        ),
        migrations.AlterField(
            model_name='employee',
            name='address_line',
            field=models.CharField(blank=True, db_column='ADDRESS_LINE', default=None, max_length=128, null=True),
        ),
        migrations.AlterField(
            model_name='employee',
            name='address_zip',
            field=models.CharField(blank=True, db_column='ADDRESS_ZIP', default=None, max_length=12, null=True),
        ),
        migrations.AlterField(
            model_name='employee',
            name='bathmos',
            field=models.CharField(blank=True, db_column='BATHMOS', default=None, max_length=32, null=True),
        ),
        migrations.AlterField(
            model_name='employee',
            name='current_unit',
            field=models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.SET_NULL, to='employees.unit'),
        ),
        migrations.AlterField(
            model_name='employee',
            name='fek_diorismou',
            field=models.CharField(blank=True, db_column='FEK_DORISMOU', default=None, max_length=32, null=True),
        ),
        migrations.AlterField(
            model_name='employee',
            name='fek_diorismou_date',
            field=models.DateField(blank=True, db_column='FEK_DIORISMOU_DATE', default=None, null=True),
        ),
        migrations.AlterField(
            model_name='employee',
            name='first_workday_date',
            field=models.DateField(blank=True, db_column='FIRST_WORKDAY_DATE', default=None, help_text='Ημερομηνία 1ης Ανάληψης Υπηρεσίας', null=True),
        ),
        migrations.AlterField(
            model_name='employee',
            name='imported_from_athina',
            field=models.DateTimeField(blank=True, db_column='ATHINA_IMPORTED', default=None, null=True),
        ),
        migrations.AlterField(
            model_name='employee',
            name='imported_from_myschool',
            field=models.DateTimeField(blank=True, db_column='MYSCHOOL_IMPORTED', default=None, null=True),
        ),
        migrations.AlterField(
            model_name='employee',
            name='mandatory_week_workhours',
            field=models.PositiveSmallIntegerField(blank=True, db_column='WORK_HOURS', default=None, help_text='Υποχρεωτικό Διδακτικό Ωράριο', null=True),
        ),
        migrations.AlterField(
            model_name='employee',
            name='mk',
            field=models.CharField(blank=True, db_column='MK', default=None, max_length=32, null=True),
        ),
        migrations.AlterField(
            model_name='employee',
            name='specialization',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='employees.specialization'),
        ),
        migrations.AlterField(
            model_name='employee',
            name='updated_from_athina',
            field=models.DateTimeField(blank=True, db_column='ATHINA_UPDATED', default=None, null=True),
        ),
        migrations.AlterField(
            model_name='employee',
            name='updated_from_myschool',
            field=models.DateTimeField(blank=True, db_column='MYSCHOOL_UPDATED', default=None, null=True),
        ),
    ]
