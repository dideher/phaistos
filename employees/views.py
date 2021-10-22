from django.db.models.query import QuerySet
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import serializers, status
from rest_framework.generics import get_object_or_404
from .serializers import EmployeeSerializer, SpecializationSerializer, EmployeeImportSerializer
from .models import Employee, Specialization


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