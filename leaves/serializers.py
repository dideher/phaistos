from rest_framework import serializers
from leaves.models import LeaveType, Leave


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