from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from main.models import BaseUUIDModel, SchoolYear


class Address(models.Model):
    address_line_1 = models.CharField(db_column='ADDRESS_LINE_1', max_length=128, null=False, blank=False)
    postal_code = models.CharField(db_column='POSTAL_CODE', max_length=7, null=False, blank=False)


class SchoolType(models.TextChoices):
    EPAL = "EPAL", _("ΕΠΑΛ")
    EPAS = "EPAS", _("ΕΠΑΣ")
    GEL = "GEL", _("ΓΕΛ")
    GYM = "GYM", _("ΓΥΜ")
    SMEAE = "SMEAE", _("ΣΜΕΑΕ")
    OTHER = "OTHER", _("ΑΛΛΟ")


class UnitType(models.TextChoices):
    SCHOOL = "SCHOOL", _("ΣΧΟΛΕΙΟ")
    OTHER = "OTHER", _("ΑΛΛΟ")


class Unit(models.Model):
    minoas_id = models.IntegerField(db_column='MINOAS_ID', null=True, default=None, db_index=True, blank=True)
    title = models.CharField(db_column='TITLE', max_length=80, null=False, unique=True)
    myschool_title = models.CharField(db_column='MYSCHOOL_TITLE', max_length=80, null=True, default=None, blank=True)
    address = models.ForeignKey(Address, null=True, default=None, blank=True, on_delete=models.CASCADE)
    public_sector = models.BooleanField(db_column='PUBLIC_SECTOR', null=False, default=True)
    ministry_code = models.CharField(db_column='MINISTRY_CODE', max_length=7, null=True, db_index=True)
    unit_type = models.CharField(db_column='UNIT_TYPE', choices=UnitType.choices, default=UnitType.SCHOOL, null=False,max_length=28)
    school_type = models.CharField(db_column='SCHOOL_TYPE', choices=SchoolType.choices, default=None,
                                   max_length=28, null=True)
    points = models.PositiveSmallIntegerField(db_column='POINTS', default=0, null=False)

    class Meta:
        indexes = [
            models.Index(fields=['title', ]),
            models.Index(fields=['unit_type', 'school_type']),
        ]

    def __str__(self):
        if self.unit_type == UnitType.SCHOOL:
            return f"{self.title} ({self.get_school_type_display()})"
        else:
            return f"{self.title} ({self.get_unit_type_display()})"


class Specialization(models.Model):
    code = models.CharField(db_column='CODE', max_length=20, null=False, unique=True)
    title = models.CharField(db_column='TITLE', max_length=70, null=False)
    public_code = models.CharField(db_column='PUBLIC_CODE', max_length=20, null=True)
    public_title = models.CharField(db_column='PUBLIC_TITLE', max_length=70, null=True)
    is_disabled = models.BooleanField(db_column='DISABLED', default=False)

    class Meta:
        indexes = [
            models.Index(fields=['title', 'public_title', ]),
            models.Index(fields=['is_disabled', ]),
        ]

    def __str__(self):
        return f"{ self.code } - {self.title}"


class LegacyEmployeeType(models.TextChoices):
    DEPUTY = 'DEPUTY', _('Αναπληρωτής')
    REGULAR = 'REGULAR', _('Μόνιμος')
    HOURLYPAID = 'HOURLYPAID', _('Ωρομίσθιος')
    IDAX = 'IDAX', _('Ιδιωτικού Δικαίου Αορίστου Χρόνου (Ι.Δ.Α.Χ.)'),
    ADMINISTRATIVE = 'ADMINISTRATIVE', _('Διοικητικός')


class MaritalStatusType(models.TextChoices):
    UNKNOWN = 'UNKNOWN', _('Άγνωστο')
    SINGLE = 'SINGLE', _('Άγαμος')
    MARRIED = 'MARRIED', _('Έγγαμος')
    DIVORCED = 'DIVORCED', _('Διαζευγμένος')
    WIDOWER = 'WIDOWER', _('Χηρεία')


class EmploymentStatus(models.TextChoices):
    PRESENT = 'PRESENT', _('Παρουσία')
    UNPRESENT = 'UNPRESENT', _('Απουσία')
    EXPIRED = 'EXPIRED', _('Παρήλθε')


class LegacyEmploymentType(models.TextChoices):
    DEPUTY = 'DEPUTY', _('Αναπληρωτής')
    REGULAR = 'REGULAR', _('Μόνιμος')
    HOURLYPAID = 'HOURLYPAID', _('Ωρομίσθιος')
    IDAX = 'IDAX', _('Ιδιωτικού Δικαίου Αορίστου Χρόνου (Ι.Δ.Α.Χ.)')
    ADMINISTRATIVE = 'ADMINISTRATIVE', _('Διοικητικός')


class EmploymentType(models.Model):

    title = models.CharField(null=False, blank=False, max_length=128, db_index=True)

    def __str__(self):
        return f"{self.title}"


class EmployeeType(models.Model):

    title = models.CharField(null=False, blank=False, max_length=128, db_index=True)
    legacy_type = models.CharField(choices=LegacyEmployeeType.choices, default=LegacyEmployeeType.REGULAR,
                                   max_length=32, blank=False, db_index=True)
    athina_code = models.PositiveSmallIntegerField(null=True, blank=True, db_index=True)

    def __str__(self):
        return f"{self.title} ({self.legacy_type})"


class Employee(BaseUUIDModel):
    minoas_id = models.IntegerField(db_column='MINOAS_ID', default=None, null=True, blank=True, db_index=True)
    big_family = models.BooleanField(db_column='BIG_FAMILY', null=True, blank=True)
    comment = models.CharField(db_column='COMMENT', max_length=256, null=True, blank=True)
    date_of_birth = models.DateField(db_column='BIRTH_DAY', null=True, blank=True)
    email = models.EmailField(db_column='EMAIL', max_length=64, null=True, blank=True, default=None)
    email_psd = models.EmailField(db_column='EMAIL_PSD', max_length=64, null=True, blank=True, default=None)
    father_name = models.CharField(db_column="FATHER_NAME", max_length=25, null=True)
    father_surname = models.CharField(db_column="FATHER_SURNAME", max_length=35, null=True, blank=True)
    first_name = models.CharField(db_column="FIRST_NAME", max_length=25)
    last_name = models.CharField(db_column="LAST_NAME", max_length=35)
    id_number = models.CharField(db_column="ID_NUMBER", max_length=32, null=True, blank=True)
    id_number_authority = models.CharField(db_column="ID_NUMBER_AUTHORITY", max_length=64, null=True, blank=True)
    is_man = models.BooleanField(db_column='MAN', null=True, blank=True)
    mother_name = models.CharField(db_column="MOTHER_NAME", max_length=25, null=True, blank=True)
    mother_surname = models.CharField(db_column="MOTHER_SURNAME", max_length=35, null=True, blank=True)
    vat_number = models.CharField(db_column="VAT_NUMBER", max_length=10, null=True, default=None, blank=False,
                                  db_index=True)
    amka = models.CharField(db_column='AMKA', max_length=12, null=True, default=None, blank=True,)
    registry_id = models.CharField(db_column="REGISTRY_ID", max_length=32, null=True, default=None, db_index=True,
                                   blank=True)
    employee_type = models.CharField(choices=LegacyEmployeeType.choices, default=LegacyEmployeeType.REGULAR,
                                     max_length=32, db_column='EMPLOYEE_TYPE')
    employee_type_extended = models.ForeignKey(EmployeeType, null=True, on_delete=models.CASCADE, default=None,
                                               blank=True)
    marital_status = models.CharField(choices=MaritalStatusType.choices, default=MaritalStatusType.UNKNOWN,
                                      max_length=30, db_column='MARITAL_STATUS')
    specialization = models.ForeignKey(Specialization, null=True, blank=True, on_delete=models.SET_NULL)
    current_unit = models.ForeignKey(Unit, null=True, default=None, blank=True, on_delete=models.SET_NULL)
    is_active = models.BooleanField(db_column="IS_ACTIVE", null=False, default=True, db_index=True)
    address_line = models.CharField(db_column='ADDRESS_LINE', max_length=128, blank=True, null=True, default=None)
    address_city = models.CharField(db_column='ADDRESS_CITY', max_length=64, blank=True, null=True, default=None)
    address_zip = models.CharField(db_column='ADDRESS_ZIP', max_length=12, blank=True, null=True, default=None)
    telephone = models.CharField(db_column='TELEPHONE', max_length=32, null=True, default=None, blank=True)
    mobile = models.CharField(db_column='MOBILE', max_length=32, null=True, blank=True, default=None)
    fek_diorismou = models.CharField(db_column='FEK_DORISMOU', max_length=32, blank=True, null=True, default=None)
    fek_diorismou_date = models.DateField(db_column='FEK_DIORISMOU_DATE', null=True, blank=True, default=None)
    mk = models.CharField(db_column='MK', max_length=32, null=True, blank=True, default=None)
    bathmos = models.CharField(db_column='BATHMOS', max_length=32, null=True, blank=True, default=None)
    first_workday_date = models.DateField(db_column='FIRST_WORKDAY_DATE', null=True, blank=True, default=None,
                                          help_text="Ημερομηνία 1ης Ανάληψης Υπηρεσίας")
    mandatory_week_workhours = models.PositiveSmallIntegerField(db_column='WORK_HOURS', blank=True, null=True,
                                                                default=None,
                                                                help_text='Υποχρεωτικό Διδακτικό Ωράριο')
    updated_from_athina = models.DateTimeField(db_column='ATHINA_UPDATED', blank=True, null=True, default=None)
    imported_from_athina = models.DateTimeField(db_column='ATHINA_IMPORTED', blank=True, null=True, default=None)
    updated_from_myschool = models.DateTimeField(db_column='MYSCHOOL_UPDATED', blank=True, null=True, default=None)
    imported_from_myschool = models.DateTimeField(db_column='MYSCHOOL_IMPORTED', blank=True, null=True, default=None)

    deleted_on = models.DateField(db_column="DELETED_ON", null=True, blank=True, default=None)
    deleted_comment = models.TextField(db_column="DELETED_COMMENT", blank=True, verbose_name='Σχόλιο Διαγραφής',
                                       help_text='Προαιρετικά εισάγετε σχόλιο ή περιγραφή διαγραφής',
                                       null=True, max_length=255, default=None)
    created_on = models.DateTimeField(db_column="CREATED_ON", null=False, blank=True, default=timezone.now)
    updated_on = models.DateTimeField(db_column="UPDATED_ON", null=True, blank=True)

    class Meta:
        indexes = [
            models.Index(fields=['last_name', 'first_name', ]),
            models.Index(fields=['employee_type', ]),
            models.Index(fields=['minoas_id'], )
        ]

    def get_smart_specialization_str(self):
        old_specialization: Specialization = self.specialization
        if old_specialization is not None:
            return f"{old_specialization.code} - {old_specialization.title}"

    def get_smart_fek_diorismou_str(self):
        if self.fek_diorismou is None and self.fek_diorismou_date is None:
            return None
        elif self.fek_diorismou and self.fek_diorismou_date:
            return f"{self.fek_diorismou}/{self.fek_diorismou_date}"
        elif self.fek_diorismou is None:
            return self.fek_diorismou_date
        else:
            return self.fek_diorismou

        return f"{old_specialization.code} - {old_specialization.title}"

    def __str__(self):
        return f"{ self.last_name } {self.first_name} του {self.father_name}"


class Employment(BaseUUIDModel):
    employee = models.ForeignKey(Employee, null=False, db_column="EMPLOYEE_ID", on_delete=models.CASCADE)
    specialization = models.ForeignKey(Specialization, null=False, on_delete=models.CASCADE)
    current_unit = models.ForeignKey(Unit, null=False, on_delete=models.CASCADE)
    school_year = models.ForeignKey(SchoolYear, null=False, on_delete=models.CASCADE)
    employment_type = models.CharField(choices=LegacyEmploymentType.choices, default=LegacyEmploymentType.REGULAR,
                                     max_length=32, null=False, blank=False, db_column='EMPLOYMENT_TYPE')
    employment_type_extended = models.ForeignKey(EmploymentType, null=True, blank=True, on_delete=models.CASCADE,
                                                 default=None)
    is_active = models.BooleanField(db_column="IS_ACTIVE", null=False, default=True)
    myschool_status = models.CharField(db_column='MYSCHOOL_STATUS', null=True, default=None, blank=True, max_length=68)
    mandatory_week_workhours = models.PositiveSmallIntegerField(db_column='WORK_HOURS', blank=True, null=True,
                                                                default=None,
                                                                help_text='Υποχρεωτικό Διδακτικό Ωράριο')
    week_workdays = models.CharField(max_length=10, blank=True)
    effective_from = models.DateField(default=timezone.now, null=False)
    effective_until = models.DateField(null=False)

    praksi_topothetisis = models.CharField(db_column='PRAKSI_TOPOTHETISIS', max_length=64, blank=True, null=True,
                                           default=None)
    praksi_topothetisis_date = models.DateField(db_column='PRAKSI_TOPOTHETISIS_DATE', null=True, blank=True, default=None)

    deleted_on = models.DateField(db_column="DELETED_ON", null=True, blank=True, default=None)
    deleted_comment = models.TextField(db_column="DELETED_COMMENT", blank=True, verbose_name='Σχόλιο Διαγραφής',
                                       help_text='Προαιρετικά εισάγετε σχόλιο ή περιγραφή διαγραφής',
                                       null=True, max_length=255, default=None)
    created_on = models.DateTimeField(db_column="CREATED_ON", null=False, blank=True, default=timezone.now)
    updated_on = models.DateTimeField(db_column="UPDATED_ON", null=True, blank=True)
    updated_from_myschool = models.DateTimeField(db_column='MYSCHOOL_UPDATED', blank=True, null=True, default=None)
    imported_from_myschool = models.DateTimeField(db_column='MYSCHOOL_IMPORTED', blank=True, null=True, default=None)

    class Meta:
        indexes = [
            models.Index(fields=['is_active', ]),
            models.Index(fields=['employment_type', ]),
        ]

    def get_smart_specialization_str(self):
        old_specialization: Specialization = self.specialization
        if old_specialization is not None:
            return f"{old_specialization.code} - {old_specialization.title}"

    def __str__(self):
        employee = self.employee
        return f'{employee} [{self.employment_type}] ({self.specialization.code}) {self.current_unit} για {self.mandatory_week_workhours} ώρες από ' \
               f'{self.effective_from} έως {self.effective_until}'


class WorkExperienceType(models.Model):

    code = models.PositiveSmallIntegerField(null=False, unique=True)
    description = models.CharField(null=False, max_length=128)

    def __str__(self):
        return f"[{ self.code }] {self.description}"


class WorkExperience(models.Model):
    employee = models.ForeignKey(Employee, null=False, on_delete=models.CASCADE)
    work_experience_type = models.ForeignKey(WorkExperienceType, null=False, db_column="WORK_EXPERIENCE_TYPE_ID",
                                             on_delete=models.PROTECT,
                                             verbose_name='Τύπος Υπηρεσίας',
                                             help_text="Επιλέξτε τον τύπος της Υπηρεσίας")
    date_from = models.DateField(db_column="DATE_FROM", null=True, default=None, verbose_name='Έναρξη Υπηρεσίας',
                                 help_text="Καταχωρίστε την ημ/νια έναρξης")
    date_until = models.DateField(db_column="DATE_UNTIL", null=True, default=None, verbose_name='Λήξη Υπηρεσίας',
                                  help_text="Καταχωρίστε την ημ/νια λήξης")
    comment = models.TextField(db_column="COMMENT", null=True, blank=True, verbose_name='Σχόλια Υπηρεσίας',
                               help_text='Εισάγετε τυχόν σχόλια που έχετε για την υπηρεσία', max_length=255)
    created_on = models.DateTimeField(db_column="CREATED_ON", null=False, blank=False, default=timezone.now)
    updated_on = models.DateTimeField(db_column="UPDATED_ON", null=True, blank=True)
    duration_total_in_days = models.IntegerField(db_column="DURATION_TOTAL_DAYS", null=False, default=0)
    duration_days = models.PositiveSmallIntegerField(db_column="DURATION_DAYS", null=False, default=0)
    duration_months = models.PositiveSmallIntegerField(db_column="DURATION_MONTHS", null=False, default=0)
    duration_years = models.PositiveSmallIntegerField(db_column="DURATION_YEARS", null=False, default=0)
    document_number = models.CharField(db_column='DOCUMENT_NUMBER', null=True, default=None, max_length=32)
    document_date = models.DateField(db_column="DOCUMENT_DATE", null=True)
    authority = models.CharField(db_column='AUTHORITY', null=True, max_length=128)

    def get_safe_document_str(self):
        if self.document_number and self.document_date:
            return f'{self.document_number}/{self.document_date}'
        elif self.document_number:
            return self.document_number
        elif self.document_date:
            return self.document_date
        else:
            return ''

    def __str__(self):
        return f"[{ self.work_experience_type }] {self.date_from} - {self.date_until} - {self.duration_total_in_days}"
