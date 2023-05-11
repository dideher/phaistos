# Generated by Django 4.0.10 on 2023-05-10 06:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('employees', '0059_employment_week_workdays'),
    ]

    operations = [
        migrations.AddField(
            model_name='employment',
            name='myschool_status',
            field=models.CharField(blank=True, db_column='MYSCHOOL_STATUS', default=None, max_length=68, null=True),
        ),
        migrations.AlterField(
            model_name='employee',
            name='employee_type',
            field=models.CharField(choices=[('DEPUTY', 'Αναπληρωτής'), ('REGULAR', 'Μόνιμος'), ('HOURLYPAID', 'Ωρομίσθιος'), ('IDAX', 'Ιδιωτικού Δικαίου Αορίστου Χρόνου (Ι.Δ.Α.Χ.)'), ('ADMINISTRATIVE', 'Διοικητικός')], db_column='EMPLOYEE_TYPE', default='REGULAR', max_length=32),
        ),
        migrations.AlterField(
            model_name='employeetype',
            name='legacy_type',
            field=models.CharField(choices=[('DEPUTY', 'Αναπληρωτής'), ('REGULAR', 'Μόνιμος'), ('HOURLYPAID', 'Ωρομίσθιος'), ('IDAX', 'Ιδιωτικού Δικαίου Αορίστου Χρόνου (Ι.Δ.Α.Χ.)'), ('ADMINISTRATIVE', 'Διοικητικός')], db_index=True, default='REGULAR', max_length=32),
        ),
        migrations.AlterField(
            model_name='employment',
            name='employment_type',
            field=models.CharField(choices=[('DEPUTY', 'Αναπληρωτής'), ('REGULAR', 'Μόνιμος'), ('HOURLYPAID', 'Ωρομίσθιος'), ('IDAX', 'Ιδιωτικού Δικαίου Αορίστου Χρόνου (Ι.Δ.Α.Χ.)'), ('ADMINISTRATIVE', 'Διοικητικός')], db_column='EMPLOYMENT_TYPE', default='REGULAR', max_length=32),
        ),
        migrations.AlterField(
            model_name='employment',
            name='is_active',
            field=models.BooleanField(db_column='IS_ACTIVE', default=True),
        ),
    ]
