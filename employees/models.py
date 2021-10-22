from django.db import models

from django.utils.translation import gettext_lazy as _

class Specialization(models.Model):
    code = models.CharField(db_column='CODE', max_length=9, null=False, unique=True)
    title = models.CharField(db_column='TITLE', max_length=70, null=False)
    public_code = models.CharField(db_column='PUBLIC_CODE', max_length=9, null=True)
    public_title = models.CharField(db_column='PUBLIC_TITLE', max_length=70, null=True)
    is_disabled = models.BooleanField(db_column='DISABLED', default=False)

    class Meta:
        indexes = [
            models.Index(fields=['title', 'public_title',]),
            models.Index(fields=['is_disabled',]),
        ]

    def __str__(self):
        return f"{ self.code } - {self.title}"

class EmployeeType(models.TextChoices):
    DEPUTY = 'DEPUTY', _('Αναπληρωτής')
    REGULAR = 'REGULAR', _('Μόνιμος')
    HOURLYPAID = 'HOURLYPAID', _('Ωρομίσθιος')
    ADMINISTRATIVE = 'ADMINISTRATIVE', _('Διοικητικός')

class MaritalStatusType(models.TextChoices):
    UNKNOWN = 'UNKNOWN', _('Άγνωστο')
    SINGLE = 'SINGLE', _('Άγαμος')
    MARRIED = 'MARRIED', _('Έγγαμος')
    DIVORCED = 'DIVORCED', _('Διαζευγμένος')
    WIDOWER = 'WIDOWER', _('Χηρεία')

class Employee(models.Model):
    minoas_id = models.IntegerField(db_column='MINOAS_ID', default=None, null=False, unique=True)
    big_family = models.BooleanField(db_column='BIG_FAMILY', null=True)
    comment = models.CharField(db_column='COMMENT', max_length=256, null=True)
    date_of_birth = models.DateField(db_column='BIRTH_DAY', null=True)
    email = models.EmailField(db_column='EMAIL', max_length=64, null=True)
    father_name = models.CharField(db_column="FATHER_NAME", max_length=25, null=True)
    father_surname = models.CharField(db_column="FATHER_SURNAME", max_length=35, null=True)
    first_name = models.CharField(db_column="FIRST_NAME", max_length=25)
    last_name = models.CharField(db_column="LAST_NAME", max_length=35)
    id_number = models.CharField(db_column="ID_NUMBER", max_length=10, null=True)
    id_number_authority = models.CharField(db_column="ID_NUMBER_AUTHORITY", max_length=64, null=True)
    is_man = models.BooleanField(db_column='MAN', null=True)
    mother_name = models.CharField(db_column="MOTHER_NAME", max_length=25, null=True)
    mother_surname = models.CharField(db_column="MOTHER_SURNAME", max_length=35, null=True)
    vat_number = models.CharField(db_column="VAT_NUMBER", max_length=10, null=True)
    employee_type = models.CharField(choices=EmployeeType.choices, default=EmployeeType.REGULAR, max_length=32,
                            db_column='EMPLOYEE_TYPE')
    marital_status = models.CharField(choices=MaritalStatusType.choices, default=MaritalStatusType.UNKNOWN, max_length=30,
                            db_column='MARITAL_STATUS')
    specialization = models.ForeignKey(Specialization, null=True, on_delete=models.SET_NULL)

    class Meta:
        indexes = [
            models.Index(fields=['last_name', 'first_name',]),
            models.Index(fields=['vat_number',]),
            models.Index(fields=['employee_type',]),
        ]

    def __str__(self):
        return f"{ self.last_name } {self.last_name} {self.father_name}"
