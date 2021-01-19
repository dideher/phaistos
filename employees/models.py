from django.db import models

from django.utils.translation import gettext_lazy as _


class Employee(models.Model):

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

    big_family = models.BooleanField(db_column='BIG_FAMILY')
    comment = models.CharField(db_column='COMMENT', max_length=256)
    date_of_birth = models.DateField(db_column='BIRTH_DAY')
    email = models.EmailField(db_column='EMAIL', max_length=64)
    father_name = models.CharField(db_column="FATHER_NAME", max_length=25)
    father_surname = models.CharField(db_column="FATHER_SURNAME", max_length=35)
    first_name = models.CharField(db_column="FIRST_NAME", max_length=25)
    last_name = models.CharField(db_column="LAST_NAME", max_length=35)
    id_number = models.CharField(db_column="ID_NUMBER", max_length=10)
    id_number_authority = models.CharField(db_column="ID_NUMBER_AUTHORITY", max_length=64)
    is_man = models.BooleanField(db_column='MAN')
    mother_name = models.CharField(db_column="MOTHER_NAME", max_length=25)
    mother_surname = models.CharField(db_column="MOTHER_SURNAME", max_length=35)
    vat_number = models.CharField(db_column="VAT_NUMBER", max_length=10)
    type = models.CharField(choices=EmployeeType.choices, default=EmployeeType.REGULAR, max_length=32,
                            db_column='EMPLOYEE_TYPE')
    maritalType = models.CharField(choices=MaritalStatusType.choices, default=MaritalStatusType.UNKNOWN, max_length=30,
                            db_column='MARITAL_STATUS')

    def __str__(self):
        return f"{ self.last_name } {self.last_name} {self.father_name}"

