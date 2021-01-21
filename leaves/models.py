from django.db import models
from django.utils.translation import gettext_lazy as _

from employees.models import Employee, EmployeeType


class LeaveBasicType(models.TextChoices):
    UNPAID_LEAVE = 'UNPAID_LEAVE', _('Άνευ Αποδοχών')
    REGULAR_LEAVE = 'REGULAR_LEAVE', _('Κανονική Άδεια')
    GENERIC_LEAVE = 'HOURLYPAID', _('Γενική Άδεια')


class LeaveType(models.Model):
    """
    Leave Types
    """
    is_active = models.BooleanField(db_column="IS_ACTIVE", null=False, default=True)
    description = models.CharField(db_column="DESCRIPTION", max_length=255, null=True)
    legacy_code = models.CharField(db_column="LEGACY_CODE", null=False, max_length=32)
    suitable_for_employee_type = models.CharField(choices=EmployeeType.choices,
                                                  default=EmployeeType.REGULAR,
                                                  max_length=32,
                                                  db_column='EMPLOYEE_TYPE')
    basic_type = models.CharField(choices=LeaveBasicType.choices,
                                  default=LeaveBasicType.REGULAR_LEAVE,
                                  max_length=32, db_column='BASIC_TYPE')


class Leave(models.Model):
    """
    Models an employee leave
    """
    employee = models.ForeignKey(Employee, null=False, db_column="EMPLOYEE_ID", on_delete=models.PROTECT)
    leave_type = models.ForeignKey(LeaveType, null=False, db_column="EMPLOYEE_LEAVE_TYPE_ID", on_delete=models.PROTECT)
    is_active = models.BooleanField(db_column="IS_ACTIVE", null=False, default=True)
    comment = models.TextField(db_column="COMMENT", null=True)
    date_from = models.DateField(db_column="DATE_FROM", null=False)
    date_until = models.DateField(db_column="DATE_UNTIL", null=False)
    effective_number_of_days = models.IntegerField(db_column="EFFECTIVE_DAYS_COUNT", null=True)
    number_of_days = models.IntegerField(db_column="DAYS_COUNT", null=True)
