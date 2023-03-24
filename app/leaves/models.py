from django.db import models
from django.utils.translation import gettext_lazy as _
from django.utils import timezone
from employees.models import Employee, LegacyEmployeeType


class LeaveBasicType(models.TextChoices):
    UNPAID_LEAVE = 'UNPAID_LEAVE', _('Άνευ Αποδοχών')
    REGULAR_LEAVE = 'REGULAR_LEAVE', _('Κανονική Άδεια')
    GENERIC_LEAVE = 'GENERIC_LEAVE', _('Γενική Άδεια')


class LeaveType(models.Model):
    """
    Leave Types
    """
    minoas_id = models.IntegerField(db_column='MINOAS_ID', default=None, null=True, unique=False, blank=True,
                                    db_index=True)
    is_active = models.BooleanField(db_column="IS_ACTIVE", db_index=True, null=False, default=True)
    description = models.CharField(db_column="DESCRIPTION", db_index=True, max_length=255, blank=True, null=True)
    legacy_code = models.CharField(db_column="LEGACY_CODE", db_index=True, max_length=32, blank=True, null=False)
    suitable_for_employee_type = models.CharField(choices=LegacyEmployeeType.choices,
                                                  default=LegacyEmployeeType.REGULAR,
                                                  max_length=32,
                                                  db_index=True,
                                                  db_column='EMPLOYEE_TYPE')
    basic_type = models.CharField(choices=LeaveBasicType.choices,
                                  default=LeaveBasicType.REGULAR_LEAVE,
                                  max_length=32, db_column='BASIC_TYPE')

    def __str__(self):
        return f"(#{self.legacy_code}) - {self.description} ({LegacyEmployeeType(self.suitable_for_employee_type).label})"


class Leave(models.Model):
    """
    Models an employee leave
    """
    minoas_id = models.IntegerField(db_column='MINOAS_ID', default=None, null=True)
    employee = models.ForeignKey(Employee, null=False, db_column="EMPLOYEE_ID", on_delete=models.PROTECT)
    leave_type = models.ForeignKey(LeaveType, null=False, db_column="EMPLOYEE_LEAVE_TYPE_ID", on_delete=models.PROTECT,
                                   verbose_name='Τύπος Άδειας', help_text="Επιλέξτε τον τύπος της άδειας")
    is_active = models.BooleanField(db_column="IS_ACTIVE", null=False, default=True, db_index=True)
    comment = models.TextField(db_column="COMMENT", null=True, blank=True, verbose_name='Σχόλια Άδειας',
                               help_text='Εισάγετε τυχόν σχόλια που έχετε για την άδεια', max_length=255)
    date_from = models.DateField(db_column="DATE_FROM", null=False, verbose_name='Έναρξη Άδειας',
                                 help_text="Καταχωρίστε την ημ/νια έναρξης")
    date_until = models.DateField(db_column="DATE_UNTIL", null=False, verbose_name='Λήξη Άδειας',
                                  help_text="Καταχωρίστε την ημ/νια λήξης")
    effective_number_of_days = models.IntegerField(db_column="EFFECTIVE_DAYS_COUNT", null=True,
                                                   verbose_name='Διάρκεια Άδειας',
                                                   help_text="Καταχωρίστε την πραγματική διάρκειας της άδειας")
    number_of_days = models.IntegerField(db_column="DAYS_COUNT", null=True, verbose_name='Ημερολογιακή Διάρκεια Άδειας',
                                         help_text='Ημερολογιακή Διάρκεια Άδειας. Υπολογίζεται αυτόματα απο την Ημ/νια '
                                                   'Έναρξης και Λήξης της άδειας')
    is_deleted = models.BooleanField(db_column="IS_DELETED", null=False, default=False, db_index=True)
    deleted_on = models.DateField(db_column="DELETED_ON", null=True)
    deleted_comment = models.TextField(db_column="DELETED_COMMENT", verbose_name='Σχόλιο Διαγραφής',
                                       help_text='Προαιρετικά εισάγετε σχόλιο ή περιγραφή διαγραφής της άδειας',
                                       null=True, max_length=255)
    created_on = models.DateTimeField(db_column="CREATED_ON", null=False, blank=False, default=timezone.now)
    updated_on = models.DateTimeField(db_column="UPDATED_ON", null=True, blank=True)

    health_committee_protocol = models.CharField(db_column="HEALTH_COMMITTEE_PROTOCOL", max_length=128, blank=True,
                                                 verbose_name="Πρωτόκολλο Γνωμάτευσης Υγ. Επιτροπής",
                                                 default='',
                                                 help_text="Καταχωρίστε το πρωτόκολλο της γνωμάτευσης της Α/θμιας "
                                                           "Υγειονομικής Επιτροπής")

    incoming_protocol = models.CharField(db_column="INCOMING_PROTOCOL", max_length=64, blank=True, default='',
                                         verbose_name="Αριθμός Εισερχόμενου Πρωτοκόλλου",
                                         help_text="Καταχωρίστε τον αριθμό του εισερχόμενου πρωτοκόλλου")

    incoming_protocol_date = models.DateField(db_column="INCOMING_PROTOCOL_DATE", null=True, default=None, blank=True,
                                              verbose_name="Ημ/νια Εισερχόμενου Πρωτοκόλλου",
                                              help_text="Καταχωρίστε την ημ/νία του εισερχόμενου πρωτοκόλλου")

    class Meta:
        indexes = [
            models.Index(fields=['employee', 'leave_type', ]),
            models.Index(fields=['minoas_id'], )
        ]

    def __str__(self):
        return f"[{self.leave_type}] - {self.effective_number_of_days} : {self.date_from} - {self.date_until}"
