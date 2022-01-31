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
    minoas_id = models.IntegerField(db_column='MINOAS_ID', default=None, null=True)
    employee = models.ForeignKey(Employee, null=False, db_column="EMPLOYEE_ID", on_delete=models.PROTECT)
    leave_type = models.ForeignKey(LeaveType, null=False, db_column="EMPLOYEE_LEAVE_TYPE_ID", on_delete=models.PROTECT,
                                   verbose_name='Τύπος Άδειας', help_text="Επιλέξτε τον τύπος της άδειας")
    is_active = models.BooleanField(db_column="IS_ACTIVE", null=False, default=True, db_index=True)
    comment = models.TextField(db_column="COMMENT", null=True, blank=True,
                               help_text='Εισάγεται τυχόν σχόλια που έχετε για την άδεια', max_length=255)
    date_from = models.DateField(db_column="DATE_FROM", null=False, verbose_name='Έναρξη Άδειας',
                                 help_text="Καταχωρίστε την ημ/νια έναρξης")
    date_until = models.DateField(db_column="DATE_UNTIL", null=False, verbose_name='Λήξη Άδειας',
                                  help_text="Καταχωρίστε την ημ/νια λήξης")
    effective_number_of_days = models.IntegerField(db_column="EFFECTIVE_DAYS_COUNT", null=True,
                                                   verbose_name='Έναρξη Άδειας',
                                                   help_text="Καταχωρίστε την πραγματική διάρκειας της άδειας")
    number_of_days = models.IntegerField(db_column="DAYS_COUNT", null=True, verbose_name='Ημερολογιακή Διάρκεια Άδειας',
                                         help_text='Ημερολογιακή Διάρκεια Άδειας. Υπολογίζεται αυτόματα απο την Ημ/νια '
                                                   'Έναρξης και Λήξεις της άδειας')
    is_deleted = models.BooleanField(db_column="IS_DELETED", null=False, default=False, db_index=True)
    deleted_on = models.DateField(db_column="DELETED_ON", null=True)
    deleted_comment = models.TextField(db_column="DELETED_COMMENT", verbose_name='Σχόλιο Διαγραφής',
                                       help_text='Προαιρετικά εισάγεται σχόλιο ή περιγραφή διαγραφής της άδειας',
                                       null=True, max_length=255)

    class Meta:
        indexes = [
            models.Index(fields=['employee', 'leave_type',]),
        ]

    def __str__(self):
        return f"[{self.leave_type}] - {self.effective_number_of_days} : {self.date_from} - {self.date_until}"