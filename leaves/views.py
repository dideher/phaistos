from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from employees.models import Employee
from leaves.models import LeaveType, Leave
from leaves.serializers import LeaveTypeSerializer, LeaveSerializer, LeaveImportSerializer
from rest_framework import serializers, status
from rest_framework.generics import get_object_or_404

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