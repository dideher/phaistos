import json
import logging

from django.db.models.query import QuerySet
from django.utils.timezone import now
from django.db import transaction

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import serializers, status
from rest_framework import generics

from rest_framework.generics import get_object_or_404, CreateAPIView, ListCreateAPIView
from rest_framework.permissions import IsAdminUser
from rest_framework.exceptions import ValidationError
from api.serializers import (
    EmployeeSerializer,
    EmploymentSerializer,
    SpecializationSerializer,
    EmployeeImportSerializer,
    LeaveImportSerializer,
    LeaveSerializer,
    LeaveTypeSerializer,
    UnitImportSerializer,
    UnitSerializer,
    AthinaEmployeeImportSerializer,
    MySchoolEmployeeImportSerializer,
    MySchoolEmploymentImportSerializer,
    SchoolPrincipalSerializer
)
from api.core.pagination import StandardResultsSetPagination
from api.cache import get_cached_employee_type, get_cached_employee_specialization, get_cached_unit, get_cached_employment_type
from employees.models import (
    Employee,
    Specialization,
    Unit,
    UnitType,
    EmployeeType,
    LegacyEmployeeType,
    WorkExperience,
    WorkExperienceType,
    Employment,
    EmploymentType,
    LegacyEmploymentType,
    EmploymentStatus,
    SchoolPrincipals
)
from leaves.models import (
    Leave,
    LeaveType,
)
from main.models import SchoolYear


class SchoolPrincipalImportSerializer(serializers.Serializer):
    """
    Special Serializer to be used for bulk importing school principals from MySchool
    """
    employee_afm = serializers.CharField(allow_blank=False, required=True)
    employee_am = serializers.CharField(allow_blank=False, required=True)
    assignment_unit_id = serializers.CharField(allow_null=False, allow_blank=False, required=True)
    # assignment_from = serializers.DateField(format='%d/%m/%Y', input_formats=['%d/%m/%Y', ], required=True, allow_null=False)
    # assignment_until = serializers.DateField(format='%d/%m/%Y', input_formats=['%d/%m/%Y', ], required=True, allow_null=False)


class SchoolPrincipalImportAPIView(APIView):

    def post(self, request):

        serializer = SchoolPrincipalImportSerializer(data=request.data)

        if serializer.is_valid() is False:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        validated_data = serializer.validated_data

        employee_afm = validated_data.get('employee_afm')
        employee_am = validated_data.get('employee_am')
        assignment_unit_id = validated_data.get('assignment_unit_id')


        with transaction.atomic():

            try:
                assignment_unit: Unit = get_cached_unit(assignment_unit_id)
            except Unit.DoesNotExist:
                logging.error(f'******* unit {assignment_unit_id} could not be found')
                return Response({"error": "unit could not be found"}, status=status.HTTP_404_NOT_FOUND)

            # first try to match employee with AM
            employee: Employee = None

            if len(employee_am) > 0:
                employees: QuerySet[Employee] = Employee.objects.filter(
                    registry_id=employee_am,
                    is_active=True,
                    employee_type=LegacyEmployeeType.REGULAR)
                if employees.count() > 0:
                    employee: Employee = employees.first()

            # if we failed to match, then try with AFM
            if employee is None and len(employee_afm) > 0:
                employees: QuerySet[Employee] = Employee.objects.filter(
                    vat_number=employee_afm,
                    is_active=True,
                    employee_type=LegacyEmployeeType.REGULAR)

                if employees.count() > 0:
                    employee: Employee = employees.first()

            if employee is None:
                # we failed to match the employee
                msg = f'******* employee with AFM {employee_afm} or AM {employee_am} could not be found'
                logging.error(msg)
                return Response({"error": msg}, status=status.HTTP_404_NOT_FOUND)

            today = now()

            school_principal_dict = {
                'employee': employee,
                'current_unit': assignment_unit,
                'school_year': SchoolYear.get_current_school_year()
            }
            from django.db import IntegrityError
            try:
                school_principal: SchoolPrincipals = SchoolPrincipals.objects.create(**school_principal_dict)
            except IntegrityError as e:
                logging.warning("failed to process request '%s' due to : %s", school_principal_dict, e)
                return Response({"error": e.args[0], 'payload': school_principal_dict}, status=status.HTTP_409_CONFLICT)
                pass

            return Response(SchoolPrincipalSerializer(school_principal).data, status=status.HTTP_201_CREATED)
