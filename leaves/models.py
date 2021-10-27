from django.db import models
from django.utils.translation import gettext_lazy as _

from employees.models import Employee, EmployeeType


class LeaveBasicType(models.TextChoices):
    UNPAID_LEAVE = 'UNPAID_LEAVE', _('Άνευ Αποδοχών')
    REGULAR_LEAVE = 'REGULAR_LEAVE', _('Κανονική Άδεια')
    GENERIC_LEAVE = 'GENERIC_LEAVE', _('Γενική Άδεια')


class LeaveType(models.Model):
    """
    Leave Types
    """
    minoas_id = models.IntegerField(db_column='MINOAS_ID', default=None, null=False, unique=True)
    is_active = models.BooleanField(db_column="IS_ACTIVE", db_index=True, null=False, default=True)
    description = models.CharField(db_column="DESCRIPTION", db_index=True, max_length=255, null=True)
    legacy_code = models.CharField(db_column="LEGACY_CODE", db_index=True, max_length=32, null=False)
    suitable_for_employee_type = models.CharField(choices=EmployeeType.choices,
                                                  default=EmployeeType.REGULAR,
                                                  max_length=32,
                                                  db_index=True,
                                                  db_column='EMPLOYEE_TYPE')
    basic_type = models.CharField(choices=LeaveBasicType.choices,
                                  default=LeaveBasicType.REGULAR_LEAVE,
                                  max_length=32, db_column='BASIC_TYPE')

    def __str__(self):
        return f"(#{self.legacy_code}) - {self.description}"




class Leave(models.Model):
    """
    Models an employee leave
    """
    minoas_id = models.IntegerField(db_column='MINOAS_ID', default=None, null=False, unique=True)
    employee = models.ForeignKey(Employee, null=False, db_column="EMPLOYEE_ID", on_delete=models.PROTECT)
    leave_type = models.ForeignKey(LeaveType, null=False, db_column="EMPLOYEE_LEAVE_TYPE_ID", on_delete=models.PROTECT)
    is_active = models.BooleanField(db_column="IS_ACTIVE", null=False, default=True, db_index=True)
    comment = models.TextField(db_column="COMMENT", null=True, max_length=255)
    date_from = models.DateField(db_column="DATE_FROM", null=False)
    date_until = models.DateField(db_column="DATE_UNTIL", null=False)
    effective_number_of_days = models.IntegerField(db_column="EFFECTIVE_DAYS_COUNT", null=True)
    number_of_days = models.IntegerField(db_column="DAYS_COUNT", null=True)
    is_deleted = models.BooleanField(db_column="IS_DELETED", null=False, default=False, db_index=True)
    deleted_on = models.DateField(db_column="DELETED_ON", null=True)
    deleted_comment = models.TextField(db_column="DELETED_COMMENT", null=True, max_length=255)

    class Meta:
        indexes = [
            models.Index(fields=['employee', 'leave_type',]),
        ]

    def __str__(self):
        return f"[{self.leave_type}] - {self.effective_number_of_days} : {self.date_from} - {self.date_until}"