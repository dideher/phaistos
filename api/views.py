from django.db.models.query import QuerySet
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import serializers, status
from rest_framework.generics import get_object_or_404
from api.serializers import (
    EmployeeSerializer, 
    SpecializationSerializer, 
    EmployeeImportSerializer,
    LeaveImportSerializer,
    LeaveSerializer,
    LeaveTypeSerializer
)
from employees.models import (
    Employee, 
    Specialization,
)
from leaves.models import (
    Leave,
    LeaveType
)
from django.views.generic.list import ListView


class EmployeesAPIView(APIView):

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


class EmployeeImportAPIView(APIView):
    def post(self, request):
        
        serializer = EmployeeImportSerializer(data=request.data)
        
        if serializer.is_valid():
            validated_data = serializer.validated_data
            
            try:
                specialization = Specialization.objects.get(code=validated_data.get('specialization_code'))
            except Specialization.DoesNotExist:
                specialization = None
                

            employee = Employee.objects.create(
                minoas_id = validated_data.get('minoas_id'),
                big_family = validated_data.get('big_family'),
                comment = validated_data.get('comment'),
                date_of_birth = validated_data.get('date_of_birth'),
                email = validated_data.get('email'),
                father_name = validated_data.get('father_name'),
                father_surname = validated_data.get('father_surname'),
                first_name = validated_data.get('first_name'),
                last_name = validated_data.get('last_name'),
                id_number = validated_data.get('id_number'),
                id_number_authority = validated_data.get('id_number_authority'),
                is_man = validated_data.get('is_man'),
                mother_name = validated_data.get('mother_name'),
                mother_surname = validated_data.get('mother_surname'),
                vat_number = validated_data.get('minoas_id'),
                employee_type = validated_data.get('employee_type'),
                marital_status = validated_data.get('marital_status'),
                specialization = specialization,
            )
            
            employee_serializer = EmployeeSerializer(employee)
            return Response(employee_serializer.data, status=status.HTTP_201_CREATED)
        
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
        objs:QuerySet[Specialization] = Specialization.objects.filter()
        serializer = SpecializationSerializer(objs, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = SpecializationSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class SpecializationDetailAPI(APIView):

    def get_object(self, pk):
        return get_object_or_404(Specialization, pk=pk)

    def get(self, request, pk):
        obj = self.get_object(pk)
        serializer = SpecializationSerializer(obj)
        return Response(serializer.data)

    def put(self, request, pk):
        obj = self.get_object(pk)
        serializer = SpecializationSerializer(obj, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        obj = self.get_object(pk)
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

            leave = Leave.objects.create(
                minoas_id = validated_data.get('minoas_id'),
                employee = employee,
                leave_type = leave_type,
                is_active = validated_data.get('is_active'),
                comment = validated_data.get('comment'),
                date_from = validated_data.get('date_from'),
                date_until = validated_data.get('date_until'),
                effective_number_of_days = validated_data.get('effective_number_of_days'),
                number_of_days = validated_data.get('number_of_days'),
                is_deleted = validated_data.get('is_deleted'),
                deleted_on = validated_data.get('deleted_on'),
                deleted_comment = validated_data.get('deleted_comment'),
            )
            
            leave_serializer = LeaveSerializer(leave)
            return Response(leave_serializer.data, status=status.HTTP_201_CREATED)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)