from django.shortcuts import render
from leaves.models import LeaveType, Leave
from leaves.serializers import LeaveTypeSerializer

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
        serializer = LeaveTypeSerializer(employee)
        return Response(serializer.data)

    def put(self, request, pk):
        leavetype = self.get_object(pk)
        serializer = LeaveTypeSerializer(employee, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        leavetype = self.get_object(pk)
        leavetype.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
