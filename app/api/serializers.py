from rest_framework import serializers
from employees.models import Employee, Specialization, Unit, Employment, SchoolPrincipals
from leaves.models import Leave, LeaveType


class SpecializationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Specialization
        fields = "__all__"


class EmployeeSerializer(serializers.ModelSerializer):

    specialization = serializers.SlugRelatedField(
        read_only=True,
        slug_field='code'
    )
    class Meta:
        model = Employee
        fields = ("uuid", 'last_name', 'first_name', 'father_name', 'mother_name', 'vat_number', 'registry_id',
                  'employee_type', 'specialization', 'current_unit', 'date_of_birth')


class UnitImportSerializer(serializers.Serializer):
    """
    Special Serializer to used for bulk importing units & schools
    """
    minoas_id = serializers.CharField(allow_null=True, required=True)
    title = serializers.CharField(allow_null=False, required=True)
    public_sector = serializers.BooleanField(allow_null=False, default=False)

    ministry_code = serializers.CharField(max_length=7, allow_null=True, required=False)
    school_type = serializers.CharField(max_length=28, allow_null=True, required=False)
    points = serializers.IntegerField(allow_null=True, required=False)
    is_school = serializers.BooleanField(required=False, default=False)
    is_general_unit = serializers.BooleanField(required=False, default=False)


class UnitSerializer(serializers.ModelSerializer):
    class Meta:
        model = Unit
        fields = "__all__"


class EmployeeImportSerializer(serializers.Serializer):
    """
    Special Serializer to be used for bulk importing employees
    """
    minoas_id = serializers.CharField(allow_null=True, required=True)
    email = serializers.CharField(allow_null=True, required=False)
    big_family = serializers.BooleanField(allow_null=True, required=False)
    comment = serializers.CharField(allow_null=True, required=False)
    date_of_birth = serializers.DateField(format='%Y-%m-%d', allow_null=True, required=False)
    father_name = serializers.CharField(allow_null=True, required=False)
    father_surname = serializers.CharField(allow_null=True, required=False)
    first_name = serializers.CharField(allow_null=False, required=True)
    last_name = serializers.CharField(allow_null=False, required=True)
    id_number = serializers.CharField(allow_null=True, required=False)
    id_number_authority = serializers.CharField(allow_null=True, required=False)
    is_man = serializers.BooleanField(allow_null=True, required=False)
    mother_name = serializers.CharField(allow_null=True, required=False)
    mother_surname = serializers.CharField(allow_null=True, required=False)
    vat_number = serializers.CharField(allow_null=True, required=False)
    employee_type = serializers.CharField(allow_null=False, required=True)
    marital_status = serializers.CharField(allow_null=False, required=False, default=False)
    specialization_code = serializers.CharField(allow_null=True, required=False)
    registry_id = serializers.CharField(allow_null=True, required=False)
    current_unit_id = serializers.IntegerField(allow_null=True, required=False)
    is_active = serializers.BooleanField(allow_null=False, required=False, default=True)


class LeaveTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = LeaveType
        fields = "__all__"


class LeaveSerializer(serializers.ModelSerializer):
    class Meta:
        model = Leave
        fields = "__all__"


class LeaveImportSerializer(serializers.Serializer):
    """
    Special Serializer to be used for bulk importing leaves
    """
    minoas_id = serializers.IntegerField(allow_null=False, required=True)
    minoas_employee_id = serializers.IntegerField(allow_null=False, required=True)
    minoas_leave_type_id = serializers.IntegerField(allow_null=False, required=True)
    is_active = serializers.BooleanField(allow_null=False, required=True)
    comment = serializers.CharField(allow_null=True, required=True)
    date_from = serializers.DateField(format='%Y-%m-%d', allow_null=True, required=False)
    date_until = serializers.DateField(format='%Y-%m-%d', allow_null=True, required=False)
    effective_number_of_days = serializers.IntegerField(allow_null=False, required=True)
    number_of_days = serializers.IntegerField(allow_null=False, required=True)
    is_deleted = serializers.BooleanField(allow_null=True, required=False)
    deleted_on = serializers.DateField(format='%Y-%m-%d', allow_null=True, required=False)
    deleted_comment = serializers.CharField(allow_null=True, required=False)
    specialization_code = serializers.CharField(allow_null=True, required=False)
    # class Meta:
    #     model = Employee
    #     fields = "__all__"

    # def create(self, validated_data):

    #     employee


class AthinaWorkExperience(serializers.Serializer):
    work_type = serializers.CharField(allow_null=False, allow_blank=False, required=True)
    work_type_name = serializers.CharField(allow_null=False, allow_blank=False, required=True)
    work_duration = serializers.CharField(allow_null=True, required=True)
    document_number = serializers.CharField(allow_null=True, allow_blank=False, required=True)
    document_date = serializers.DateField(format='%d/%m/%Y', input_formats=['%d/%m/%Y', ], required=False,
                                                 allow_null=True)
    authority = serializers.CharField(allow_null=True, required=True)
    work_from = serializers.DateField(format='%d/%m/%Y', input_formats=['%d/%m/%Y', ], required=True, allow_null=True)
    work_until = serializers.DateField(format='%d/%m/%Y', input_formats=['%d/%m/%Y', ], required=True, allow_null=True)
    work_comment = serializers.CharField(allow_null=True, required=True)


class AthinaEmployeeImportSerializer(serializers.Serializer):
    """
    Special Serializer to be used for bulk importing employees and work expirience from Athina
    """
    employee_first_name = serializers.CharField(allow_null=False, required=True)
    employee_last_name = serializers.CharField(allow_null=False, required=True)
    employee_father_name = serializers.CharField(allow_null=True, required=True)
    employee_mother_name = serializers.CharField(allow_null=True, allow_blank=True, required=False)
    employee_sex = serializers.CharField(allow_null=False, required=False)
    employee_type = serializers.CharField(allow_null=False, required=True)
    employee_type_name = serializers.CharField(allow_null=False, required=True)
    employee_specialization = serializers.CharField(allow_null=False, required=True)
    employee_specialization_name = serializers.CharField(allow_null=False, required=True)
    employee_afm = serializers.CharField(allow_null=True, required=False)
    employee_adt = serializers.CharField(allow_null=True, required=False)
    employee_am = serializers.CharField(allow_null=False, required=True)
    employee_amka = serializers.CharField(allow_null=True, required=False)
    employee_birthday = serializers.DateField(format='%d/%m/%Y', input_formats=['%d/%m/%Y', ], required=False,
                                              allow_null=True)
    communication_address = serializers.CharField(allow_null=True, required=False)
    communication_city = serializers.CharField(allow_null=True, required=False)
    communication_zip = serializers.CharField(allow_null=True, required=False)
    communication_telephone = serializers.CharField(allow_null=True, required=False)
    employee_fek_diorismou = serializers.CharField(allow_null=True, required=False)
    employee_fek_diorismou_date = serializers.DateField(format='%d/%m/%Y', input_formats=['%d/%m/%Y', ],
                                                        required=False, allow_null=True)
    employee_specialization_old = serializers.CharField(allow_null=False, required=False)
    employee_specialization_old_name = serializers.CharField(allow_null=False, required=False)

    work_experience = AthinaWorkExperience(many=True)


class MySchoolEmployeeImportSerializer(serializers.Serializer):
    """
    Special Serializer to be used for bulk importing employees from myschool
    """
    employee_first_name = serializers.CharField(allow_null=False, required=True)
    employee_last_name = serializers.CharField(allow_null=False, required=True)
    employee_email = serializers.CharField(allow_null=True, allow_blank=True, required=False)
    employee_email_psd = serializers.CharField(allow_null=True, allow_blank=True, required=False)
    employee_father_name = serializers.CharField(allow_null=True, required=True)
    employee_mother_name = serializers.CharField(allow_null=True, allow_blank=True, required=False)
    employee_sex = serializers.CharField(allow_null=False, allow_blank=True, required=False)
    employee_type_name = serializers.CharField(allow_null=False, required=True)
    employee_specialization_id = serializers.CharField(allow_null=False, allow_blank=False, required=True)
    employee_specialization_name = serializers.CharField(allow_null=False, allow_blank=False, required=True)
    employee_afm = serializers.CharField(allow_blank=True, required=False)
    employee_am = serializers.CharField(allow_blank=True, required=True)
    employee_birthday = serializers.DateField(format='%d/%m/%Y', input_formats=['%d/%m/%Y', ], required=False,
                                              allow_null=True)
    employee_current_unit_id = serializers.CharField(allow_null=True, allow_blank=False, required=True)
    employee_current_unit_name = serializers.CharField(allow_null=True, allow_blank=False, required=True)
    employee_telephone = serializers.CharField(allow_null=True, required=False, allow_blank=True)
    employee_mobile = serializers.CharField(allow_null=True, required=False, allow_blank=True)
    employee_fek_diorismou = serializers.CharField(allow_null=True, required=False)
    employee_fek_diorismou_date = serializers.DateField(format='%d/%m/%Y', input_formats=['%d/%m/%Y', ],
                                                        required=False, allow_null=True)
    employee_mk = serializers.CharField(allow_null=True, required=False, allow_blank=True)
    employee_bathmos = serializers.CharField(allow_null=True, required=False, allow_blank=True)
    employee_first_workday_date = serializers.DateField(format='%d/%m/%Y', input_formats=['%d/%m/%Y', ],
                                                        required=False, allow_null=True)
    employee_mandatory_week_workhours = serializers.IntegerField(allow_null=True, required=False)


class EmploymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Employment
        fields = "__all__"


class MySchoolEmploymentImportSerializer(serializers.Serializer):
    """
    Special Serializer to be used for bulk importing employees from myschool
    """
    employee_afm = serializers.CharField(allow_blank=True, required=True)
    employee_am = serializers.CharField(allow_blank=True, required=True)
    employee_last_name = serializers.CharField(allow_null=False, required=True)
    employee_first_name = serializers.CharField(allow_null=False, required=True)

    employee_specialization_id = serializers.CharField(allow_null=False, allow_blank=False, required=True)

    employee_employment_unit_id = serializers.CharField(allow_null=False, allow_blank=False, required=True)
    employee_employment_unit_name = serializers.CharField(allow_null=False, allow_blank=False, required=True)

    employee_type = serializers.CharField(allow_null=False, required=False, allow_blank=False)
    employee_employment_type = serializers.CharField(allow_null=False, required=True, allow_blank=False)
    employee_employment_days = serializers.CharField(allow_null=False, allow_blank=True, required=True)
    employee_employment_hours = serializers.IntegerField(allow_null=False, required=True)
    employee_employment_from = serializers.DateField(format='%d/%m/%Y', input_formats=['%d/%m/%Y', ], required=True, allow_null=False)
    employee_employment_until = serializers.DateField(format='%d/%m/%Y', input_formats=['%d/%m/%Y', ],
                                                      required=True, allow_null=False)
    employee_employment_status = serializers.CharField(allow_null=False, allow_blank=False, required=True)


class SchoolPrincipalSerializer(serializers.ModelSerializer):
    class Meta:
        model = SchoolPrincipals
        fields = "__all__"
