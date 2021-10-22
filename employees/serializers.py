from rest_framework import serializers
from .models import Employee, Specialization

class SpecializationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Specialization
        fields = "__all__"
class EmployeeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Employee
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
    marital_status = serializers.CharField(allow_null=True, required=False)
    

    specialization_code = serializers.CharField(allow_null=True, required=False)
    # class Meta:
    #     model = Employee
    #     fields = "__all__"

    # def create(self, validated_data):

    #     employee