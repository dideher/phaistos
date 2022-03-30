import logging

from django.db.models.query import QuerySet
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import serializers, status
from rest_framework.generics import get_object_or_404, CreateAPIView
from api.serializers import (
    EmployeeSerializer, 
    SpecializationSerializer, 
    EmployeeImportSerializer,
    LeaveImportSerializer,
    LeaveSerializer,
    LeaveTypeSerializer,
    UnitImportSerializer,
    UnitSerializer
)
from employees.models import (
    Employee, 
    Specialization,
    Unit,
    UnitType
)
from leaves.models import (
    Leave,
    LeaveType
)
from django.views.generic.list import ListView


class EmployeeListAPIView(APIView):

    def get(self, request):
        employees = Employee.objects.filter()
        serializer = EmployeeSerializer(employees, many=True)
        return Response(serializer.data)

    def post(self, request):

        serializer = EmployeeSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UnitImportAPIView(APIView):


    def insert_or_update_general_unit(self, serializer: UnitImportSerializer) -> Response:

        validated_data = serializer.validated_data

        try:
            general_unit: Unit = Unit.objects.get(minoas_id=validated_data.get('minoas_id'))
        except Unit.DoesNotExist:
            general_unit = None

        if general_unit is None:

            general_unit = Unit.objects.create(
                minoas_id=validated_data.get('minoas_id'),
                title=validated_data.get('title'),
                public_sector=validated_data.get('public_sector'),
                school_type=None,
                unit_type=UnitType.OTHER,
            )

            school_serializer = UnitSerializer(general_unit)
            return Response(school_serializer.data, status=status.HTTP_201_CREATED)

        else:
            general_unit.title = validated_data.get('title')
            general_unit.public_sector = validated_data.get('public_sector')

            general_unit.save()
            school_serializer = UnitSerializer(general_unit)
            return Response(school_serializer.data, status=status.HTTP_200_OK)

    def insert_or_update_school(self, serializer: UnitImportSerializer) -> Response:

        validated_data = serializer.validated_data

        try:
            school: Unit = Unit.objects.get(minoas_id=validated_data.get('minoas_id'))
        except Unit.DoesNotExist:
            school = None

        if school is None:

            school = Unit.objects.create(
                minoas_id=validated_data.get('minoas_id'),
                title=validated_data.get('title'),
                school_type=validated_data.get('school_type'),
                ministry_code=validated_data.get('ministry_code'),
                points=validated_data.get('points'),
                public_sector=validated_data.get('public_sector'),
                unit_type=UnitType.SCHOOL,
            )

            school_serializer = UnitSerializer(school)
            return Response(school_serializer.data, status=status.HTTP_201_CREATED)

        else:
            school.title = validated_data.get('title')
            school.school_type = validated_data.get('school_type')
            school.ministry_code = validated_data.get('ministry_code')
            school.points = validated_data.get('points')
            school.public_sector = validated_data.get('public_sector')

            school.save()
            school_serializer = UnitSerializer(school)

            return Response(school_serializer.data, status=status.HTTP_200_OK)

    def post(self, request):

        serializer = UnitImportSerializer(data=request.data)

        if serializer.is_valid():
            validated_data = serializer.validated_data
            if validated_data.get('is_school', False) is True:
                return self.insert_or_update_school(serializer)
            elif validated_data.get('is_general_unit', False) is True:
                return self.insert_or_update_general_unit(serializer)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class EmployeeImportAPIView(APIView):

    def post(self, request):
        
        serializer = EmployeeImportSerializer(data=request.data)
        
        if serializer.is_valid():
            validated_data = serializer.validated_data
            
            try:
                specialization: Specialization = Specialization.objects.get(code=validated_data.get('specialization_code'))
            except Specialization.DoesNotExist:
                specialization = None

            try:
                employee: Employee = Employee.objects.get(minoas_id=validated_data.get('minoas_id'))
            except Employee.DoesNotExist:
                employee = None

            current_unit_id = validated_data.get('current_unit_id')
            if current_unit_id is not None:
                try:
                    current_unit = Unit.objects.get(minoas_id=current_unit_id)
                except Unit.DoesNotExist:
                    current_unit = None
            else:
                current_unit = None

            if employee is None:

                employee = Employee.objects.create(
                    minoas_id=validated_data.get('minoas_id'),
                    big_family=validated_data.get('big_family'),
                    comment=validated_data.get('comment'),
                    date_of_birth=validated_data.get('date_of_birth'),
                    email=validated_data.get('email'),
                    father_name=validated_data.get('father_name'),
                    father_surname=validated_data.get('father_surname'),
                    first_name=validated_data.get('first_name'),
                    last_name=validated_data.get('last_name'),
                    id_number=validated_data.get('id_number'),
                    id_number_authority = validated_data.get('id_number_authority'),
                    is_man=validated_data.get('is_man'),
                    mother_name=validated_data.get('mother_name'),
                    mother_surname=validated_data.get('mother_surname'),
                    vat_number=validated_data.get('vat_number'),
                    employee_type=validated_data.get('employee_type'),
                    marital_status=validated_data.get('marital_status'),
                    specialization=specialization,
                    registry_id=validated_data.get('registry_id'),
                    current_unit=current_unit
                )

                employee_serializer = EmployeeSerializer(employee)
                return Response(employee_serializer.data, status=status.HTTP_201_CREATED)

            else:
                employee.big_family = validated_data.get('big_family')
                employee.comment = validated_data.get('comment')
                employee.date_of_birth =validated_data.get('date_of_birth')
                employee.email = validated_data.get('email')
                employee.father_name = validated_data.get('father_name')
                employee.father_surname = validated_data.get('father_surname')
                employee.first_name = validated_data.get('first_name')
                employee.last_name = validated_data.get('last_name')
                employee.id_number = validated_data.get('id_number')
                employee.id_number_authority = validated_data.get('id_number_authority')
                employee.is_man = validated_data.get('is_man')
                employee.mother_name = validated_data.get('mother_name')
                employee.mother_surname = validated_data.get('mother_surname')
                employee.vat_number = validated_data.get('vat_number')
                employee.employee_type = validated_data.get('employee_type')
                employee.marital_status = validated_data.get('marital_status')
                employee.specialization = specialization
                employee.registry_id = validated_data.get('registry_id')
                employee.current_unit = current_unit

                employee.save()
                employee_serializer = EmployeeSerializer(employee)
                return Response(employee_serializer.data, status=status.HTTP_200_OK)

        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class EmployeeDetailAPI(APIView):

    def get_object(self, pk):
        return get_object_or_404(Employee, pk=pk)

    def get(self, request, pk):
        employee = self.get_object(pk)
        serializer = EmployeeSerializer(employee)
        return Response(serializer.data)

    def put(self, request, pk):
        employee = self.get_object(pk)
        serializer = EmployeeSerializer(employee, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        employee = self.get_object(pk)
        employee.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class SpecializationAPIView(APIView):

    def get(self, request):
        objs: QuerySet[Specialization] = Specialization.objects.filter()
        serializer = SpecializationSerializer(objs, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = SpecializationSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class SpecializationDetailAPI(APIView):

    def get_object(self, code):
        return get_object_or_404(Specialization, code=code)

    def get(self, request, code):
        obj = self.get_object(code)
        serializer = SpecializationSerializer(obj)
        return Response(serializer.data)

    def put(self, request, code):
        obj = self.get_object(code)
        serializer = SpecializationSerializer(obj, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, code):
        obj = self.get_object(code)
        obj.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class LeaveTypesAPIView(APIView):

    def get(self, request):
        leavetype = LeaveType.objects.filter()
        serializer = LeaveTypeSerializer(leavetype, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = LeaveTypeSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LeaveTypeDetailAPI(APIView):

    def get_object(self, pk):
        return get_object_or_404(LeaveType, pk=pk)

    def get(self, request, pk):
        leavetype = self.get_object(pk)
        serializer = LeaveTypeSerializer(leavetype)
        return Response(serializer.data)

    def put(self, request, pk):
        leavetype = self.get_object(pk)
        serializer = LeaveTypeSerializer(leavetype, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        leavetype = self.get_object(pk)
        leavetype.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class LeaveImportAPIView(APIView):
    def post(self, request):
        
        serializer = LeaveImportSerializer(data=request.data)
        
        if serializer.is_valid():
            validated_data:dict = serializer.validated_data
            
            try:
                employee = Employee.objects.get(minoas_id=validated_data.get('minoas_employee_id'))
            except Employee.DoesNotExist:
                return Response({
                    'message': f"Employee {validated_data.get('minoas_employee_id')} could not be found"
                }, status=status.HTTP_404_NOT_FOUND)

            try:
                leave_type = LeaveType.objects.get(minoas_id=validated_data.get('minoas_leave_type_id'))
            except LeaveType.DoesNotExist:
                return Response({
                    'message': f"leave type {validated_data.get('minoas_leave_type_id')} could not be found"
                }, status=status.HTTP_404_NOT_FOUND)

            try:
                leave: Leave = Leave.objects.get(minoas_id=validated_data.get('minoas_id'))
            except Leave.DoesNotExist:
                leave = None

            if leave is None:

                leave = Leave.objects.create(
                    minoas_id=validated_data.get('minoas_id'),
                    employee=employee,
                    leave_type=leave_type,
                    is_active=validated_data.get('is_active'),
                    comment=validated_data.get('comment'),
                    date_from=validated_data.get('date_from'),
                    date_until=validated_data.get('date_until'),
                    effective_number_of_days=validated_data.get('effective_number_of_days'),
                    number_of_days=validated_data.get('number_of_days'),
                    is_deleted=validated_data.get('is_deleted'),
                    deleted_on=validated_data.get('deleted_on'),
                    deleted_comment=validated_data.get('deleted_comment'),
                )

                leave_serializer = LeaveSerializer(leave)
                return Response(leave_serializer.data, status=status.HTTP_201_CREATED)

            else:

                leave.minoas_id = validated_data.get('minoas_id')
                leave.employee = employee
                leave.leave_type = leave_type
                leave.is_active = validated_data.get('is_active')
                leave.comment = validated_data.get('comment')
                leave.date_from = validated_data.get('date_from')
                leave.date_until = validated_data.get('date_until')
                leave.effective_number_of_days = validated_data.get('effective_number_of_days')
                leave.number_of_days = validated_data.get('number_of_days')
                leave.is_deleted = validated_data.get('is_deleted')
                leave.deleted_on = validated_data.get('deleted_on')
                leave.deleted_comment = validated_data.get('deleted_comment')

                leave.save()
                leave_serializer = LeaveSerializer(leave)

                return Response(leave_serializer.data, status=status.HTTP_201_CREATED)

            
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)